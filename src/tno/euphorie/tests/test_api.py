from tno.euphorie.testing import TnoEuphorieFunctionalTestCase


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
        self.assertEqual(response['type'], 'dutch-company')
        self.assertEqual(response['title'], u'Acme B.V.')
        self.assertEqual(response['employees'], '40h')
        self.assertEqual(response['submitted'], '2012-06-06')

    def do_PUT(self):
        import datetime
        from zope.publisher.browser import TestRequest
        context = self.create_context()
        view = self.Company(context, TestRequest())
        view.input = {'visit-address': {
                          'address': u'Dorpsstraat 15',
                          'city': u'Ons Dorp'},
                      'department': u'Incasso',
                      'accidents': 15,
                      'employees': 'over25',
                      'works-council-approval': '2012-06-04',
                     }
        view.do_PUT()
        self.assertEqual(
                context.dutch_company.address_visit_address,
                u'Dorpsstraat 15')
        self.assertEqual(
                context.dutch_company.address_visis_city,
                u'Ons Dorp')
        self.assertEqual(context.dutch_company.department, u'Incasso')
        self.assertEqual(context.dutch_company.accidents, 15)
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
