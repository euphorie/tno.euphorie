# coding=utf-8
from euphorie.client.browser.webhelpers import WebHelpers
from logging import getLogger
from plone.memoize.instance import memoize

log = getLogger(__name__)


class TNOWebHelpers(WebHelpers):

    @memoize
    def styles_override(self):

        css = super(TNOWebHelpers, self).styles_override
        css += """
#osc .miller-columns .browser .item .object-name {
    color: inherit;
}
"""
        return css
