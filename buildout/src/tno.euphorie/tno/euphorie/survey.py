from five import grok
from euphorie.client.survey import SurveyPublishTraverser
from euphorie.client.survey import ActionPlanReportView
from euphorie.client.survey import ActionPlanReportDownload
from tno.euphorie.interfaces import ITnoIdentificationPhaseSkinLayer
from tno.euphorie.interfaces import ITnoEvaluationPhaseSkinLayer
from tno.euphorie.interfaces import ITnoActionPlanPhaseSkinLayer
from tno.euphorie.interfaces import ITnoReportPhaseSkinLayer
from tno.euphorie.model import DutchCompany

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

    def update(self):
        super(TnoActionPlanReportView, self).update()
        if self.session.dutch_company is None:
            self.session.dutch_company=DutchCompany()


class TnoActionPlanReportDownload(ActionPlanReportDownload):
    grok.layer(ITnoReportPhaseSkinLayer)
    grok.name("download")
    grok.template("report_actionplan")

    def update(self):
        super(TnoActionPlanReportDownload, self).update()
        if self.session.dutch_company is None:
            self.session.dutch_company=DutchCompany()

