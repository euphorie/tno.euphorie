from sqlalchemy import sql
from five import grok
from euphorie.client import model
from euphorie.client.module import ActionPlanView
from tno.euphorie.interfaces import ITnoActionPlanPhaseSkinLayer

grok.templatedir('templates')


class TnoActionPlanView(ActionPlanView):
    grok.context(model.Module)
    grok.require('euphorie.client.ViewSurvey')
    grok.layer(ITnoActionPlanPhaseSkinLayer)
    grok.name('index_html')

    question_filter = sql.and_(
            model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER,
            sql.or_(model.MODULE_WITH_RISK_FILTER,
                    model.RISK_PRESENT_FILTER))
