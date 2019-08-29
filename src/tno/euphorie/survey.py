# coding=utf-8
from Acquisition import aq_parent
from euphorie.client import model
from euphorie.client.browser import session
from five import grok
from plone.memoize.view import memoize
from sqlalchemy import sql

grok.templatedir('templates')


class ActionPlanView(session.ActionPlanView):

    question_filter = sql.or_(model.MODULE_WITH_RISK_TOP5_TNO_FILTER,
                              model.RISK_PRESENT_FILTER_TOP5_TNO_FILTER)
    risk_filter = model.RISK_PRESENT_FILTER_TOP5_TNO_FILTER


class Status(session.Status):

    show_high_risks = False


class Start(session.Start):

    @property
    @memoize
    def sector(self):
        return aq_parent(self.survey)

    @property
    @memoize
    def scaled_tool_image_url(self):
        if not getattr(self.sector, "logo", None):
            return ""
        scales = self.sector.restrictedTraverse('@@images')
        scale = scales.scale('logo', scale='large')
        return scale.url if scale else ""
