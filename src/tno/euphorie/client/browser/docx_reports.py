# coding=utf-8
from Acquisition import aq_parent
from datetime import date
from euphorie.client import MessageFactory as _
from euphorie.client.docx.compiler import delete_paragraph
from euphorie.client.docx.compiler import DocxCompiler
from euphorie.client.docx.views import ActionPlanDocxView
from euphorie.client.docx.views import IdentificationReportDocxView
from pkg_resources import resource_filename
from plonetheme.nuplone.utils import formatDate
from tno.euphorie.client.browser.company import DutchCompanySchema
from tno.euphorie.client.browser.report import formatAddress


class RIEDocxCompiler(DocxCompiler):
    _template_filename = resource_filename(
        "tno.euphorie.client.browser",
        "templates/rie.docx",
    )

    def set_session_title_row(self, data):
        """This fills the workspace activity run with some text"""
        request = self.request
        doc = self.template
        header = doc.sections[0].header
        h_table = header.tables[0]

        h_table.cell(0, 0).paragraphs[0].text = data["heading"]
        h_table.cell(0, 1).paragraphs[0].text = u"Datum download: {}".format(
            formatDate(request, date.today())
        )

        doc.paragraphs[0].text = data["heading"]

        heading1 = self.t(_("plan_report_intro_header", default=u"Introduction"))
        intro = self.t(
            _(
                "plan_report_intro_1",
                default=u"By filling in the list of questions, you have "
                u"completed a risk assessment. This assessment is used to "
                u"draw up an action plan. The progress of this action "
                u"plan must be discussed annually and a small report must "
                u"be written on the progress. Certain subjects might have "
                u"been completed and perhaps new subjects need to be "
                u"added.",
            )
        )

        doc.add_paragraph(heading1, style="Heading 1")
        doc.add_paragraph(intro)

        survey = aq_parent(self.context)
        footer_txt = self.t(
            _(
                "report_survey_revision",
                default=u"This document was based on the OiRA Tool '${title}' "
                u"of revision date ${date}.",
                mapping={
                    "title": survey.published[1],
                    "date": formatDate(request, survey.published[2]),
                },
            )
        )
        footer = doc.sections[0].footer
        f_table = footer.tables[0]
        paragraph = f_table.cell(0, 0).paragraphs[0]

        # Example code for inserting image (into a newly created table)
        # width = header_table.cell(0, 0).width + header_table.cell(0, 1).width
        # table = footer.add_table(rows=1, cols=2, width=width)
        # wh = self.context.restrictedTraverse('webhelpers')
        # image = wh.get_sector_logo
        # img = image.data._blob.open()
        # from docx.shared import Cm
        # paragraph = table.cell(0, 1).paragraphs[0]
        # paragraph.add_run().add_picture(img, width=Cm(1))
        # paragraph = table.cell(0, 0).paragraphs[0]

        paragraph.style = "Footer"
        paragraph.text = footer_txt

        doc.add_page_break()
        doc.add_paragraph(
            self.t(_("plan_report_company_header", default=u"Company details")),
            style="Heading 1",
        )
        missing = self.t(_("missing_data", default=u"Not provided"))
        company = self.session.dutch_company
        table = doc.add_table(rows=1, cols=2)
        total_width = table.columns[0].width + table.columns[1].width
        table.columns[0].width = int(total_width * 0.20)
        table.columns[1].width = int(total_width * 0.80)

        field = DutchCompanySchema["title"]
        row_cells = table.rows[0].cells
        row_cells[0].text = str(field.title)
        row_cells[1].text = company.title if company and company.title else missing

        row_cells = table.add_row().cells
        address = (
            formatAddress(
                company.address_visit_address,
                company.address_visit_postal,
                company.address_visit_city,
            )
            if company
            else None
        )

        row_cells[0].text = "Bezoekadres bedrijf"
        row_cells[1].text = address if address else missing
        row_cells = table.add_row().cells

        address = (
            formatAddress(
                company.address_postal_address,
                company.address_postal_postal,
                company.address_postal_city,
            )
            if company
            else None
        )
        row_cells[0].text = "Postadres bedrijf"
        row_cells[1].text = address if address else missing

        for key in [
            "email",
            "phone",
            "activity",
            "submitter_name",
            "submitter_function",
            "department",
            "location",
        ]:
            field = DutchCompanySchema[key]
            value = getattr(company, key, None)
            row_cells = table.add_row().cells
            row_cells[0].text = str(field.title)
            row_cells[1].text = value if value else missing

        formatDecimal = request.locale.numbers.getFormatter("decimal").format
        field = DutchCompanySchema["absentee_percentage"]
        row_cells = table.add_row().cells
        row_cells[0].text = str(field.title)
        row_cells[1].text = (
            u"%s %%" % formatDecimal(company.absentee_percentage)
            if company and company.absentee_percentage
            else missing
        )

        for key in ["accidents", "incapacitated_workers"]:
            field = DutchCompanySchema[key]
            value = getattr(company, key, None)
            row_cells = table.add_row().cells
            row_cells[0].text = str(field.title)
            row_cells[1].text = "%d" % value if value else missing

        field = DutchCompanySchema["submit_date"]
        row_cells = table.add_row().cells
        row_cells[0].text = str(field.title)
        row_cells[1].text = (
            formatDate(request, company.submit_date)
            if company and company.submit_date
            else missing
        )

        field = DutchCompanySchema["employees"]
        row_cells = table.add_row().cells
        row_cells[0].text = str(field.title)
        row_cells[1].text = (
            field.vocabulary.getTerm(company.employees).title
            if company and company.employees
            else missing
        )

        field = DutchCompanySchema["arbo_expert"]
        row_cells = table.add_row().cells
        row_cells[0].text = str(field.title)
        row_cells[1].text = (
            company.arbo_expert if company and company.arbo_expert else missing
        )

        doc.add_page_break()

    def compile(self, data):
        """"""
        self.set_session_title_row(data)
        self.set_body(data, show_risk_state=True, always_print_description=True)


