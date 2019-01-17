from five import grok
from plonetheme.nuplone.skin import error
from ..interfaces import ITnoContentSkinLayer

grok.templatedir("templates")


class Unauthorized(error.Unauthorized):
    grok.layer(ITnoContentSkinLayer)
    grok.template("error_unauthorized")
