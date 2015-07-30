import datetime
import logging
import urlparse
import uuid
from urllib import urlencode
from lxml import etree
from sqlalchemy import orm
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_base
from Acquisition import aq_inner
from zExceptions import Unauthorized
from zExceptions import NotFound
from five import grok
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import Interface
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
from tno.euphorie.model import DutchCompany
from tno.euphorie.model import OdLink
from tno.euphorie.report import TnoActionPlanReportDownload


EUPHORIE_NAMESPACE_UUID = uuid.UUID('0002320c-e708-4837-bfc4-8a92ad6e0579')

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


class OdWebHelpers(grok.View):
    """Modified @@webhelpers view.
    """
    grok.context(Interface)
    grok.layer(ITnoClientSkinLayer)
    grok.require('zope2.View')
    grok.name('od')

    def is_od_session(self):
        account = aq_base(getSecurityManager().getUser())
        return isinstance(account, model.Account) and account.password is None

    def render(self):
        pass


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


class ODReportDownload(grok.View):
    """Entry point from OndernemingsDossier.
    """
    grok.context(ISurvey)
    grok.require("zope2.View")
    grok.layer(ITnoClientSkinLayer)
    grok.name('od-report')

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
        if link is None:
            return NotFound()
        else:
            self.request.survey = aq_inner(self.context)
            view = TnoActionPlanReportDownload(self.request.survey, self.request)
            view.session = link.session
            if view.session.dutch_company is None:
                view.session.dutch_company = DutchCompany()
            return view.render()


NS_REGELHULP = 'http://ondernemingsdossier.nl/nta9040-1/2.0/regelhulpresponse.xsd'
NS_XMLSI = 'http://www.w3.org/2001/XMLSchema-instance'
NSMAP = {
        None: NS_REGELHULP,
        'xsi': NS_XMLSI,
        }


def _tag(name, ns=NS_REGELHULP):
    return etree.QName(ns, name)


def add_response_metadata(regelhulp, survey, od_link):
    metadata = etree.SubElement(regelhulp, _tag('RegelhulpResponseMetadata'))
    etree.SubElement(metadata, _tag('Vestigingssleutel')).text = od_link.vestigings_sleutel
    etree.SubElement(metadata, _tag('Foutcode')).text = u'0'
    etree.SubElement(metadata, _tag('Datum')).text = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    bijlage = etree.SubElement(metadata, _tag('RegelhulpBijlage'))
    etree.SubElement(bijlage, _tag('Bestandsnaam')).text = 'plan-van-aanpak.rtf'
    etree.SubElement(bijlage, _tag('DownloadUri')).text = '%s/@@od-report?vestigingssleutel=%s' % (survey.absolute_url(), od_link.vestigings_sleutel)
    etree.SubElement(bijlage, _tag('VestionMajor')).text = '1'
    etree.SubElement(bijlage, _tag('VestionMinor')).text = '1'


def add_response_kern(regelhulp, survey, od_link):
    kern = etree.SubElement(regelhulp, _tag('RegelhulpResponseKern'))
    wos = etree.SubElement(kern, _tag('WettelijkOnderwerpen'))
    wo = etree.SubElement(wos, _tag('WettelijkOnderwerp'))
    wid = etree.SubElement(wo, _tag('WettelijkOnderwerpId'))
    etree.SubElement(wid, _tag('Uuid')).text = 'XXX'  # XXX UUID voor wettelijker onderwerp
    etree.SubElement(wid, _tag('VersionMajor')).text = '1'
    etree.SubElement(wid, _tag('VersionMinor')).text = '1'
    etree.SubElement(wo, _tag('Naam')).text = u'Risico Inventarisatie & Evaludatie'
    etree.SubElement(wo, _tag('Definitie')).text = u'Formele definitie wettelijk onderwerp, zoals opgenomen in bron'  # XXX Te bepalen
    etree.SubElement(wo, _tag('Bron')).text = u'RI&E bron'  # XXX Te bepalen
    etree.SubElement(wo, _tag('Verwijzing')).text = u'URL voor RI&E besluit of wet'  # XXX Te bepalen

    voorschriften = etree.SubElement(wo, _tag('LijstVoorschriften'))
    vs = etree.SubElement(voorschriften, _tag('Voorschrift'))
    vsid = etree.SubElement(vs, _tag('VoorschriftId'))
    etree.SubElement(vsid, _tag('Uuid')).text = 'XXX'  # XXX UUID voor voorschift
    etree.SubElement(vsid, _tag('VersionMajor')).text = '1'
    etree.SubElement(vsid, _tag('VersionMinor')).text = '1'
    etree.SubElement(vs, _tag('Aanduiding')).text = 'Aanduiding uit bron waar voorschift uit komt (bv. artikel 123)'  # XXX Te bepalen
    etree.SubElement(vs, _tag('Verwijzing')).text = 'URL voor voorschrift'  # XXX Te bepalen

    maatregelen = etree.SubElement(vs, _tag('LijstMaatregelen'))
    mr = etree.SubElement(maatregelen, _tag('Maatregel'))
    mrid = etree.SubElement(mr, _tag('MaatregelId'))
    etree.SubElement(mrid, _tag('Uuid')).text = str(uuid.uuid3(EUPHORIE_NAMESPACE_UUID, str(od_link.session.zodb_path)))
    etree.SubElement(mrid, _tag('VersionMajor')).text = '1'
    etree.SubElement(mrid, _tag('VersionMinor')).text = '1'
    etree.SubElement(mr, _tag('Omschrijving')).text = u'Korte omschrijving maatregel'  # XXX Te bepalen
    etree.SubElement(mr, _tag('Brontype')).text = u'regelhulp branche'

    tkp = etree.SubElement(mr, _tag('Terugkeerpatroon'))
    etree.SubElement(tkp, _tag('HerhaalFrequentie')).text = u'jaarlijks'
    etree.SubElement(tkp, _tag('Interval')).text = u'1'


def create_response(survey, od_link):
    response = etree.Element(_tag('RegelhulpResponse'), nsmap=NSMAP)
    response.attrib[_tag('schemalocation', NS_XMLSI)] = 'http://www.ondernemingsdossier.nl/nta9040-1/2.0/regelhulpresponse.xsd'
    add_response_metadata(response, survey, od_link)
    add_response_kern(response, survey, od_link)
    return response


class ODResponse(grok.View):
    grok.context(ISurvey)
    grok.require('euphorie.client.ViewSurvey')
    grok.layer(ITnoClientSkinLayer)
    grok.name('od-response')

    def render(self):
        session = SessionManager.session
        response = create_response(aq_inner(self.context), session.od_link)
        self.request.response.setHeader('content-text', 'text/html')
        return etree.tostring(response, pretty_print=True, xml_declaration=True, encoding='utf-8')
