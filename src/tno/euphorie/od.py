import datetime
import hashlib
import logging
import os
import urlparse
import uuid
from urllib import urlencode
import osa
from sqlalchemy import orm
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_base
from Acquisition import aq_inner
from zExceptions import Forbidden
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
from Products.statusmessages.interfaces import IStatusMessage
from euphorie import MessageFactory as _
from euphorie.client import model
from euphorie.client import utils
from euphorie.content.survey import ISurvey
from euphorie.client.authentication import authenticate
from euphorie.client.profile import Profile
from euphorie.client.session import SessionManager
from tno.euphorie.interfaces import ITnoClientSkinLayer
from tno.euphorie.model import DutchCompany
from tno.euphorie.model import OdLink
from tno.euphorie.report import TnoActionPlanReportDownload
from euphorie import client


#: Path to original Euphorie client templates
ORIG_TEMPLATE_PATH = os.path.join(client.__path__[0], 'templates')


NAMESPACE_EUPHORIE = uuid.UUID('0002320c-e708-4837-bfc4-8a92ad6e0579')
NAMESPACE_WO = uuid.UUID('32f0e6ea-b54f-45ef-b15e-b85f31d55655')

REGELHULP_UUID = '9963734c-7003-4104-ac56-cc53744f9bae'
THEMA_UUID = '5f9a53a5-84f6-40f7-89ef-253e7d1fa842'  # Arbo thema
PVA_UUID = '68487da9-18af-49e9-bece-fd4cb613c728'  # Plan van Aanpak voorschrift


log = logging.getLogger(__name__)
grok.templatedir("templates")


