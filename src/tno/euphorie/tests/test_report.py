import unittest


class FormatAddressTests(unittest.TestCase):
    def formatAddress(self, *a, **kw):
        from tno.euphorie.client.browser.report import formatAddress

        return formatAddress(*a, **kw)

    def testEmptyAddress(self):
        self.assertEqual(self.formatAddress(None, None, None), None)

    def testAddressOnly(self):
        self.assertEqual(self.formatAddress("Street", None, None), "Street")

    def testPostalOnly(self):
        self.assertEqual(self.formatAddress(None, "Postal", None), "Postal")

    def testPostalAndCity(self):
        self.assertEqual(self.formatAddress(None, "Postal", "City"), "Postal City")

    def testFull(self):
        self.assertEqual(
            self.formatAddress("Street", "Postal", "City"), "Street\nPostal City"
        )
