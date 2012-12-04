import datetime
import transaction
from Acquisition import aq_base
from Acquisition import aq_inner
from plone.directives import form
from five import grok
import lxml.etree
import lxml.objectify
from z3c.saconfig import Session
from zope.interface import Invalid
from z3c.form import button
from z3c.form.interfaces import WidgetActionExecutionError
from plone.namedfile.field import NamedFile
from euphorie.client.country import IClientCountry
from euphorie.client.sector import IClientSector
from euphorie.client.profile import BuildSurveyTree
from tno.euphorie.interfaces import ITnoClientSkinLayer
from euphorie.client import model
from euphorie.client.navigation import FindFirstQuestion
from euphorie.client.navigation import QuestionURL
from euphorie.content.interfaces import IQuestionContainer
from euphorie.content.survey import ISurvey
from euphorie.content.profilequestion import IProfileQuestion
from euphorie.content.upload import el_unicode
from euphorie.content.upload import attr_unicode
from euphorie.client.session import SessionManager
from tno.euphorie.model import DutchCompany
from tno.euphorie import MessageFactory as _

grok.templatedir("templates")


def parse_date(value, default=None):
    try:
        return datetime.datetime.strptime(value, "%d/%m/%Y").date()
    except ValueError:
        return default


def attr_date(node, tag, default=None):
    value = unicode(node.attrib.get(tag, u"")).strip()
    if not value:
        return default
    return parse_date(value, default)


def attr_int(node, tag, default=None):
    value = node.attrib.get(tag, None)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


class UploadSchema(form.Schema):
    file = NamedFile(
            title=_("label_session_file", default=u"RI&E bestand"),
            required=True)


