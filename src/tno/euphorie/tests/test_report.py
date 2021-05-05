import unittest


class FormatAddressTests(unittest.TestCase):
    def formatAddress(self, *a, **kw):
        from tno.euphorie.report import formatAddress

        return formatAddress(*a, **kw)

    def testEmptyAddress(self):
        self.assertEqual(self.formatAddress(None, None, None), None)

    def testAddressOnly(self):
        self.assertEqual(self.formatAddress(u"Street", None, None), u"Street")

    def testPostalOnly(self):
        self.assertEqual(self.formatAddress(None, u"Postal", None), u"Postal")

    def testPostalAndCity(self):
        self.assertEqual(self.formatAddress(None, u"Postal", u"City"), u"Postal City")

    def testFull(self):
        self.assertEqual(
            self.formatAddress(u"Street", u"Postal", u"City"), u"Street\nPostal City"
        )
