from zope.interface import Interface
from five import grok
from plonetheme.nuplone.skin import layout as nuplone
from ..interfaces import ITnoContentSkinLayer

grok.templatedir("templates")


class Layout(nuplone.Layout):
    grok.context(Interface)
    grok.name("layout")
    grok.layer(ITnoContentSkinLayer)
    grok.template("layout")
