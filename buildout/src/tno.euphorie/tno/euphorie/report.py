from five import grok
from euphorie.client.report import ActionPlanReportView
from euphorie.client.report import ActionPlanReportDownload
from tno.euphorie.interfaces import ITnoReportPhaseSkinLayer
from tno.euphorie.model import DutchCompany

grok.templatedir("templates")

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

    def update(self):
        super(TnoActionPlanReportDownload, self).update()
        if self.session.dutch_company is None:
            self.session.dutch_company=DutchCompany()

    def addCompanyInformation(self, document):
        pass

