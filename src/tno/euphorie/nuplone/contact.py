from five import grok
from plonetheme.nuplone.skin import contact
from ..interfaces import ITnoContentSkinLayer


class ContactForm(contact.ContactForm):
    grok.require("cmf.ManagePortal")
    grok.layer(ITnoContentSkinLayer)
