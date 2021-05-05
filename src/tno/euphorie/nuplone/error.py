from ..interfaces import ITnoContentSkinLayer
from five import grok
from plonetheme.nuplone.skin import error


grok.templatedir("templates")


class Unauthorized(error.Unauthorized):
    grok.layer(ITnoContentSkinLayer)
    grok.template("error_unauthorized")