class Upload(form.SchemaForm):
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(ITnoClientSkinLayer)
    grok.name("rie-session")
    grok.template("upload")
    form.wrap(False)

    ignoreContext = True
    schema = UploadSchema

    def updateCompany(self, input, session):
        mapping = {"afdeling": ("department", attr_unicode),
                   "bezoekadres": ("address_visit_address", attr_unicode),
                   "bezoekpostcode": ("address_visit_postal", attr_unicode),
                   "bezoekwoonplaats": ("address_visit_city", attr_unicode),
                   "postadres": ("address_postal_address", attr_unicode),
                   "postcode": ("address_postal_postal", attr_unicode),
                   "woonplaats": ("address_postal_city", attr_unicode),
                   "emailadres": ("email", attr_unicode),
                   "telefoonnummer": ("phone", attr_unicode),
                   "auteur": ("submitter_name", attr_unicode),
                   "datum": ("submit_date", attr_date),
                   "bedrijfsactiviteit": ("activity", attr_unicode),
                   "invullerfunctie": ("submitter_function", attr_unicode),
                   "lokatie": ("location", attr_unicode),
                   "verzuimpercentage": ("absentee_percentage", attr_int),
                   "ongevallen": ("accidents", attr_int),
                   "WAO": ("incapacitated_workers", attr_int),
                   }
        data = input.gegevens
        company = session.dutch_company = DutchCompany()

        for (old, new) in mapping.items():
            setattr(company, new[0], new[1](data, old))

        employees = attr_int(data, "aantalindienst")
        if employees is not None:
            if employees <= 1:
                company.employees = "40h"
            elif 1 < employees <= 25:
                company.employees = "max25"
            elif 25 < employees:
                company.employees = "over25"

        if attr_int(data, "orakkoord") == 1:
            company.works_council_approved = attr_date(data, "orakkoorddatum")

    def buildProfile(self, input, survey, session):
        idmap = {}
        for profilequestion in survey.values():
            if not IProfileQuestion.providedBy(profilequestion):
                continue
            idmap[profilequestion.external_id] = profilequestion
        if not idmap:
            return ({}, {})

        profile = {}
        keuzemap = {}  # Map `keuze' to profile index
        for facet in input.profiel.facet:
            question = idmap.get(facet.attrib["vraag-id"])
            if question is None:
                continue
            if question.type == "optional":
                profile[question.id] = True
                keuzemap[facet.keuze.attrib["antwoord"]] = 0
            elif question.type == "repeat":
                profile[question.id] = []
                for (i, keuze) in enumerate(facet.keuze):
                    antwoord = attr_unicode(keuze, "antwoord")
                    profile[question.id].append(antwoord)
                    keuzemap[keuze.attrib["antwoord"]] = i

        return (profile, keuzemap)

    def buildExternalIdMap(self, root, zodb_path=[], mapping=None):
        if mapping is None:
            mapping = {}
        for child in root.values():
            external_id = getattr(aq_base(child), "external_id", None)
            newpath = zodb_path + [child.id]
            if external_id is not None:
                mapping[external_id] = "/".join(newpath)
            if IQuestionContainer.providedBy(child):
                self.buildExternalIdMap(child, newpath, mapping)
        return mapping

    def updateAnswers(self, input, keuzemap, survey, session):
        idmap = self.buildExternalIdMap(survey)
        query = Session.query(model.Risk)\
                .filter(model.Risk.session_id == session.id)
        identification_map = {"1": "yes",
                              "2": "no",
                              "3": "n/a"}
        priority_map = {"laag": "low",
                        "midden": "medium",
                        "hoog": "high"}

        for antwoord in input.antwoorden.antwoord:
            risk_id = idmap.get(antwoord.attrib["risk-id"])
            if risk_id is None:
                continue

            risk = query\
                .filter(model.Risk.zodb_path == risk_id)\
                .filter(model.Risk.profile_index ==
                        keuzemap.get(antwoord.attrib["keuze"], 0))\
                .first()
            if risk is None:
                continue

            risk.identification = identification_map.get(antwoord.attrib["inventariseren"])
            if antwoord.attrib["inventariseren"] == "-1":
                risk.postponed = True
            elif risk.identification is not None:
                risk.postponed = False
            risk.probability = attr_int(antwoord, "evalueren1")
            risk.frequency = attr_int(antwoord, "evalueren2")
            risk.effect = attr_int(antwoord, "evalueren3")
            risk.priority = priority_map.get(antwoord.attrib["prioriteit"])
            if hasattr(antwoord, "opmerking"):
                risk.comment = el_unicode(antwoord, "opmerking")
            for pva in antwoord.iterchildren("pva"):
                plan = model.ActionPlan(risk=risk)
                plan.action_plan = el_unicode(pva, "maatregel")
                plan.prevention_plan = el_unicode(pva, "preventietaken")
                plan.requirements = el_unicode(pva, "preventiekennis")
                plan.responsible = el_unicode(pva, "uitvoerder")
                try:
                    plan.budget = int(pva.budget.text)
                except (TypeError, ValueError):
                    pass
                timeline = pva.planning.text.split()
                plan.planning_start = parse_date(timeline[0])
                plan.planning_end = parse_date(timeline[2])
                Session.add(plan)

        session.touch()

    def parseInput(self, input):
        """Try to parse a RI&E session file. The parsed data is
        returned as a lxml.objectified element. If the file could
        not be parsed or has the wrong format None is returned instead.
        """
        try:
            input = lxml.objectify.fromstring(input)
        except lxml.etree.XMLSyntaxError:
            return None

        if input.tag != "rieprogress":
            return None

        rie_path = input.attrib["rie_path"]
        if not rie_path.startswith("/rie/data/"):
            return None

        return input

    def findSurvey(self, input):
        """Find the survey to match the (already parsed) input data."""
        rie = input.attrib["rie_path"].split("/")[3]
        matches = []
        for sector in aq_inner(self.context).values():
            if not IClientSector.providedBy(sector):
                continue
            for survey in sector.values():
                if ISurvey.providedBy(survey) and \
                        survey.id != 'preview' and \
                        getattr(aq_base(survey), "external_id", None) == rie:
                    matches.append(survey)
        if not matches:
            return None
        # Pick the oldest published survey on the assumption this is not a
        # modified copy.
        matches.sort(key=lambda s: s.published[2], reverse=True)
        return matches[0]

    @button.buttonAndHandler(_("button_upload", default=u"Upload"), name="upload")
    def handleUpload(self, action):
        (data, errors) = self.extractData()
        if errors:
            return

        input = self.parseInput(data["file"].data)
        if input is None:
            raise WidgetActionExecutionError("file",
                    Invalid(_("error_invalid_session_file",
                        default=u"Geen valide RI&E bestand.")))

        survey = self.findSurvey(input)
        if survey is None:
            raise WidgetActionExecutionError("file",
                    Invalid(_("error_unknown_survey",
                        default=u"De gebruikte vragenlijst bestaat niet op deze site.")))

        session = SessionManager.start(
                attr_unicode(input, "rienaam", u"RI&E import"), survey)
        self.updateCompany(input, session)
        (profile, keuzemap) = self.buildProfile(input, survey, session)
        BuildSurveyTree(survey, profile, session)
        self.updateAnswers(input, keuzemap, survey, session)

        question = FindFirstQuestion(dbsession=session)
        if question is None:
            transaction.get().doom()
            raise WidgetActionExecutionError("file",
                    Invalid(u"Deze RI&E is helaas teveel veranderd om te kunnen gebruiken."))
        self.request.response.redirect(
                QuestionURL(survey, question, phase="identification"))
