from sqlalchemy import sql
from five import grok
from euphorie.client import model
from euphorie.client.risk import ActionPlanView
from tno.euphorie.interfaces import ITnoActionPlanPhaseSkinLayer

grok.templatedir('templates')


class TnoActionPlanView(ActionPlanView):
    grok.context(model.Risk)
    grok.layer(ITnoActionPlanPhaseSkinLayer)
    grok.name('index_html')
    grok.template('risk_actionplan')
    grok.require('euphorie.client.ViewSurvey')

    question_filter = sql.or_(model.MODULE_WITH_RISK_TOP5_TNO_FILTER,
                              model.RISK_PRESENT_FILTER_TOP5_TNO_FILTER)
    risk_filter = model.RISK_PRESENT_FILTER_TOP5_TNO_FILTER
