from tno.euphorie import testing

NORMAL_SURVEY =  \
        """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>ICT</title>
             <survey>
              <title>Software development</title>
              <module optional="no">
                <title>Module one</title>
                <description>Hello</description>
                 <risk type="risk">
                   <title>New hires are not aware of design patterns.</title>
                   <description>&lt;p&gt;Every developer should know about them..&lt;/p&gt;</description>
                   <evaluation-method>direct</evaluation-method>
                   <image caption="Key image" content-type="image/gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>
                 </risk>
              </module>
            </survey>
          </sector>"""

TOP5_SURVEY =  \
        """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
             <title>ICT</title>
             <survey>
              <title>Software development</title>
              <module optional="no">
                <title>Module one</title>
                <description>Hello</description>
                 <risk type="top5">
                   <title>New hires are not aware of design patterns.</title>
                   <description>&lt;p&gt;Every developer should know about them..&lt;/p&gt;</description>
                   <evaluation-method>direct</evaluation-method>
                   <image caption="Key image" content-type="image/gif">R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7</image>
                 </risk>
              </module>
            </survey>
          </sector>"""


class ActionPlanBrowserTests(testing.TnoEuphorieFunctionalTestCase):
    BASE_URL = "http://nohost/plone/client/nl?language=nl-NL"

    def createSurvey(self, survey):
        from euphorie.client.tests.utils import addSurvey
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)

    def startSurveySession(self):
        from Products.Five.testbrowser import Browser
        browser=Browser()
        browser.open(self.BASE_URL)
        # Register a new user
        testing.registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value="Test session"
        browser.getControl(name="next", index=1).click()
        # Start the survey
        browser.getForm().submit()
        browser.handleErrors=False
        return browser

    def test_skip_top5_risk_if_not_present(self):
        # This is a deviation from standard Euphorie which always asks for
        # policy and top5 risks.
        self.createSurvey(TOP5_SURVEY)
        browser = self.startSurveySession()
        # Jump to the risk and note that it is not present
        browser.getLink('Start risico inventarisatie').click()
        url = browser.url
        browser.getControl(name='next', index=1).click()
        browser.getControl(name='answer').value = ['yes']
        browser.getControl('next').click()
        # Now go to action plan view of the module make sure its next step is
        # the report landing page.
        url = url.replace('identification', 'actionplan')
        browser.open(url)
        self.assertEqual(
                browser.getLink('Volgende').url,
                'http://nohost/plone/client/nl/ict/software-development/report')

