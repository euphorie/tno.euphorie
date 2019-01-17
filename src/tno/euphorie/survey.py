# coding=utf-8
from euphorie.client import model
from euphorie.client.interfaces import ICustomizationPhaseSkinLayer
from euphorie.client.survey import ActionPlan
from euphorie.client.survey import PathGhost
from euphorie.client.survey import Status
from euphorie.client.survey import SurveyPublishTraverser
from euphorie.content.survey import ISurvey
from five import grok
from sqlalchemy import sql
from tno.euphorie.interfaces import ITnoActionPlanPhaseSkinLayer
from tno.euphorie.interfaces import ITnoEvaluationPhaseSkinLayer
from tno.euphorie.interfaces import ITnoIdentificationPhaseSkinLayer
from tno.euphorie.interfaces import ITnoReportPhaseSkinLayer
from tno.euphorie.interfaces import ITnoClientSkinLayer

grok.templatedir('templates')


class TnoSurveyPublishTraverser(SurveyPublishTraverser):
    phases = {
        'identification': ITnoIdentificationPhaseSkinLayer,
        'customization': ICustomizationPhaseSkinLayer,
        'evaluation': ITnoEvaluationPhaseSkinLayer,
        'actionplan': ITnoActionPlanPhaseSkinLayer,
        'report': ITnoReportPhaseSkinLayer,
    }


class TnoActionPlanView(ActionPlan):
    grok.context(PathGhost)
    grok.require('euphorie.client.ViewSurvey')
    grok.layer(ITnoActionPlanPhaseSkinLayer)
    grok.template('actionplan')
    grok.name('index_html')

    question_filter = sql.or_(model.MODULE_WITH_RISK_TOP5_TNO_FILTER,
                              model.RISK_PRESENT_FILTER_TOP5_TNO_FILTER)


class TNOStatus(Status):
    grok.context(ISurvey)
    grok.layer(ITnoClientSkinLayer)
    grok.name("status")

    show_high_risks = False
