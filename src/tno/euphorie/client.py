from zope.component import adapts
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides
from zope.publisher.interfaces.browser import IBrowserSkinType
from ZPublisher.BaseRequest import DefaultPublishTraverse
from tno.euphorie.interfaces import IProductLayer
from tno.euphorie.interfaces import ITnoClientSkinLayer
from tno.euphorie.interfaces import ITnoClientAPISkinLayer
from euphorie.client.client import IClient
from euphorie.client.api.entry import access_api


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

        if name == 'api':
           api = access_api(request).__of__(self.context)
           directlyProvides(request, ITnoClientAPISkinLayer, [])
           return api

        ifaces = [iface for iface in directlyProvidedBy(request)
                  if not IBrowserSkinType.providedBy(iface)]
        directlyProvides(request, ITnoClientSkinLayer, ifaces)
        return super(ClientPublishTraverser, self)\
                .publishTraverse(request, name)
