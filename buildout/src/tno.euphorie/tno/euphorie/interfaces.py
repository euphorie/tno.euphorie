from zope.interface import Interface
from euphorie.client.interfaces import IClientSkinLayer

class IProductLayer(Interface):
    """Marker interface for requests indicating the tno.euphorie
    package has been installed.
    """


class ITnoClientSkinLayer(IClientSkinLayer):
    """Marker interface for the TNO client skin."""
