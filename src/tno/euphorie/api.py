import decimal
from five import grok
from tno.euphorie.model import DutchCompany
from tno.euphorie.module import TnoActionPlanView as TnoModuleActionPlan
from tno.euphorie.risk import TnoActionPlanView as TnoRiskActionPlan
from tno.euphorie.company import DutchCompanySchema
from tno.euphorie.interfaces import ITnoClientAPISkinLayer
from tno.euphorie.report import TnoActionPlanReportDownload
from euphorie.client.api.module import ActionPlan as ModuleActionPlan
from euphorie.client.api.risk import ActionPlan as RiskActionPlan
from euphorie.client.api import JsonView
try:
    from euphorie.json import get_json_date
    from euphorie.json import get_json_int
    from euphorie.json import get_json_string
    from euphorie.json import get_json_token
    from euphorie.json import vocabulary_options
    from euphorie.json import vocabulary_token
except ImportError:
    from euphorie.client.api import get_json_date
    from euphorie.client.api import get_json_int
    from euphorie.client.api import get_json_string
    from euphorie.client.api import get_json_token
    from euphorie.client.api import vocabulary_options
    from euphorie.client.api import vocabulary_token
from euphorie.client.model import SurveySession


def apply_monkeys():
    RiskActionPlan.question_filter = TnoRiskActionPlan.question_filter
    ModuleActionPlan.question_filter = TnoModuleActionPlan.question_filter


def get_json_decimal(input, name, required=False, default=None):
    value = input.get(name)
    if value is None:
        if not required:
            return default
        raise KeyError('Required field %s is missing' % name)
    if not isinstance(value, (int, float)):
        raise ValueError('Field %s has wrong type' % name)
    return decimal.Decimal(str(value))  # Use str to prevent rounding issues


class Company(JsonView):
    grok.context(SurveySession)
    grok.layer(ITnoClientAPISkinLayer)
    grok.require('zope2.View')
    grok.name('company')

    def update(self):
        if self.context.dutch_company is None:
            self.context.dutch_company = DutchCompany()

    def do_GET(self):
        company = self.context.dutch_company
        return {'type': 'dutch-company',
                'title': company.title,
                'visit-address': {
                    'address': company.address_visit_address,
                    'postal': company.address_visit_postal,
                    'city': company.address_visit_city,
                },
                'postal-address': {
                    'address': company.address_postal_address,
                    'postal': company.address_postal_postal,
                    'city': company.address_postal_city,
                },
                'email': company.email,
                'phone': company.phone,
                'activity': company.activity,
                'department': company.department,
                'location': company.location,
                'employees': vocabulary_token(
                    DutchCompanySchema['employees'], company.employees)
                    if company.employees else None,
                'employees-options': vocabulary_options(
                    DutchCompanySchema['employees'], self.request),
                'absentee-percentage': float(company.absentee_percentage)
                    if company.absentee_percentage is not None else None,
                'accidents': company.accidents,
                'incapacitated-workers': company.incapacitated_workers,
                'submitter': {
                    'name': company.submitter_name,
                    'function': company.submitter_function,
                },
                'submitted': company.submit_date.isoformat()
                        if company.submit_date is not None else None,
                'arbo-expert': company.arbo_expert,
                'works-council-approval':
                    company.works_council_approval.isoformat()
                    if company.works_council_approval is not None else None,
                }

    def do_PUT(self):
        company = self.context.dutch_company
        try:
            company.title = get_json_string(self.input, 'title',
                    default=company.title, length=128)
            if 'visit-address' in self.input:
                input = self.input['visit-address']
                company.address_visit_address = get_json_string(
                        input, 'address',
                        default=company.address_visit_address)
                company.address_visit_postal = get_json_string(
                        input, 'postal',
                        default=company.address_visit_postal, length=16)
                company.address_visit_city = get_json_string(
                        input, 'city',
                        default=company.address_visit_city, length=64)
            if 'postal-address' in self.input:
                input = self.input['postal-address']
                company.address_postal_address = get_json_string(
                        input, 'address',
                        default=company.address_postal_address)
                company.address_postal_postal = get_json_string(
                        input, 'postal',
                        default=company.address_postal_postal, length=16)
                company.address_postal_city = get_json_string(
                        input, 'city',
                        default=company.address_postal_city, length=64)
            company.email = get_json_string(self.input, 'email',
                    default=company.email, length=128)
            company.phone = get_json_string(self.input, 'phone',
                    default=company.email, length=64)
            company.activity = get_json_string(self.input, 'activity',
                    default=company.activity, length=64)
            company.department = get_json_string(self.input, 'department',
                    default=company.department, length=64)
            company.location = get_json_string(self.input, 'location',
                    default=company.location, length=64)
            company.submit_date = get_json_date(self.input, 'submitted',
                    default=company.submit_date)
            company.employees = get_json_token(self.input, 'employees',
                    DutchCompanySchema['employees'], company.employees)
            company.absentee_percentage = get_json_decimal(self.input,
                    'absentee-percentage', default=company.absentee_percentage)
            company.accidents = get_json_int(self.input, 'accidents',
                    default=company.accidents)
            company.incapacitated_workers = get_json_int(self.input,
                    'incapacitated-workers',
                    default=company.incapacitated_workers)
            if 'submitter' in self.input:
                input = self.input['submitter']
                company.submitter_name = get_json_string(input,
                        'name', default=company.submitter_name, length=64)
                company.submitter_function = get_json_string(input,
                        'function', default=company.submitter_function,
                        length=64)
            company.arbo_expert = get_json_string(self.input, 'arbo-expert',
                    default=company.arbo_expert, length=128)
            company.works_council_approval = get_json_date(self.input,
                    'works-council-approval',
                    default=company.works_council_approval)
        except (KeyError, ValueError) as e:
            return {'type': 'error',
                    'message': str(e)}
        return self.do_GET()


class ActionPlanReport(grok.View):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.layer(ITnoClientAPISkinLayer)
    grok.name('report-actionplan')

    def update(self):
        if self.context.dutch_company is None:
            self.context.dutch_company = DutchCompany()

    def render(self):
        view = TnoActionPlanReportDownload(self.request.survey, self.request)
        view.session = self.context
        return view.render()


_applied_monkeys = False
if not _applied_monkeys:
    apply_monkeys()
    _applied_monkeys = True