class RIEActionPlanDocxView(ActionPlanDocxView):

    _compiler = RIEDocxCompiler

    def get_data(self, for_download=False):
        """Gets the data structure in a format suitable for `DocxCompiler`"""
        session = self.context.session

        data = {
            "title": session.title,
            "heading": self.get_heading(session.title),
            "section_headings": [
                "Plan van aanpak",
            ],
            "nodes": [
                self.get_session_nodes(),
            ],
        }
        return data


class RIEIdentificationReportCompiler(RIEDocxCompiler):
    def set_session_title_row(self, data):

        request = self.request
        doc = self.template

        # Remove existing paragraphs
        for paragraph in doc.paragraphs:
            delete_paragraph(paragraph)

        header = doc.sections[0].header
        h_table = header.tables[0]
        h_table.cell(0, 0).paragraphs[0].text = data["heading"]
        h_table.cell(0, 1).paragraphs[0].text = u"Datum download: {}".format(
            formatDate(request, date.today())
        )

        # doc.paragraphs[0].text = data['heading']

        survey = aq_parent(self.context)
        footer_txt = self.t(
            _(
                "report_survey_revision",
                default=u"This document was based on the OiRA Tool '${title}' "
                u"of revision date ${date}.",
                mapping={
                    "title": survey.published[1],
                    "date": formatDate(request, survey.published[2]),
                },
            )
        )
        footer = doc.sections[0].footer
        f_table = footer.tables[0]
        paragraph = f_table.cell(0, 0).paragraphs[0]
        paragraph.style = "Footer"
        paragraph.text = footer_txt

    def compile(self, data):
        """"""
        self.set_session_title_row(data)
        self.set_body(
            data,
            show_priority=False,
            show_risk_state=True,
            always_print_description=True,
            skip_legal_references=False,
            skip_existing_measures=True,
            skip_planned_measures=True,
        )


class RIEIdentificationReportDocxView(IdentificationReportDocxView):

    _compiler = RIEIdentificationReportCompiler

    def get_data(self, for_download=False):
        """Gets the data structure in a format suitable for `DocxCompiler`"""
        session = self.context.session

        data = {
            "title": session.title,
            "heading": session.title,
            "section_headings": [session.title],
            "nodes": [self.get_session_nodes()],
        }
        return data
