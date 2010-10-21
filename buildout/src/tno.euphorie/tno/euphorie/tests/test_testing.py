from tno.euphorie.testing import TnoEuphorieTestCase


class TestingTests(TnoEuphorieTestCase):
    def testTnoEuphorieInstalled(self):
        quickinstaller=self.portal.portal_quickinstaller
        self.assertEqual(
                quickinstaller.isProductInstalled("tno.euphorie"),
                True)

