from euphorie.client import model
from euphorie.client.browser.module import ActionPlanView
from sqlalchemy import sql


class TnoActionPlanView(ActionPlanView):
    question_filter = sql.or_(
        model.MODULE_WITH_RISK_TOP5_TNO_FILTER,
        model.RISK_PRESENT_FILTER_TOP5_TNO_FILTER,
    )
