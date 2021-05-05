from ..interfaces import ITnoContentSkinLayer
from five import grok
from plonetheme.nuplone.skin import contact


class ContactForm(contact.ContactForm):
    grok.require("cmf.ManagePortal")
    grok.layer(ITnoContentSkinLayer)
