from rtfng.document.paragraph import Paragraph
from rtfng.document.paragraph import Cell
from rtfng.document.paragraph import Table
from rtfng.PropertySets import TabPropertySet
from sqlalchemy import sql
from z3c.saconfig import Session
from five import grok
from zope.i18n import translate
from plonetheme.nuplone.utils import formatDate
from euphorie.client import model
from euphorie.client.report import ActionPlanReportView
from euphorie.client.report import ActionPlanReportDownload
from euphorie.client.report import createSection
from euphorie.client import MessageFactory as eu_
from tno.euphorie.interfaces import ITnoReportPhaseSkinLayer
from tno.euphorie.model import DutchCompany
from tno.euphorie.company import DutchCompanySchema

grok.templatedir("templates")

def formatAddress(address, postal, city):
    output=[]
    if address:
        output.append(address)
        if postal or city:
            output.append(u"\n")
    bits=filter(None, [postal, city])
    if bits:
        output.append(u" ".join(bits))
    return u"".join(output) if output else None



class TnoActionPlanReportView(ActionPlanReportView):
    grok.layer(ITnoReportPhaseSkinLayer)
    grok.name("view")
    grok.template("report_actionplan")

    def getNodes(self):
        query = Session.query(model.SurveyTreeItem)\
                .filter(model.SurveyTreeItem.session == self.session)\
                .filter(sql.not_(model.SKIPPED_PARENTS))\
                .filter(sql.or_(model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                                model.RISK_PRESENT_OR_TOP5_FILTER))\
                .order_by(model.SurveyTreeItem.path)
        return  query.all()

    def update(self):
        super(TnoActionPlanReportView, self).update()
        if self.session.dutch_company is None:
            self.session.dutch_company=DutchCompany()



class TnoActionPlanReportDownload(ActionPlanReportDownload):
    grok.layer(ITnoReportPhaseSkinLayer)
    grok.name("download")

    def getNodes(self):
        query = Session.query(model.SurveyTreeItem)\
                .filter(model.SurveyTreeItem.session == self.session)\
                .filter(sql.not_(model.SKIPPED_PARENTS))\
                .filter(sql.or_(model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                                model.RISK_PRESENT_OR_TOP5_FILTER))\
                .order_by(model.SurveyTreeItem.path)
        return  query.all()

    def update(self):
        super(TnoActionPlanReportDownload, self).update()
        if self.session.dutch_company is None:
            self.session.dutch_company=DutchCompany()

    def addCompanyInformation(self, document):
        request=self.request
        company=self.session.dutch_company
        t=lambda txt: translate(txt, context=request)
        section = createSection(document, self.context, self.session,
                self.request)
        normal_style=document.StyleSheet.ParagraphStyles.Normal
        missing=t(eu_("missing_data", default=u"Not provided"))

        section.append(Paragraph(
            document.StyleSheet.ParagraphStyles.Heading1,
            t(eu_("plan_report_company_header", default=u"Company details"))))

        table=Table(TabPropertySet.DEFAULT_WIDTH*3, TabPropertySet.DEFAULT_WIDTH*8)

        field=DutchCompanySchema["title"]
        table.append(
                Cell(Paragraph(normal_style, str(field.title))),
                Cell(Paragraph(normal_style, company.title if company.title else missing)))

        address=formatAddress(company.address_visit_address,
                company.address_visit_postal, company.address_visit_city)
        table.append(
                Cell(Paragraph(normal_style, "Bezoekadres bedrijf")),
                Cell(Paragraph(normal_style, address if address else missing)))

        address=formatAddress(company.address_postal_address,
                company.address_postal_postal, company.address_postal_city)
        table.append(
                Cell(Paragraph(normal_style, "Postadres bedrijf")),
                Cell(Paragraph(normal_style, address if address else missing)))

        for key in ["email", "phone", "activity", "submitter_name",
                      "submitter_function", "department", "location"]:
            field=DutchCompanySchema[key]
            value=getattr(company, key, None)
            table.append(
                    Cell(Paragraph(normal_style, field.title)),
                    Cell(Paragraph(normal_style, value if value else missing))),

        formatDecimal=request.locale.numbers.getFormatter("decimal").format
        field=DutchCompanySchema["absentee_percentage"]
        table.append(
                Cell(Paragraph(normal_style, field.title)),
                Cell(Paragraph(normal_style, u"%s %%" % formatDecimal(company.absentee_percentage) if company.absentee_percentage else missing)))

        for key in [ "accidents", "incapacitated_workers"]:
            field=DutchCompanySchema[key]
            value=getattr(company, key, None)
            table.append(
                    Cell(Paragraph(normal_style, field.title)),
                    Cell(Paragraph(normal_style, "%d" % value if value is not None else missing)))

        field=DutchCompanySchema["submit_date"]
        table.append(
                Cell(Paragraph(normal_style, field.title)),
                Cell(Paragraph(normal_style, formatDate(request, company.submit_date) if company.submit_date else missing)))

        field=DutchCompanySchema["employees"]
        table.append(
                Cell(Paragraph(normal_style, field.title)),
                Cell(Paragraph(normal_style, field.vocabulary.getTerm(company.employees).title if company.employees else missing)))

        field=DutchCompanySchema["arbo_expert"]
        table.append(
                Cell(Paragraph(normal_style, str(field.title))),
                Cell(Paragraph(normal_style, company.arbo_expert if company.arbo_expert else missing)))

        section.append(table)
