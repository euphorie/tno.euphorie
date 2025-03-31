from ftw.upgrade import UpgradeStep
from logging import getLogger
from plone import api
from plone.app.upgrade.bbb import ITinyMCE


logger = getLogger(__name__)


class RemoveBrokenTinyMCEUtility(UpgradeStep):
    """Remove broken TinyMCE utility."""

    def __call__(self):
        portal = api.portal.get()
        sm = portal.getSiteManager()
        removed = sm.unregisterUtility(provided=ITinyMCE)
        if removed:
            logger.info("Removed TinyMCE utility.")