class EntrySchema(form.Schema):
    existing = schema.Choice(
            title=u'Heeft u al een RI&E buiten het Ondernemingsdossier?',
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
    """Entry point from Ondernemingsdossier.
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

    def update(self):
        if not getattr(aq_base(aq_inner(self.context)), 'regelhulp_id', None):
            log.error('OD entry, but survey has no regelhulp id.')
            raise NotFound()
        utils.setLanguage(self.request, self.context, self.context.language)

    def render(self):
        vestiging = self.request.form['vestigingssleutel']
        session = Session()
        zodb_path = utils.RelativePath(self.request.client, self.context)
        link = session.query(OdLink)\
                .join(model.SurveySession)\
                .filter(OdLink.vestigings_sleutel == vestiging)\
                .filter(model.SurveySession.zodb_path == zodb_path)\
                .options(orm.joinedload_all('session.account', innerjoin=True))\
                .first()
        if link is not None:
            self._start(link)
        else:
            url = '%s/@@od-offer-link?%s' % (self.context.absolute_url(), urlencode(self.request.form))
            self.request.response.redirect(url)


class ODOfferLink(form.SchemaForm):
    """Entry point from Ondernemingsdossier.
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
        session = Session()
        # Check if there is an account from another regelhulp for the same
        # vestiging.
        account = session.query(model.Account)\
            .filter(model.Account.loginname == vestigings_sleutel)\
            .first()
        if account is None:
            # Create a new account
            account = model.Account(
                    loginname=vestigings_sleutel,
                    password=None)
            session.add(account)
            session.flush()  # Make sure account.id is set
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
    """Entry point from Ondernemingsdossier.
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
        zodb_path = utils.RelativePath(self.request.client, self.context)
        link = session.query(OdLink)\
                .join(model.SurveySession)\
                .filter(OdLink.vestigings_sleutel == vestiging)\
                .filter(model.SurveySession.zodb_path == zodb_path)\
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


def create_response_metadata(survey, od_link, client):
    metadata = client.types.RegelhulpResponseMetadata(True)
    metadata.Vestigingssleutel = od_link.vestigings_sleutel
    metadata.Foutcode = u'0'
    metadata.Datum = datetime.datetime.now()
    metadata.RegelhulpId = survey.regelhulp_id
    return metadata


def create_response_kern(survey, od_link, client):
    kern = client.types.RegelhulpResponseKern(True)
    wo = client.types.WettelijkOnderwerp(True)
    kern.LijstWettelijkeOnderwerpen = client.types.ArrayOfWettelijkOnderwerp()
    kern.LijstWettelijkeOnderwerpen.WettelijkOnderwerp = [wo]

    wo.WettelijkOnderwerpId = wid = client.types.Id(True)
    # The UUID is specific to the survey so we can include the survey title
    # in the naam.
    wid.Uuid = uuid.uuid3(NAMESPACE_WO, str(od_link.session.zodb_path))
    wid.VersionMajor = 1
    wid.VersionMinor = 1

    wo.Thema = thema = client.types.Thema(True)
    thema.ThemaNaam = u'Arbeidsomstandighedenbeleid'
    thema.ThemaId = THEMA_UUID

    wo.Definitie = u'Formele definitie wettelijk onderwerp, zoals opgenomen in bron'  # XXX Te bepalen
    wo.Naam = u'Risico Inventarisatie & Evaluatie: %s' % survey.Title()
    wo.Bron = u'Arbeidsomstandighedenwet 1998, Artikel 5 lid 3'
    wo.Verwijzing = u'http://wetten.overheid.nl/BWBR0010346/geldigheidsdatum_10-08-2015#Hoofdstuk2_PAR624212'

    vs = client.types.Voorschrift(True)
    wo.LijstVoorschriften = client.types.ArrayOfVoorschrift()
    wo.LijstVoorschriften.Voorschrift = [vs]

    vs.VoorschriftId = vsid = client.types.Id(True)
    vsid.Uuid = PVA_UUID
    vsid.VersionMajor = 1
    vsid.VersionMinor = 1
    vs.Aanduiding = u'Artikel 5 lid 4'
    vs.Citaat = (
            u'Een plan van aanpak, waarin is aangegeven welke maatregelen '
            u'zullen worden genomen in verband met de bedoelde risico\'s en '
            u'de samenhang daartussen, een en ander overeenkomstig '
            u'<a href="http://wetten.overheid.nl/BWBR0010346/geldigheidsdatum_10-08-2015#Hoofdstuk2_PAR623742_Artikel3">artikel 3</a>, '
            u'maakt deel uit van de risico-inventarisatie en -evaluatie. '
            u'In het plan van aanpak wordt tevens aangegeven binnen welke '
            u'termijn deze maatregelen zullen worden genomen.')
    vs.Bron = u'Arbeidsomstandighedenwet 1998'
    vs.Verwijzing = u'http://wetten.overheid.nl/BWBR0010346/geldigheidsdatum_10-08-2015#Hoofdstuk2_PAR624212'

    mr = client.types.Maatregel(True)
    vs.LijstMaatregelen = client.types.ArrayOfMaatregel()
    vs.LijstMaatregelen.Maatregel = [mr]
    mr.MaatregelId = mrid = client.types.Id(True)
    # This is a variant of standard version 5 UUIDs: we include two extras
    # in the SHA1 hash isntead of one.
    hash = hashlib.new('sha1')
    hash.update(NAMESPACE_EUPHORIE.bytes)
    hash.update(od_link.session.zodb_path)
    hash.update(od_link.vestigings_sleutel)
    mrid.Uuid = str(uuid.UUID(bytes=hash.digest()[:16], version=5))

    mrid.VersionMajor = 1
    mrid.VersionMinor = od_link.version
    report_url = '%s/@@od-report?vestigingssleutel=%s' % \
            (survey.absolute_url(), od_link.vestigings_sleutel)
    mr.Omschrijving = u'Controleer voortgang en plan van aanpak en actualiteit RI&E.'
    mr.Toelichting = (
            u'<p>Controleer of de maatregelen in het <a target="_blank" '
            u'href="%s">plan van aanpak</a> op tijd worden uitgevoerd.</p>'
    ) % report_url
    mr.Brontype = u'regelhulp branche'

    mr.Terugkeerpatroon = tkp = client.types.Terugkeerpatroon(True)
    tkp.HerhaalFrequentie = u'Jaarlijks'
    tkp.Interval = u'1'

    return kern


def create_response(survey, od_link, client):
    response = client.types.RegelhulpResponse(True)
    response.RegelhulpResponseMetadata = create_response_metadata(survey, od_link, client)
    response.RegelhulpResponseKern = create_response_kern(survey, od_link, client)
    return response


class ODResponse(grok.View):
    grok.context(ISurvey)
    grok.require('euphorie.client.ViewSurvey')
    grok.layer(ITnoClientSkinLayer)
    grok.name('od-response')

    def update(self):
        if self.request.method != 'POST':
            raise Forbidden()

    def render(self):
        flash = IStatusMessage(self.request).addStatusMessage
        session = SessionManager.session
        client = osa.Client(session.od_link.wsdl_url)
        session.od_link.version += 1
        response = create_response(aq_inner(self.context), session.od_link, client)
        r = client.service.SetRegelhulpResponse(response)
        if r.Foutcode != 0:
            log.error('SetRegelhulpResponse error %d: %s',
                    r.Foutcode, r.Foutbericht)
            flash(u'Er is een fout opgetreden bij het bijwerken van uw Ondernemingsdossier. U kunt het later nog een keer proberen.', 'error')
        else:
            if session.od_link.version == 1:
                flash(u'Het plan van aanpak is opgenomen in uw Ondernemingsdossier.', 'success')
            else:
                flash(u'Het plan van aanpak in uw Ondernemingsdossier is bijgewerkt.', 'success')
        self.request.response.redirect("%s/report/view" % self.context.absolute_url())


class OdProfile(Profile):
    """(Re)set the survey profile, while keeping the OD link uptodate.
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(ITnoClientSkinLayer)
    grok.name("profile")
    grok.template(os.path.join(ORIG_TEMPLATE_PATH, "profile"))

    def setupSession(self):
        od_link = self.session.od_link
        super(OdProfile, self).setupSession()
        s = Session()
        if od_link.session in s.deleted:
            s.expunge(od_link)
            new_link = OdLink(
                    session=self.session,
                    vestigings_sleutel=od_link.vestigings_sleutel,
                    webservice=od_link.webservice)
            s.add(new_link)


class OdProfileUpdate(OdProfile):
    """Update a survey session after a survey has been republished. If a
    the survey has a profile the user is asked to confirm the current
    profile before continueing.

    The behaviour is exactly the same as the normal start page for a session
    (see the :py:class:`Profile` view), but uses a different template with more
    detailed instructions for the user.
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(ITnoClientSkinLayer)
    grok.template(os.path.join(ORIG_TEMPLATE_PATH, "updated"))
    grok.name("update")
