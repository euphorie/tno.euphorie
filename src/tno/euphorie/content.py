from five import grok
from euphorie.content.survey import Edit as EuphorieEdit
from euphorie.content.survey import ISurvey
from .interfaces import ITnoContentSkinLayer
from .schema import UUID


class ITnoSurvey(ISurvey):
    """This schema adds all fields related to the Ondernemings Dossier."""

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


class EditForm(EuphorieEdit):
    grok.context(ISurvey)
    grok.require('cmf.ModifyPortalContent')
    grok.layer(ITnoContentSkinLayer)
    schema = ITnoSurvey
