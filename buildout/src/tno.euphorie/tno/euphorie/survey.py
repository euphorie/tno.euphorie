from five import grok
from euphorie.client.survey import SurveyPublishTraverser
from euphorie.client.survey import ActionPlanReportView
from tno.euphorie.interfaces import ITnoIdentificationPhaseSkinLayer
from tno.euphorie.interfaces import ITnoEvaluationPhaseSkinLayer
from tno.euphorie.interfaces import ITnoActionPlanPhaseSkinLayer
from tno.euphorie.interfaces import ITnoReportPhaseSkinLayer

grok.templatedir("templates")

class TnoSurveyPublishTraverser(SurveyPublishTraverser):
    phases = {
            "identification": ITnoIdentificationPhaseSkinLayer,
            "evaluation": ITnoEvaluationPhaseSkinLayer,
            "actionplan": ITnoActionPlanPhaseSkinLayer,
            "report": ITnoReportPhaseSkinLayer,
            }


class TnoActionPlanReportView(ActionPlanReportView):
    grok.layer(ITnoReportPhaseSkinLayer)
    grok.name("view")
    grok.template("report_actionplan")

