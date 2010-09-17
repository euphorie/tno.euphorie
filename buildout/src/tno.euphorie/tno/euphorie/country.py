from five import grok
from euphorie.client.country import View as BaseView
from euphorie.client.country import IClientCountry
from tno.euphorie.interfaces import ITnoClientSkinLayer

grok.templatedir("templates")

class View(BaseView):
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(ITnoClientSkinLayer)
    grok.template("sessions")

