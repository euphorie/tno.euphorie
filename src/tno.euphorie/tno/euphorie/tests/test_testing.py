from tno.euphorie.testing import TnoEuphorieTestCase


class TestingTests(TnoEuphorieTestCase):
    def testTnoEuphorieInstalled(self):
        quickinstaller=self.portal.portal_quickinstaller
        self.assertEqual(
                quickinstaller.isProductInstalled("tno.euphorie"),
                True)

    def testClientUserCataloged(self):
        self.assertNotEqual(
                self.portal.acl_users.getUserById("client"), None)


