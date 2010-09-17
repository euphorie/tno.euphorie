import logging
from optparse import OptionParser
import sys
import lxml.etree
import lxml.objectify
import transaction
import zExceptions
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from Testing.makerequest import makerequest
from zope.site import hooks
from plone.dexterity.utils import createContentInContainer
from euphorie.content.upload import SurveyImporter
from euphorie.client import publish

log = logging.getLogger(__name__)


class Abort(RuntimeError):
    def __init__(self, message, exitcode=1):
        self.message=message
        self.exitcode=exitcode


def GetCountry(plone, options):
    sectors=plone.sectors
    if not hasattr(sectors, options.country):
        log.info("Creating missing country %s", options.country)
        sectors.invokeFactory("euphorie.country", options.country,
                title=options.country)
    return getattr(sectors, options.country)



def GetSector(country, branche, options):
    if options.sector is None:
        if not hasattr(branche, "account"):
            return None
        login=branche.account.get("login").lower()
        password=branche.account.get("password")
        email=branche.account.get("email")
    else:
        login=password=options.sector
        email=None

    sector=getattr(country, login, None)
    if sector is not None:
        return sector

    log.info("Creating new sector '%s' with password '%s'", login, password)
    id=country.invokeFactory("euphorie.sector", login,
            title=branche.title.text.strip())
    sector=getattr(country, id)
    sector.password=password
    sector.contact_email=email
    return sector



def ImportSector(plone, options, filename):
    input=open(filename, "r")
    dom=lxml.objectify.parse(input)
    branche=dom.getroot()

    country=GetCountry(plone, options)

    if not hasattr(branche, "survey"):
        return

    sector=GetSector(country, branche, options)
    if sector is None:
        raise Abort("No sector specified and no account information found.")

    # Login as the sector
    sectoruser=plone.acl_users.getUserById(sector.id)
    sm=getSecurityManager()
    try:
        newSecurityManager(None, sectoruser)

        name=options.name or unicode(branche.survey.title.text)

        if hasattr(sector, name):
            raise Abort("There is already a survey named '%s'" % name)

        log.info(u"Importing survey '%s' with version '%s'", name, options.version)
        group=createContentInContainer(sector, "euphorie.surveygroup",
                                       title=name)
        importer=SurveyImporter(group)
        survey=importer(branche, options.version)

        if options.publish:
            log.info("Publishing survey")
            publisher=publish.PublishSurvey(survey, None)
            publisher.publish()
    finally:
        setSecurityManager(sm)



def main():
    parser=OptionParser(usage="Usage: bin/instance run %prog [options] <XML-files>")
    parser.add_option("-p", "--publish",
                      help="Publish the imported sector.",
                      action="store_true", dest="publish", default=False)
    parser.add_option("-S", "--site",
                      help="id of the Plone site. Defaults to Plone",
                      action="store", type="string", dest="site", 
                      default="Plone")
    parser.add_option("-c", "--country",
                      help="The country where the branch/model should be created. "
                           "Defaults to nl.",
                      action="store", type="string", dest="country", 
                      default="nl")
    parser.add_option("-s", "--sector",
                      help="The name of the sector where the survey should be created.",
                      action="store", type="string", dest="sector") 
    parser.add_option("-n", "--name",
                      help="Override name for the imported survey.",
                      action="store", type="string", dest="name")
    parser.add_option("-v", "--version-name",
                      help="Name of the new survey version. Defaults to 'default'.",
                      action="store", type="string", dest="version",
                      default="default")

    (options, args)=parser.parse_args(sys.argv[1:])

    if not args:
        raise Abort("Please specify a (single) XML file to import.")

    # The magic Zope2 setup dance
    zope2=makerequest(app)
    hooks.setHooks()
    plone=getattr(zope2, options.site)
    hooks.setSite(plone)

    # Login as admin
    admin=zope2.acl_users.getUserById("admin")
    newSecurityManager(None, admin)

    for arg in args:
        transaction.begin()
        try:
            log.info("Importing %s", arg)
            ImportSector(plone, options, arg)
            trans=transaction.get()
            trans.setUser("-commandline-")
            trans.note("Import of %s" % arg)
            trans.commit()
        except lxml.etree.XMLSyntaxError, e:
            transaction.abort()
            log.error(e.message)
            log.error("Invalid input file")
        except RuntimeError, e:
            transaction.abort()
            log.error(e.message)
        except zExceptions.Unauthorized, e:
            transaction.abort()
            log.error(e.message)
            log.error("This is mostly likely due to too deep nesting in the survey.")
        except zExceptions.BadRequest, e:
            transaction.abort()
            log.error(e.message)
            log.error("This is mostly likely due to illegal input data.")
        except Exception, e:
            transaction.abort()
            raise


if __name__=="__main__":
    # We can not use logging.basicConfig since Zope2 has already configured things
    rootlog=logging.getLogger()
    rootlog.setLevel(logging.INFO)
    formatter=logging.Formatter("[%(levelname)s] %(message)s")
    for handler in rootlog.handlers:
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)

    main()

