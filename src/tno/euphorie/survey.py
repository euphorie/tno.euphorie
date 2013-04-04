from sqlalchemy import sql
from five import grok
from euphorie.client import model
from euphorie.client.survey import PathGhost
from euphorie.client.survey import ActionPlan
from euphorie.client.survey import SurveyPublishTraverser
from tno.euphorie.interfaces import ITnoIdentificationPhaseSkinLayer
from tno.euphorie.interfaces import ITnoEvaluationPhaseSkinLayer
from tno.euphorie.interfaces import ITnoActionPlanPhaseSkinLayer
from tno.euphorie.interfaces import ITnoReportPhaseSkinLayer

class TnoSurveyPublishTraverser(SurveyPublishTraverser):
    phases = {
            'identification': ITnoIdentificationPhaseSkinLayer,
            'evaluation': ITnoEvaluationPhaseSkinLayer,
            'actionplan': ITnoActionPlanPhaseSkinLayer,
            'report': ITnoReportPhaseSkinLayer,
            }


grok.templatedir('templates')


class TnoActionPlanView(ActionPlan):
    grok.context(PathGhost)
    grok.require('euphorie.client.ViewSurvey')
    grok.layer(ITnoActionPlanPhaseSkinLayer)
    grok.template('actionplan')
    grok.name('index_html')

    question_filter = sql.or_(model.MODULE_WITH_RISK_FILTER,
                              model.RISK_PRESENT_FILTER)
