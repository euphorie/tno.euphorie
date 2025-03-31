from plone.base.utils import get_installer
from tno.euphorie.testing import TnoEuphorieTestCase


class TestingTests(TnoEuphorieTestCase):
    def testTnoEuphorieInstalled(self):
        quickinstaller = get_installer(self.portal, self.request)
        self.assertEqual(quickinstaller.is_product_installed("tno.euphorie"), True)

    def testClientUserCataloged(self):
        self.assertNotEqual(self.portal.acl_users.getUserById("client"), None)
