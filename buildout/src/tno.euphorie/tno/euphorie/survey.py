from euphorie.client.survey import SurveyPublishTraverser
from tno.euphorie.interfaces import ITnoIdentificationPhaseSkinLayer
from tno.euphorie.interfaces import ITnoEvaluationPhaseSkinLayer
from tno.euphorie.interfaces import ITnoActionPlanPhaseSkinLayer
from tno.euphorie.interfaces import ITnoReportPhaseSkinLayer

class TnoSurveyPublishTraverser(SurveyPublishTraverser):
    phases = {
            "identification": ITnoIdentificationPhaseSkinLayer,
            "evaluation": ITnoEvaluationPhaseSkinLayer,
            "actionplan": ITnoActionPlanPhaseSkinLayer,
            "report": ITnoReportPhaseSkinLayer,
            }


