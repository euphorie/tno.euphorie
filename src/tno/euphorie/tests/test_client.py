from tno.euphorie.testing import TnoEuphorieFunctionalTestCase


class ClientPublishTraverserTests(TnoEuphorieFunctionalTestCase):
    def ClientPublishTraverser(self, *a, **kw):
        from tno.euphorie.client import ClientPublishTraverser
        return ClientPublishTraverser(*a, **kw)

    def test_api_access(self):
        from Products.Five.testbrowser import Browser
        browser = Browser()
        browser.open('http://nohost/plone/client/api')
        self.assertEqual(
                browser.headers['Content-Type'],
                'application/json')
