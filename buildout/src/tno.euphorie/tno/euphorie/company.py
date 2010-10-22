import calendar
import datetime
from five import grok
from repoze import formapi
from euphorie.client import MessageFactory as _
from euphorie.client.survey import PathGhost
from euphorie.client.session import SessionManager
from tno.euphorie.interfaces import ITnoReportPhaseSkinLayer
from tno.euphorie.model import DutchCompany

grok.templatedir("templates")


class CompanyForm(formapi.Form):
    """A single action plan item."""

    fields = dict(title=unicode,
                  address_visit_address=unicode,
                  address_visit_postal=unicode,
                  address_visit_city=unicode,
                  address_postal_address=unicode,
                  address_postal_postal=unicode,
                  address_postal_city=unicode,
                  email=str,
                  phone=str,
                  activity=unicode,
                  submitter_name=unicode,
                  submitter_function=unicode,
                  department=unicode,
                  location=unicode,
                  submit_date_day=int,
                  submit_date_month=int,
                  submit_date_year=int,
                  employees=str,
                  absentee_percentage=float,
                  accidents=int,
                  incapacitated_workers=int,
                  arbo_expert=unicode,
                  works_council=bool,
                  works_council_approval_day=int,
                  works_council_approval_month=int,
                  works_council_approval_year=int)

    @formapi.validator("submit_date_day")
    def valid_submit_day(self):
        day=self.data["submit_date_day"]
        if day is None:
            return
        if not 1<=day<=31:
            yield _(u"Invalid day of month")

        try:
            (__, maxday)=calendar.monthrange(self.data["submit_date_year"],
                                            self.data["submit_date_month"])
            if day>maxday:
                yield _(u"Invalid day of month")
        except TypeError:
            # Invalid year most likely
            pass


    @formapi.validator("submit_date_year")
    def valid_submit_year(self):
        year=self.data["submit_date_year"]
        if year is None:
            return
        if year<1900:
            yield u"Het jaartal moet 1900 of later zijn"


    @formapi.validator("works_council_approval_day")
    def valid_works_council_approval_day(self):
        if not self.data["works_council"]:
            # Do not validate of works council did not approve
            return

        day=self.data["works_council_approval_day"]
        if day is None:
            return
        if not 1<=day<=31:
            yield _(u"Invalid day of month")

        try:
            (__, maxday)=calendar.monthrange(self.data["works_council_approval_year"],
                                            self.data["works_council_approval_month"])
            if day>maxday:
                yield _(u"Invalid day of month")
        except TypeError:
            # Invalid year most likely
            pass


    @formapi.validator("works_council_approval_year")
    def valid_works_council_approval_year(self):
        year=self.data["works_council_approval_year"]
        if year is None:
            return
        if year<1900:
            yield u"Het jaartal moet 1900 of later zijn"




class ReportCompanyDetails(grok.View):
    """Intro page for report phase.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a `PathGhost` object for
    the *inventory* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(ITnoReportPhaseSkinLayer)
    grok.template("report_company")
    grok.name("company")

    def update(self):
        self.session=session=SessionManager.session

        if session.dutch_company is None:
            session.dutch_company=DutchCompany(submit_date=datetime.date.today())

        self.errors={}
        if self.request.environ["REQUEST_METHOD"]=="POST":
            reply=dict([(key,value) for (key,value) in self.request.form.items()
                        if value and (not isinstance(value, basestring) or value.strip())])
            if reply.get("absentee_percentage"):
                reply["absentee_percentage"]=reply["absentee_percentage"].replace(",", ".")
            company=session.dutch_company
            form=CompanyForm(params=reply)
            if not form.validate():
                self.errors=form.errors._dict
            else:
                for key in [ "title", "address_visit_address",
                             "address_visit_postal", "address_visit_city",
                             "address_postal_address", "address_postal_postal",
                             "address_postal_city", "email", "phone",
                             "activity", "submitter_name",
                             "submitter_function", "department", "location",
                             "employees", "absentee_percentage", "accidents",
                             "incapacitated_workers", "arbo_expert"]:
                    setattr(company, key, form.data[key])

                if reply.get("works_council"):
                    try:
                        company.works_council_approval=datetime.date(form.data["works_council_approval_year"],
                                form.data["works_council_approval_month"], form.data["works_council_approval_day"])
                    except TypeError:
                        pass
                if form.data["submit_date_day"] and form.data["submit_date_year"]:
                    try:
                        company.submit_date=datetime.date(form.data["submit_date_year"],
                                form.data["submit_date_month"], form.data["submit_date_day"])
                    except TypeError:
                        pass

                if reply["next"]=="previous":
                    url="%s/report" % self.request.survey.absolute_url()
                else:
                    url="%s/report/view" % self.request.survey.absolute_url()
                self.request.response.redirect(url)

