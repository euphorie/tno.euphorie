from euphorie.testing import EUPHORIE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PloneSandboxLayer

import tno.euphorie
import unittest


class TnoEuphorieTestLayer(PloneSandboxLayer):
    def setUpZope(self, app, configurationContext):
        """
        Load and install the ZCML for tno.euphorie in the Zope environment.
        """
        self.loadZCML(package=tno.euphorie)

    def setUpPloneSite(self, portal):
        """
        Apply the package's GenericSetup profile and perform any post-install
        tasks such as reindexing or metadata creation.
        """
        # Install the default profile.
        applyProfile(portal, "tno.euphorie:default")

        # Reinstalling tno.euphorie zaps the membrane_tool contens, so manually
        # reindex the client.
        portal.membrane_tool.indexObject(portal.client)

        import tno.euphorie.model

        assert tno.euphorie.model._instrumented
        from euphorie.client import model
        from z3c.saconfig import Session

        model.metadata.create_all(Session.bind, checkfirst=True)


TNO_EUPHORIE_FIXTURE = TnoEuphorieTestLayer()

TNO_EUPHORIE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(
        EUPHORIE_FIXTURE,
        TNO_EUPHORIE_FIXTURE,
    ),
    name="TnoEuphorieTestLayer:IntegrationTesting",
)


TNO_EUPHORIE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(
        EUPHORIE_FIXTURE,
        TNO_EUPHORIE_FIXTURE,
    ),
    name="TnoEuphorieTestLayer:FunctionalTesting",
)


class TnoEuphorieTestCase(unittest.TestCase):
    layer = TNO_EUPHORIE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        return super().setUp()


class TnoEuphorieFunctionalTestCase(unittest.TestCase):
    layer = TNO_EUPHORIE_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        return super().setUp()

    def loginAsPortalOwner(self):
        return login(self.app, "admin")

    def login(self, username):
        return login(self.portal, username)


def registerUserInClient(browser):
    """Register a new user in the client. This is pretty much a direct copy
    of :py:func:`euphorie.client.tests.utils.registerUserInClient`, but updated
    to use Dutch language for button labels.
    """
    browser.getLink("Registreer").click()
    browser.getControl(name="email").value = "guest@example.com"
    browser.getControl(name="password1:utf8:ustring").value = "guest"
    browser.getControl(name="password2:utf8:ustring").value = "guest"
    browser.getControl(name="next").click()
