from tno.euphorie import testing

import unittest


class SessionBrowserTests(testing.TnoEuphorieFunctionalTestCase):
    def createSurvey(self):
        from euphorie.client.tests.utils import addSurvey
        from euphorie.content.tests.utils import BASIC_SURVEY

        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)

    def createClientBrowser(self):
        from euphorie.client.tests.utils import registerUserInClient
        from plone.testing.zope import Browser

        browser = Browser(self.app)
        browser.open(
            self.portal.client.nl["ict"]["software-development"].absolute_url()
        )
        registerUserInClient(browser)
        return browser

    @unittest.skip("This test is skipped For the moment.")
    def testUploadFormIsMentionedOnSessionScreen(self):
        self.createSurvey()
        browser = self.createClientBrowser()
        browser.open(self.portal.client.nl.absolute_url())
        self.assertTrue(
            "Als u bestanden van de oude RI&amp;E omgeving van vóór 2010 heeft kunt U deze via"  # noqa: E501
            in browser.contents
        )
        browser.getLink("dit formulier").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/rie-session")
