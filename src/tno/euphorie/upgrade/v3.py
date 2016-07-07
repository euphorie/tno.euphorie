# -*- coding: <utf-8> -*-
from plone import api


def install_private_resources(context):
    """ Install the oira.private egg, which contains non-free JS and CSS
        resources.
    """
    setup = api.portal.get_tool('portal_setup')
    setup.runAllImportStepsFromProfile('profile-oira.private:default')
