import unittest
from tno.euphorie.testing import TnoEuphorieFunctionalTestCase


class get_json_decimal_tests(unittest.TestCase):
    def get_json_decimal(self, *a, **kw):
        from ..api import get_json_decimal
        return get_json_decimal(*a, **kw)

    def test_missing_required_field(self):
        self.assertRaises(KeyError,
                self.get_json_decimal, {}, 'field', required=True)

    def test_missing_optional_field(self):
        self.assertEqual(
                self.get_json_decimal({}, 'field', required=False,
                    default='default'),
                'default')

    def test_bad_type(self):
        self.assertRaises(ValueError,
                self.get_json_decimal, {'field': 'dummy'}, 'field')

    def test_proper_value(self):
        import decimal
        self.assertEqual(
                self.get_json_decimal({'field': 15}, 'field'),
                decimal.Decimal('15'))

    def test_rounding(self):
        import decimal
        self.assertEqual(
                self.get_json_decimal({'field': 25.6}, 'field'),
                decimal.Decimal('25.6'))


class ViewBrowserTests(TnoEuphorieFunctionalTestCase):
    def test_company_no_date_present(self):
        import datetime
        import json
        from z3c.saconfig import Session
        from euphorie.client.model import SurveySession
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.api.authentication import generate_token
        from Products.Five.testbrowser import Browser
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password='secret')
        survey_session = SurveySession(
                title=u'Dummy session',
                created=datetime.datetime(2012, 4, 22, 23, 5, 12),
                modified=datetime.datetime(2012, 4, 23, 11, 50, 30),
                zodb_path='nl/ict/software-development',
                account=account)
        Session.add(survey_session)
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.open(
                'http://nohost/plone/client/api/users/1/sessions/1/company')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'dutch-company')


class CompanyTests(TnoEuphorieFunctionalTestCase):
    def Company(self, *a, **kw):
        from tno.euphorie.api import Company
        return Company(*a, **kw)

    def create_context(self):
        import datetime
        from euphorie.client.model import SurveySession
        from tno.euphorie.model import DutchCompany
        company = DutchCompany(title=u'Acme B.V.',
                employees='40h',
                email='john@example.com',
                submit_date=datetime.date(2012, 6, 6))
        return SurveySession(dutch_company=company)

    def test_do_GET_result(self):
        import json
        from zope.publisher.browser import TestRequest
        context = self.create_context()
        view = self.Company(context, TestRequest())
        response = view.do_GET()
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(
                set(response),
                set(['type', 'title', 'visit-address', 'postal-address',
                     'email', 'phone', 'activity', 'submitter', 'department',
                     'location', 'submitted', 'employees', 'employees-options',
                     'absentee-percentage', 'accidents',
                     'incapacitated-workers', 'arbo-expert',
                     'works-council-approval']))
        json.dumps(response)  # Check it is serializable
        self.assertEqual(response['type'], 'dutch-company')
        self.assertEqual(response['title'], u'Acme B.V.')
        self.assertEqual(response['absentee-percentage'], None)
        self.assertEqual(response['employees'], '40h')
        self.assertEqual(response['submitted'], '2012-06-06')

    def test_do_GET_with_absentee_percentage(self):
        import decimal
        import json
        from zope.publisher.browser import TestRequest
        context = self.create_context()
        context.dutch_company.absentee_percentage = decimal.Decimal('12.34')
        view = self.Company(context, TestRequest())
        response = view.do_GET()
        json.dumps(response)  # Check it is serializable
        self.assertEqual(response['absentee-percentage'], 12.34)

    def test_do_PUT(self):
        import datetime
        import decimal
        from zope.publisher.browser import TestRequest
        context = self.create_context()
        view = self.Company(context, TestRequest())
        view.input = {'visit-address': {
                          'address': u'Dorpsstraat 15',
                          'city': u'Ons Dorp'},
                      'department': u'Incasso',
                      'accidents': 15,
                      'absentee-percentage': 25.6,
                      'employees': 'over25',
                      'works-council-approval': '2012-06-04',
                     }
        response = view.do_PUT()
        self.assertEqual(response['type'], 'dutch-company')
        self.assertEqual(
                context.dutch_company.address_visit_address,
                u'Dorpsstraat 15')
        self.assertEqual(
                context.dutch_company.address_visit_city,
                u'Ons Dorp')
        self.assertEqual(context.dutch_company.department, u'Incasso')
        self.assertEqual(context.dutch_company.accidents, 15)
        self.assertEqual(
                context.dutch_company.absentee_percentage,
                decimal.Decimal('25.6'))
        self.assertEqual(context.dutch_company.employees, 'over25')
        self.assertEqual(
                context.dutch_company.works_council_approval,
                datetime.date(2012, 6, 4))


class ActionPlanReportTests(TnoEuphorieFunctionalTestCase):
    def test_browser_get(self):
        import datetime
        from z3c.saconfig import Session
        from euphorie.client.model import SurveySession
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addAccount
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.api.authentication import generate_token
        from tno.euphorie.model import DutchCompany
        from Products.Five.testbrowser import Browser
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password='secret')
        survey_session = SurveySession(
                title=u'Dummy session',
                created=datetime.datetime(2012, 4, 22, 23, 5, 12),
                modified=datetime.datetime(2012, 4, 23, 11, 50, 30),
                zodb_path='nl/ict/software-development',
                account=account)
        survey_session.dutch_company = DutchCompany(
                title=u'Acme B.V.',
                employees='40h',
                email='john@example.com',
                submit_date=datetime.date(2012, 6, 6))
        Session.add(survey_session)
        browser = Browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.handleErrors = False
        browser.open(
                'http://nohost/plone/client/api/users/1/sessions/1/'
                'report-actionplan')
        self.assertEqual(browser.headers['Content-Type'], 'application/rtf')
        self.assertTrue('Bedrijfsnaam' in browser.contents)
