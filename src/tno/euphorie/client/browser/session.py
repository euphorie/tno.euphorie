# coding=utf-8
from Acquisition import aq_parent
from collections import defaultdict
from datetime import date
from euphorie import MessageFactory as _
from euphorie.client import model
from euphorie.client.browser import session
from euphorie.content.interfaces import ICustomRisksModule
from euphorie.content.profilequestion import IProfileQuestion
from plone.memoize.view import memoize
from sqlalchemy import sql
from z3c.saconfig import Session
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory


PloneLocalesFactory = MessageFactory("plonelocales")


class ActionPlanView(session.ActionPlanView):

    question_filter = sql.or_(
        model.MODULE_WITH_RISK_TOP5_TNO_FILTER,
        model.RISK_PRESENT_FILTER_TOP5_TNO_FILTER,
    )
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
        scales = self.sector.restrictedTraverse("@@images")
        scale = scales.scale("logo", scale="large")
        return scale.url if scale else ""


class MeasuresOverview(session.MeasuresOverview):
    """Implements the "Overview of Measures" report, see #10967"""

    def update(self):
        super(MeasuresOverview, self).update()
        lang = getattr(self.request, "LANGUAGE", "en")
        if "-" in lang:
            lang = lang.split("-")[0]
        if self.session is not None and self.session.title != (
            callable(getattr(self.context, "Title", None))
            and self.context.Title()
            or ""
        ):
            self.session_title = self.session.title
        else:
            self.session_title = (
                callable(getattr(self.context, "Title", None))
                and self.context.Title()
                or ""
            )
        today = date.today()
        this_month = date(today.year, today.month, 1)
        self.label_page = translate(
            _(u"label_page", default=u"Page"), target_language=lang
        )
        self.label_page_of = translate(
            _(u"label_page_of", default=u"of"), target_language=lang
        )

        def get_next_month(this_month):
            month = this_month.month + 1
            year = this_month.year
            if month == 13:
                month = 1
                year = year + 1
            return date(year, month, 1)

        next_month = get_next_month(this_month)
        month_after_next = get_next_month(next_month)
        self.months = []
        self.months.append(today.strftime("%b"))
        self.months.append(next_month.strftime("%b"))
        self.months.append(month_after_next.strftime("%b"))
        self.monthstrings = [
            translate(
                PloneLocalesFactory(
                    "month_{0}_abbr".format(month.lower()),
                    default=month,
                ),
                target_language=lang,
            )
            for month in self.months
        ]

        query = (
            Session.query(model.Module, model.Risk, model.ActionPlan)
            .select_from(model.Module)
            .filter(
                sql.and_(
                    model.Module.session == self.session,
                    model.Module.profile_index > -1,
                )
            )
            .filter(sql.not_(model.SKIPPED_PARENTS))
            .filter(
                sql.or_(
                    model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                    model.RISK_PRESENT_OR_TOP5_FILTER,
                )
            )
            .join(model.Risk, model.Risk.parent_id == model.Module.id)
            .join(model.ActionPlan, model.ActionPlan.risk_id == model.Risk.id)
            .order_by(
                sql.case(
                    value=model.Risk.priority, whens={"high": 0, "medium": 1}, else_=2
                ),
                model.Risk.path,
            )
        )
        measures = [
            t
            for t in query.all()
            if (
                (
                    (
                        t[-1].planning_start is not None
                        and t[-1].planning_start.strftime("%b") in self.months
                    )
                    or (
                        t[-1].planning_end is not None
                        and t[-1].planning_end.strftime("%b") in self.months
                    )
                    or (
                        t[-1].planning_start is not None
                        and (
                            t[-1].planning_end is None
                            or t[-1].planning_end >= month_after_next
                        )
                        and t[-1].planning_start <= this_month
                    )
                )
                and t[1].identification not in ("n/a", "yes")
                and (
                    t[-1].responsible is not None
                    or t[-1].requirements is not None
                    or t[-1].budget is not None
                    or t[-1].action is not None
                )
            )
        ]

        modulesdict = defaultdict(lambda: defaultdict(list))
        for module, risk, action in measures:
            if "custom-risks" not in risk.zodb_path:
                risk_obj = self.survey.restrictedTraverse(risk.zodb_path.split("/"))
                title = risk_obj and risk_obj.problem_description or risk.title
            else:
                title = risk.title
            classes = []
            start_month = action.planning_start and date(
                action.planning_start.year, action.planning_start.month, 1
            )
            end_month = action.planning_end and date(
                action.planning_end.year, action.planning_end.month, 1
            )
            for m in [this_month, next_month, month_after_next]:
                cls = None
                if start_month:
                    if start_month == m:
                        cls = "start"
                    if end_month:
                        if end_month == m:
                            if end_month == (start_month is not None and start_month):
                                cls = "start-end"
                            else:
                                cls = "end"
                        elif start_month < m and end_month > m:
                            cls = "ongoing"
                    elif start_month < m:
                        cls = "ongoing"
                elif end_month:
                    if end_month == m:
                        cls = "end"
                    elif end_month > m:
                        cls = "ongoing"
                classes.append(cls)
            modulesdict[module][risk.priority].append(
                {
                    "title": title,
                    "description": action.action,
                    "months": [
                        (
                            action.planning_start
                            and action.planning_start.month == m.month
                        )
                        or (
                            action.planning_end and action.planning_end.month == m.month
                        )
                        for m in [today, next_month, month_after_next]
                    ],
                    "classes": classes,
                }
            )

        main_modules = {}
        for module, risks in sorted(modulesdict.items(), key=lambda m: m[0].zodb_path):
            module_obj = self.survey.restrictedTraverse(module.zodb_path.split("/"))
            if (
                IProfileQuestion.providedBy(module_obj)
                or ICustomRisksModule.providedBy(module_obj)
                or module.depth >= 3
            ):
                path = module.path[:6]
            else:
                path = module.path[:3]
            if path in main_modules:
                for prio in risks.keys():
                    if prio in main_modules[path]["risks"]:
                        main_modules[path]["risks"][prio].extend(risks[prio])
                    else:
                        main_modules[path]["risks"][prio] = risks[prio]
            else:
                title = module.title
                number = module.number
                main_modules[path] = {"name": title, "number": number, "risks": risks}

        self.modules = []
        for key in sorted(main_modules.keys()):
            self.modules.append(main_modules[key])
