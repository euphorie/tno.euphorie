from tno.euphorie import testing


class CompanyBrowserTests(testing.TnoEuphorieFunctionalTestCase):
    BASE_URL = "http://nohost/plone/client/nl?language=nl-NL"

    def createSurvey(self):
        from euphorie.client.tests.utils import addSurvey
        from euphorie.content.tests.utils import BASIC_SURVEY

        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)

    def startSurveySession(self):
        from Products.Five.testbrowser import Browser

        browser = Browser()
        browser.open(self.BASE_URL)
        # Register a new user
        testing.registerUserInClient(browser)
        # Create a new survey session
        browser.getLink(id="button-new-session").click()
        browser.getControl(name="title:utf8:ustring").value = "Test session"
        browser.getControl(name="next").click()
        # Start the survey
        browser.getForm().submit()
        browser.handleErrors = False
        return browser

    def testDutchCompanyFormUsed(self):
        self.createSurvey()
        browser = self.startSurveySession()
        # Jump to the report phase
        browser.getLink("Rapport").click()
        browser.getControl(name="next").click()
        # We should now be at the company form
        self.assertEqual(
            browser.url,
            "http://nohost/plone/client/nl/ict/software-development/report/company",
        )
        self.assertTrue("Bezoekadres bedrijf" in browser.contents)

    def testDutchCompanyReportViewUsed(self):
        self.createSurvey()
        browser = self.startSurveySession()
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/view"
        )
        self.assertTrue("Bezoekadres bedrijf" in browser.contents)

    def testDutchCompanyReportDownloadUsed(self):
        self.createSurvey()
        browser = self.startSurveySession()
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/download"
        )
        self.assertTrue("Bezoekadres bedrijf" in browser.contents)

    def testDecimalAbsenteePercentage_DutchNotation(self):
        self.createSurvey()
        browser = self.startSurveySession()
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/company"
        )
        browser.getControl(name="form.widgets.absentee_percentage").value = "50,1"
        browser.getControl(name="form.buttons.next").click()
        self.assertEqual(
            browser.url,
            "http://nohost/plone/client/nl/ict/software-development/report/view",
        )

    def testDecimalAbsenteePercentage_EnglishNotation(self):
        self.createSurvey()
        browser = self.startSurveySession()
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/company"
        )
        browser.getControl(name="form.widgets.absentee_percentage").value = "40.1"
        browser.getControl(name="form.buttons.next").click()
        self.assertTrue("Vul een getal (maximaal 100) in." in browser.contents)

    def testInvalidAbsenteePercentageGetsErrorMessage(self):
        self.createSurvey()
        browser = self.startSurveySession()
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/company"
        )
        browser.getControl(name="form.widgets.absentee_percentage").value = "4.0.1"
        browser.getControl(name="form.buttons.next").click()
        self.assertTrue("Vul een getal (maximaal 100) in." in browser.contents)

    def testDecimalAbsenteePercentageNotRoundedInReport(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/162
        self.createSurvey()
        browser = self.startSurveySession()
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/company"
        )
        browser.getControl(name="form.widgets.absentee_percentage").value = "50,1"
        browser.getControl(name="form.buttons.next").click()
        self.assertTrue("50,1" in browser.contents)

    def testPartialYear(self):
        self.createSurvey()
        browser = self.startSurveySession()
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/company"
        )
        browser.getControl(name="form.widgets.submit_date-day").value = "10"
        browser.getControl(name="form.widgets.submit_date-month").value = ["9"]
        browser.getControl(name="form.widgets.submit_date-year").value = "8"
        browser.getControl(name="form.buttons.next").click()
        self.assertTrue("Geef een datum na 1 januari 2000 op." in browser.contents)
        browser.getControl(name="form.widgets.submit_date-year").value = "2008"
        browser.getControl(name="form.buttons.next").click()
        self.assertEqual(
            browser.url,
            "http://nohost/plone/client/nl/ict/software-development/report/view",
        )
        self.assertTrue("10 september 2008" in browser.contents)

    def testEmployeeSaved(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/151
        self.createSurvey()
        browser = self.startSurveySession()
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/company"
        )
        browser.getControl(name="form.widgets.employees").value = ["over25"]
        browser.getControl(name="form.buttons.next").click()
        self.assertEqual(
            browser.url,
            "http://nohost/plone/client/nl/ict/software-development/report/view",
        )
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/company"
        )
        self.assertEqual(
            browser.getControl(name="form.widgets.employees").value, ["over25"]
        )

    def testWorksCouncilApprovalNotSetAfterOtherError(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/163
        self.createSurvey()
        browser = self.startSurveySession()
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/company"
        )
        browser.getControl(name="form.widgets.absentee_percentage").value = "ABC"
        browser.getControl(name="form.buttons.next").click()
        self.assertEqual(browser.getControl(name="works_council").value, [])

    def testAbsenteePercentageNotLost(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/167
        self.createSurvey()
        browser = self.startSurveySession()
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/company"
        )
        browser.getControl(name="form.widgets.absentee_percentage").value = "50"
        browser.getControl(name="form.buttons.next").click()
        self.assertEqual(
            browser.url,
            "http://nohost/plone/client/nl/ict/software-development/report/view",
        )
        browser.open(
            "http://nohost/plone/client/nl/ict/software-development/report/company"
        )
        value = browser.getControl(name="form.widgets.absentee_percentage").value
        self.assertTrue(value.startswith("50"))
