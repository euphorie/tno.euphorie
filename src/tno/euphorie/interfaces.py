from zope.interface import Interface
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.interfaces import IIdentificationPhaseSkinLayer
from euphorie.client.interfaces import IEvaluationPhaseSkinLayer
from euphorie.client.interfaces import IActionPlanPhaseSkinLayer
from euphorie.client.interfaces import IReportPhaseSkinLayer
from euphorie.client.api.interfaces import IClientAPISkinLayer


class IProductLayer(Interface):
    """Marker interface for requests indicating the tno.euphorie
    package has been installed.
    """


class ITnoFormLayer(INuPloneFormLayer):
    """Browser layer to indicate we want TNO form components."""


class ITnoContentSkinLayer(ITnoFormLayer, NuPloneSkin):
    """Marker interface for the CMS/Content editing skin."""


class ITnoClientSkinLayer(IClientSkinLayer):
    """Marker interface for the TNO client skin."""


class ITnoIdentificationPhaseSkinLayer(IIdentificationPhaseSkinLayer):
    """Marker interface for the identification phase in a tno.euphorie site."""


class ITnoEvaluationPhaseSkinLayer(IEvaluationPhaseSkinLayer):
    """Marker interface for the evaluation phase in a tno.euphorie site."""


class ITnoActionPlanPhaseSkinLayer(IActionPlanPhaseSkinLayer):
    """Marker interface for the action plan phase in a tno.euphorie site."""


class ITnoReportPhaseSkinLayer(IReportPhaseSkinLayer):
    """Marker interface for the report phase in a tno.euphorie site."""


class ITnoClientAPISkinLayer(IClientAPISkinLayer):
    """Marker itnerface for the tno.euphorie extensions to the client API."""
