from euphorie.client.browser.company import Company as GenericCompany
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
    title = schema.TextLine(title=u"Bedrijfsnaam", max_length=128, required=False)

    address_visit_address = schema.TextLine(title=u"Adres", required=False)
    address_visit_postal = schema.TextLine(
        title=u"Postcode", max_length=16, required=False
    )
    address_visit_city = schema.TextLine(title=u"Plaats", max_length=64, required=False)

    address_postal_address = schema.TextLine(title=u"Adres", required=False)
    address_postal_postal = schema.TextLine(
        title=u"Postcode", max_length=16, required=False
    )
    address_postal_city = schema.TextLine(
        title=u"Plaats", max_length=64, required=False
    )
    email = schema.ASCIILine(title=u"E-mailadres", max_length=128, required=False)
    # widget(email="tno.euphorie.company.TextSpan6")
    phone = schema.ASCIILine(title=u"Telefoonnummer", max_length=32, required=False)
    activity = schema.TextLine(
        title=u"Bedrijfsactiviteit", max_length=64, required=False
    )
    submitter_name = schema.TextLine(
        title=u"Naam invuller", max_length=64, required=False
    )
    submitter_function = schema.TextLine(
        title=u"Functie invuller", max_length=64, required=False
    )
    department = schema.TextLine(title=u"Afdeling", max_length=64, required=False)
    location = schema.TextLine(title=u"Lokatie", max_length=64, required=False)
    submit_date = schema.Date(
        title=u"Datum",
        description=u"Datum waarop de gegevens verzameld zijn",
        min=datetime.date(2000, 1, 1),
        required=False,
    )
    employees = schema.Choice(
        title=u"Aantal werknemers",
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(u"40h", title=u"Maximaal 40 uur betaalde arbeid per week"),
                SimpleTerm(u"max25", title=u"Maximaal 25 werknemers"),
                SimpleTerm(u"over25", title=u"Meer dan 25 werknemers"),
            ]
        ),
        required=False,
    )
    absentee_percentage = schema.Decimal(
        title=u"Verzuimpercentage",
        min=decimal.Decimal(0),
        max=decimal.Decimal(100),
        required=False,
    )
    # widget(absentee_percentage="tno.euphorie.company.TextSpan1")
    accidents = schema.Int(title=u"Aantal ongevallen vorig jaar", required=False)
    # widget(accidents="tno.euphorie.company.TextSpan1")
    incapacitated_workers = schema.Int(
        title=u"Aantal mensen in de WIA vorig jaar", required=False
    )
    # widget(incapacitated_workers="tno.euphorie.company.TextSpan1")
    arbo_expert = schema.TextLine(
        title=u"Gegevens arbodienst/-deskundige", max_length=128, required=False
    )
    works_council_approval = schema.Date(
        title=u"Datum van akkoord OR/medewerkersvertegenwoordiging",
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

    def _assertCompany(self):
        if self.company is not None:
            return
        session = self.session
        if session.dutch_company is None:
            session.dutch_company = DutchCompany(submit_date=datetime.date.today())
        directlyProvides(session.dutch_company, DutchCompanySchema)
        self.company = session.dutch_company
