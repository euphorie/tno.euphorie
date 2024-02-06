from euphorie.client.client import ClientPublishTraverser as BaseClientPublishTraverser
from euphorie.client.client import IClient
from tno.euphorie.interfaces import IProductLayer
from tno.euphorie.interfaces import ITnoClientSkinLayer
from zope.component import adapter


@adapter(IClient, IProductLayer)
class ClientPublishTraverser(BaseClientPublishTraverser):
    """Publish traverser to setup the skin layer.

    This traverser marks the request with ITnoClientSkinLayer when the
    client is traversed and the tno.euphorie product is installed.
    """

    skin_layer = ITnoClientSkinLayer
