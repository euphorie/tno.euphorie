from lxml import objectify

from tno.euphorie.testing import TnoEuphorieTestCase


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


