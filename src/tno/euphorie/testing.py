from collective.testcaselayer import ptc
from euphorie.deployment.tests.functional import EuphorieLayer
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.PloneTestCase import PloneTestCase


class TnoEuphorieTestLayer(ptc.BasePTCLayer):
    def afterSetUp(self):
        from Testing.ZopeTestCase import installPackage
        import tno.euphorie

        self.loadZCML('configure.zcml', package=tno.euphorie)
        installPackage('tno.euphorie')
        self.addProduct('tno.euphorie')
        # Reinstalling tno.euphorie zaps the membrane_tool contens, so manually
        # reindex the client.
        self.portal.membrane_tool.indexObject(self.portal.client)

        import tno.euphorie.model
        assert tno.euphorie.model._instrumented
        from euphorie.client import model
        from z3c.saconfig import Session
        model.metadata.create_all(Session.bind, checkfirst=True)

    def beforeTearDown(self):
        pass


TnoEuphorieLayer = TnoEuphorieTestLayer([EuphorieLayer, ptc.ptc_layer])


class TnoEuphorieTestCase(PloneTestCase.PloneTestCase):
    layer = TnoEuphorieLayer


class TnoEuphorieFunctionalTestCase(EuphorieFunctionalTestCase):
    layer = TnoEuphorieLayer


def registerUserInClient(browser):
    """Register a new user in the client. This is pretty much a direct copy
    of :py:func:`euphorie.client.tests.utils.registerUserInClient`, but updated
    to use Dutch language for button labels.
    """
    browser.getLink('Registreer').click()
    browser.getControl(name='email').value = 'guest@example.com'
    browser.getControl(name='password1:utf8:ustring').value = 'guest'
    browser.getControl(name='password2:utf8:ustring').value = 'guest'
    browser.getControl(name='next', index=1).click()
