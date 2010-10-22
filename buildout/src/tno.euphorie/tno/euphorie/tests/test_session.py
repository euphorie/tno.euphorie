import unittest
from lxml import objectify
from tno.euphorie.testing import TnoEuphorieTestCase


class parse_dateTests(unittest.TestCase):
    def parse_date(self, value, default=None):
        from tno.euphorie.session import parse_date
        return parse_date(value, default)

    def testMissingValue(self):
        self.assertEqual(self.parse_date(""), None)
        marker=[]
        self.assertTrue(self.parse_date("", marker) is marker)

    def testInvalidValue(self):
        self.assertEqual(self.parse_date("invalid"), None)

    def testDutchDateOrder(self):
        import datetime
        self.assertEqual(self.parse_date("06/08/2010"),
                datetime.date(2010, 8, 6))



class attr_dateTests(unittest.TestCase):
    def attr_date(self, node, tag, default=None):
        from tno.euphorie.session import attr_date
        return attr_date(node, tag, default)

    def testMissingValue(self):
        from lxml import etree
        node=etree.Element("node")
        self.assertEqual(self.attr_date(node, "date"), None)
        marker=[]
        self.assertTrue(self.attr_date(node, "date", marker) is marker)

    def testEmptyValue(self):
        from lxml import etree
        node=etree.Element("node", date=u"")
        self.assertEqual(self.attr_date(node, "date"), None)


    
class UploadTests(TnoEuphorieTestCase):
    BASE_SNIPPET = """
            <rieprogress>
              <gegevens
                bezoekwoonplaats=""
                datum=""
                afdeling=""
                postcode=""
                organisatie=""
                deeltijdindienst=""
                arbodienstcontactpersoon=""
                bezoekadres=""
                emailadres=""
                bedrijfsactiviteit=""
                faxnummer=""
                invullerfunctie=""
                orakkoord=""
                telefoonnummer=""
                bezoekpostcode=""
                verzuimpercentage=""
                WAO=""
                arbodienstpostplaats=""
                arbodienstpostadres=""
                ongevallen=""
                auteur=""
                woonplaats=""
                arbodienstpostcode=""
                postadres=""
                arbodienstemail=""
                arbodienstnaam=""
                orakkoorddatum=""
                lokatie=""
                aantalindienst=""/>
            </rieprogress>"""

    def testUpdateCompany_Empty(self):
        from tno.euphorie.session import Upload
        from euphorie.client import model
        from tno.euphorie.model import DutchCompany
        session=model.SurveySession()
        input=objectify.fromstring(self.BASE_SNIPPET)
        view=Upload(None, None)
        view.updateCompany(input, session)
        self.assertTrue(isinstance(session.dutch_company, DutchCompany))

    def testUpdateCompany_AantalInDienst(self):
        from tno.euphorie.session import Upload
        from euphorie.client import model
        session=model.SurveySession()
        input=objectify.fromstring(self.BASE_SNIPPET)
        view=Upload(None, None)
        input.gegevens.attrib["aantalindienst"]="1"
        view.updateCompany(input, session)
        self.assertEqual(session.dutch_company.employees, "40h")
        input.gegevens.attrib["aantalindienst"]="25"
        view.updateCompany(input, session)
        self.assertEqual(session.dutch_company.employees, "max25")
        input.gegevens.attrib["aantalindienst"]="999"
        view.updateCompany(input, session)
        self.assertEqual(session.dutch_company.employees, "over25")


