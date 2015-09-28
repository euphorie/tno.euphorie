from five import grok
from zope.component import getUtility
from z3c.appconfig.interfaces import IAppConfig
from plonetheme.nuplone.utils import getPortal
from euphorie.content.survey import Edit as EuphorieEdit
from euphorie.content.survey import View as EuphorieView
from euphorie.content.survey import ISurvey
from .interfaces import ITnoContentSkinLayer
from .schema import UUID


grok.templatedir('templates')


class ITnoSurvey(ISurvey):
    """This schema adds all fields related to the Ondernemingsdossier."""

    regelhulp_id = UUID(
            title=u'Regelhulp Id',
            description=
                u'De regelhulp id wordt toegewezen door het ondernemingsdossier '
                u'als de RI&E wordt opgenemen als regelhulp.',
            required=False)


@grok.adapter(ISurvey)
@grok.implementer(ITnoSurvey)
def context_proxy(content):
    """Trivial adapter to pretend all surveys implement ITnoSurvey. This allows
    us to use ITnoSurvey without persisting it or a custom content class in the
    database so we keep a clean migration path.
    """
    return content


class View(EuphorieView):
    grok.context(ISurvey)
    grok.require('zope2.View')
    grok.layer(ITnoContentSkinLayer)
    grok.template('survey_view')
    grok.name('nuplone-view')

    def client_url(self):
        config = getUtility(IAppConfig)
        client_url = config.get("euphorie", {}).get("client")
        if not client_url:
            client_url = getPortal(self.context).client.absolute_url()
        return client_url.rstrip('/')

    def update(self):
        super(View, self).update()
        steps = self.request.steps
        self.od_entry_url = '%s/%s/%s/%s/@@od-entry' % (
                self.client_url(), steps[-5], steps[-4], steps[-3])


class EditForm(EuphorieEdit):
    grok.context(ISurvey)
    grok.require('cmf.ModifyPortalContent')
    grok.layer(ITnoContentSkinLayer)
    schema = ITnoSurvey
