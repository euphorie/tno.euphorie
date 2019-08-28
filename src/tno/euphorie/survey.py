# coding=utf-8
from euphorie.client import model
from euphorie.client.browser import session
from five import grok
from sqlalchemy import sql

grok.templatedir('templates')


class ActionPlanView(session.ActionPlanView):

    question_filter = sql.or_(model.MODULE_WITH_RISK_TOP5_TNO_FILTER,
                              model.RISK_PRESENT_FILTER_TOP5_TNO_FILTER)
    risk_filter = model.RISK_PRESENT_FILTER_TOP5_TNO_FILTER


class Status(session.Status):

    show_high_risks = False
