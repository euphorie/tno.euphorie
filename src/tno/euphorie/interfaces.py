from euphorie.client.interfaces import IClientSkinLayer
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from zope.interface import Interface


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
