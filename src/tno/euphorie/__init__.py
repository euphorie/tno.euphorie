from euphorie.client.browser.webhelpers import WebHelpers
from zope.i18nmessageid import MessageFactory as mf


# Patch the WebHelpers class to hide the organisation tab
# See https://github.com/syslabcom/scrum/issues/519
WebHelpers.hide_organisation_tab = True

MessageFactory = mf("tno.euphorie")
del mf


__all__ = ["MessageFactory"]
