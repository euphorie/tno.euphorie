from euphorie.client.browser.company import Company as GenericCompany
from euphorie.client.model import Session
from plone.memoize.view import memoize
from plone.supermodel.model import Schema
from plonetheme.nuplone.z3cform.form import FieldWidgetFactory
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from tno.euphorie.model import DutchCompany
from zope import schema
from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import datetime
import decimal


TextSpan1 = FieldWidgetFactory("z3c.form.browser.text.TextFieldWidget", klass="span-1")
TextSpan6 = FieldWidgetFactory("z3c.form.browser.text.TextFieldWidget", klass="span-6")


class DutchCompanySchema(Schema):
    title = schema.TextLine(title="Bedrijfsnaam", max_length=128, required=False)

    address_visit_address = schema.TextLine(title="Adres", required=False)
    address_visit_postal = schema.TextLine(
        title="Postcode", max_length=16, required=False
    )
    address_visit_city = schema.TextLine(title="Plaats", max_length=64, required=False)

    address_postal_address = schema.TextLine(title="Adres", required=False)
    address_postal_postal = schema.TextLine(
        title="Postcode", max_length=16, required=False
    )
    address_postal_city = schema.TextLine(title="Plaats", max_length=64, required=False)
    email = schema.ASCIILine(title="E-mailadres", max_length=128, required=False)
    # widget(email="tno.euphorie.company.TextSpan6")
    phone = schema.ASCIILine(title="Telefoonnummer", max_length=32, required=False)
    activity = schema.TextLine(
        title="Bedrijfsactiviteit", max_length=64, required=False
    )
    submitter_name = schema.TextLine(
        title="Naam invuller", max_length=64, required=False
    )
    submitter_function = schema.TextLine(
        title="Functie invuller", max_length=64, required=False
    )
    department = schema.TextLine(title="Afdeling", max_length=64, required=False)
    location = schema.TextLine(title="Lokatie", max_length=64, required=False)
    submit_date = schema.Date(
        title="Datum",
        description="Datum waarop de gegevens verzameld zijn",
        min=datetime.date(2000, 1, 1),
        required=False,
    )
    employees = schema.Choice(
        title="Aantal werknemers",
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm("40h", title="Maximaal 40 uur betaalde arbeid per week"),
                SimpleTerm("max25", title="Maximaal 25 werknemers"),
                SimpleTerm("over25", title="Meer dan 25 werknemers"),
            ]
        ),
        required=False,
    )
    absentee_percentage = schema.Decimal(
        title="Verzuimpercentage",
        min=decimal.Decimal(0),
        max=decimal.Decimal(100),
        required=False,
    )
    # widget(absentee_percentage="tno.euphorie.company.TextSpan1")
    accidents = schema.Int(title="Aantal ongevallen vorig jaar", required=False)
    # widget(accidents="tno.euphorie.company.TextSpan1")
    incapacitated_workers = schema.Int(
        title="Aantal mensen in de WIA vorig jaar", required=False
    )
    # widget(incapacitated_workers="tno.euphorie.company.TextSpan1")
    arbo_expert = schema.TextLine(
        title="Gegevens arbodienst/-deskundige", max_length=128, required=False
    )
    works_council_approval = schema.Date(
        title="Datum van akkoord OR/medewerkersvertegenwoordiging",
        min=datetime.date(2000, 1, 1),
        required=False,
    )


class Company(GenericCompany):
    """Update the company details.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a `PathGhost` object for
    the *inventory* component of the URL.
    """

    schema = DutchCompanySchema
    company = None
    errors = {}
    template = ViewPageTemplateFile("templates/report_company.pt")

    company_class = DutchCompany

    @property
    def default_company_values(self):
        """The values that are used when creating a new company.

        XXX: With respect to Euphorie, this should adds
        the submit_date to the default values.
        Once this is moved back to Euphorie, the submit_date can be added to the
        values obtained from super().default_company_values.
        """
        return {
            "session": self.session,
            "submit_date": datetime.date.today(),
        }

    @property
    @memoize
    def company(self):
        # XXX: This should be backported to Euphorie
        company = (
            Session.query(self.company_class)
            .filter(self.company_class.session == self.session)
            .first()
        )
        if not company:
            company = self.company_class(**self.default_company_values)
        directlyProvides(company, self.schema)
        return company

    def _assertCompany(self):
        # XXX: This should be removed, also in Euphorie
        return
