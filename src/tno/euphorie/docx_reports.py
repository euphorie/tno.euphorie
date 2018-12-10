# coding=utf-8
from datetime import date
from euphorie.client import MessageFactory as _
from euphorie.client.docx.compiler import DocxCompiler
from euphorie.client.docx.views import ActionPlanDocxView
from pkg_resources import resource_filename
from plonetheme.nuplone.utils import formatDate
from tno.euphorie.company import DutchCompanySchema
from tno.euphorie.report import formatAddress


class RIEDocxCompiler(DocxCompiler):
    _template_filename = resource_filename(
        'tno.euphorie',
        'templates/rie.docx',
    )

    def set_session_title_row(self, data):
        ''' This fills the workspace activity run with some text
        '''
        request = self.request
        doc = self.template
        doc.paragraphs[0].text = data['heading']
        doc.add_paragraph(formatDate(request, date.today()), style="Comment")

        heading1 = self.t(_(
            "plan_report_intro_header", default=u"Introduction"))
        intro = self.t(_(
            "plan_report_intro_1",
            default=u"By filling in the list of questions, you have "
                    u"completed a risk assessment. This assessment is used to "
                    u"draw up an action plan. The progress of this action "
                    u"plan must be discussed annually and a small report must "
                    u"be written on the progress. Certain subjects might have "
                    u"been completed and perhaps new subjects need to be "
                    u"added."))

        doc.add_paragraph(heading1, style="Heading 1")
        doc.add_paragraph(intro)
        doc.add_paragraph()
        survey = request.survey
        footer_txt = self.t(
            _("report_survey_revision",
                default=u"This document was based on the OiRA Tool '${title}' "
                        u"of revision date ${date}.",
                mapping={"title": survey.published[1],
                         "date": formatDate(request, survey.published[2])}))
        doc.add_paragraph(footer_txt, 'Footer')
        doc.add_page_break()
        doc.add_paragraph(
            self.t(_(
                "plan_report_company_header", default=u"Company details")),
            style="Heading 1")
        missing = self.t(_("missing_data", default=u"Not provided"))
        company = self.session.dutch_company
        table = doc.add_table(rows=1, cols=2)
        total_width = table.columns[0].width + table.columns[1].width
        table.columns[0].width = int(total_width * 0.20)
        table.columns[1].width = int(total_width * 0.80)

        field = DutchCompanySchema["title"]
        row_cells = table.rows[0].cells
        row_cells[0].text = str(field.title)
        row_cells[1].text = company.title if company.title else missing

        row_cells = table.add_row().cells
        address = formatAddress(
            company.address_visit_address,
            company.address_visit_postal, company.address_visit_city)

        row_cells[0].text = "Bezoekadres bedrijf"
        row_cells[1].text = address if address else missing
        row_cells = table.add_row().cells

        address = formatAddress(
            company.address_postal_address,
            company.address_postal_postal, company.address_postal_city)
        row_cells[0].text = "Postadres bedrijf"
        row_cells[1].text = address if address else missing

        for key in [
            "email", "phone", "activity", "submitter_name",
            "submitter_function", "department", "location"
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
            u"%s %%" % formatDecimal(company.absentee_percentage) if
            company.absentee_percentage else missing)

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
            formatDate(request, company.submit_date) if company.submit_date
            else missing)

        field = DutchCompanySchema["employees"]
        row_cells = table.add_row().cells
        row_cells[0].text = str(field.title)
        row_cells[1].text = (
            field.vocabulary.getTerm(company.employees).title
            if company.employees else missing)

        field = DutchCompanySchema["arbo_expert"]
        row_cells = table.add_row().cells
        row_cells[0].text = str(field.title)
        row_cells[1].text = (
            company.arbo_expert if company.arbo_expert else missing)

        doc.add_page_break()

    def compile(self, data):
        '''
        '''
        self.set_session_title_row(data)
        self.set_body(
            data, show_risk_state=True, always_print_description=True
        )


class RIEActionPlanDocxView(ActionPlanDocxView):

    _compiler = RIEDocxCompiler

    def get_data(self, for_download=False):
        ''' Gets the data structure in a format suitable for `DocxCompiler`
        '''

        data = {
            'title': self.session.title,
            'heading': self.get_heading(self.session.title),
            'section_headings': ['Plan van aanpak', ],
            'nodes': [self.get_session_nodes(), ],
        }
        return data
