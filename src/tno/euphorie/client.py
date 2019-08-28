from euphorie.client.client import IClient
from tno.euphorie.interfaces import IProductLayer
from tno.euphorie.interfaces import ITnoClientSkinLayer
from zope.component import adapts
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides
from zope.publisher.interfaces.browser import IBrowserSkinType
from ZPublisher.BaseRequest import DefaultPublishTraverse


class ClientPublishTraverser(DefaultPublishTraverse):
    """Publish traverser to setup the skin layer.

    This traverser marks the request with ITnoClientSkinLayer when the
    client is traversed and the tno.euphorie product is installed.
    """

    adapts(IClient, IProductLayer)

    def publishTraverse(self, request, name):
        from euphorie.client.utils import setRequest

        setRequest(request)
        request.client = self.context

        ifaces = [
            iface
            for iface in directlyProvidedBy(request)
            if not IBrowserSkinType.providedBy(iface)
        ]
        directlyProvides(request, ITnoClientSkinLayer, ifaces)
        return super(ClientPublishTraverser, self).publishTraverse(request, name)
