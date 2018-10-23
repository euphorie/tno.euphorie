# coding=utf-8
from euphorie.client.browser.webhelpers import WebHelpers
from logging import getLogger
from euphorie.decorators import reify

log = getLogger(__name__)


class TNOWebHelpers(WebHelpers):

    @reify
    def styles_override(self):

        css = super(TNOWebHelpers, self).styles_override
        css += """
#osc .miller-columns .browser .item .object-name {
    color: inherit;
}
"""
        return css
