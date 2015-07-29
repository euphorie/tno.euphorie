import logging
import urlparse
from urllib import urlencode
from sqlalchemy import orm
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_base
from Acquisition import aq_inner
from zExceptions import Unauthorized
from five import grok
from zope import schema
from zope.component import getMultiAdapter
from z3c.saconfig import Session
from z3c.form import button
from z3c.form.interfaces import IErrorViewSnippet
from zope.interface import Invalid
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.directives import form
from plonetheme.nuplone.tiles.analytics import trigger_extra_pageview
from Products.CMFCore.utils import getToolByName
from euphorie import MessageFactory as _
from euphorie.client import model
from euphorie.client import utils
from euphorie.content.survey import ISurvey
from euphorie.client.authentication import authenticate
from euphorie.client.session import SessionManager
from tno.euphorie.interfaces import ITnoClientSkinLayer
from tno.euphorie.model import OdLink


log = logging.getLogger(__name__)
grok.templatedir("templates")


class EntrySchema(form.Schema):
    existing = schema.Choice(
            title=u'Heeft U al een RI&E buiten het Ondernemings Dossier?',
            vocabulary=SimpleVocabulary([
                SimpleTerm('new', title='Tralala'),
                SimpleTerm('existing', title='Tralala'),
                ]),
            required=True)

    email = schema.TextLine(
            title=_('label_email', default=u'Email address'),
            required=True)
    password = schema.TextLine(title=u'Wachtwoord', required=True)


class ODEntry(grok.View):
    """Entry point from OndernemingsDossier.
    """
    grok.context(ISurvey)
    grok.require("zope2.View")
    grok.layer(ITnoClientSkinLayer)
    grok.name('od-entry')

    def _start(self, link):
        pas = getToolByName(self.context, 'acl_users')
        pas.updateCredentials(self.request, self.response,
                link.session.account.loginname, None)
        newSecurityManager(None, link.session.account)
        SessionManager.resume(link.session)
        survey = self.request.client.restrictedTraverse(str(link.session.zodb_path))
        v_url = urlparse.urlsplit(self.url() + '/od-resume').path
        trigger_extra_pageview(self.request, v_url)
        self.request.response.redirect("%s/resume" % survey.absolute_url())

    def render(self):
        vestiging = self.request.form['vestigingssleutel']
        session = Session()
        link = session.query(OdLink)\
                .filter(OdLink.vestigings_sleutel == vestiging)\
                .options(orm.joinedload_all('session.account', innerjoin=True))\
                .first()
        if link is not None:
            self._start(link)
        else:
            url = '%s/@@od-offer-link?%s' % (self.context.absolute_url(), urlencode(self.request.form))
            self.request.response.redirect(url)


class ODOfferLink(form.SchemaForm):
    """Entry point from OndernemingsDossier.
    """
    grok.context(ISurvey)
    grok.require("zope2.View")
    grok.layer(ITnoClientSkinLayer)
    grok.name('od-offer-link')
    grok.template('od_offer_link')
    form.wrap(False)

    ignoreContext = True
    schema = EntrySchema

    def _newLink(self, vestigings_sleutel, webservice):
        # Create a new account
        account = model.Account(
                loginname=vestigings_sleutel,
                password=None)
        Session.add(account)
        Session.flush()  # Make sure account.id is set
        log.info('Created new OD account %s for %s', account.loginname, self.url())

        # Login with the account
        newSecurityManager(None, account)
        pas = getToolByName(self.context, 'acl_users')
        pas.updateCredentials(self.request, self.response, account.loginname, None)

        # And start a new survey
        survey = aq_inner(self.context)
        ss = SessionManager.start(title=survey.Title(), survey=survey)
        Session.add(OdLink(
            session=ss,
            vestigings_sleutel=vestigings_sleutel,
            webservice=webservice))
        v_url = urlparse.urlsplit(survey.absolute_url() + '/od-new').path
        trigger_extra_pageview(self.request, v_url)
        self.request.response.redirect('%s/start' % survey.absolute_url())

    def _tryLogin(self, login, password):
        account = authenticate(login, password)
        if account is None:
            widget = self.widgets['email']
            err = getMultiAdapter(
                    (Invalid(u'Login gegevens zijn niet correct'),
                        self.request, widget, widget.field, self, self.context),
                    interface=IErrorViewSnippet)
            err.update()
            widget.error = err
            return None
        pas = getToolByName(self.context, 'acl_users')
        pas.updateCredentials(self.request, self.response,
                account.loginname, None)
        return account

    @button.buttonAndHandler(u'Verder')
    def handleVerder(self, action):
        (data, errors) = self.extractData()
        request = self.request
        if data['existing'] == 'new':  # Ignore errors in this case
            self._newLink(request.form['vestigingssleutel'], request.form['webservice'])
        else:
            account = self._tryLogin(data['email'], data['password'])
            if account is not None:
                self.request.response.redirect('%s/@@od-select-session?%s' % (
                    aq_inner(self.context).absolute_url(),
                    urlencode({
                        'vestigingssleutel': request.form['vestigingssleutel'],
                        'webservice': request.form['webservice']})))


# This is heavily based on euphorie.client.survey.View
class ODSelectSession(grok.View):
    grok.context(ISurvey)
    grok.require('euphorie.client.ViewSurvey')
    grok.layer(ITnoClientSkinLayer)
    grok.template('od_select_session')
    grok.name('od-select-session')

    def sessions(self):
        """Return a list of all sessions for the current user. For each
        session a dictionary is returned with the following keys:

        * `id`: unique identifier for the session
        * `title`: session title
        * `modified`: timestamp of last session modification
        """
        survey = aq_inner(self.context)
        my_path = utils.RelativePath(self.request.client, survey)
        account = getSecurityManager().getUser()
        result = [{'id': session.id,
                 'title': session.title,
                 'modified': session.modified}
                 for session in account.sessions
                 if session.zodb_path == my_path]
        result.sort(key=lambda s: s['modified'], reverse=True)
        return result

    def _continue(self, session_id, vestigings_sleutel, webservice):
        session = Session.query(model.SurveySession).get(session_id)
        account = aq_base(getSecurityManager().getUser())
        if session.account is not account:
            log.warn('User %s tried to hijack session from %s',
                    getattr(account, 'loginname', repr(account)),
                    session.account.loginname)
            raise Unauthorized()

        Session.add(OdLink(
            session=session,
            vestigings_sleutel=vestigings_sleutel,
            webservice=webservice))

        SessionManager.resume(session)
        survey = self.request.client.restrictedTraverse(str(session.zodb_path))
        v_url = urlparse.urlsplit(self.url() + '/od-link').path
        trigger_extra_pageview(self.request, v_url)
        self.request.response.redirect("%s/resume" % survey.absolute_url())

    def update(self):
        request = self.request
        if request.environ["REQUEST_METHOD"] == "POST":
            self._continue(request.form['session'], request.form['vestigingssleutel'], request.form['webservice'])
        else:
            self.previous_url = '%s/@@od-offer-link?%s' % (
                    aq_inner(self.context).absolute_url(),
                    urlencode({
                        'vestigingssleutel': request.form['vestigingssleutel'],
                        'webservice': request.form['webservice']}))
