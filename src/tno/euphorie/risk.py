from five import grok
from euphorie.client.risk import ActionPlanView
from tno.euphorie.interfaces import ITnoActionPlanPhaseSkinLayer


grok.templatedir('templates')


class TnoActionPlanView(ActionPlanView):
    grok.layer(ITnoActionPlanPhaseSkinLayer)
    grok.name('view')
    grok.template('risk_actionplan')
