from tno.euphorie.testing import TnoEuphorieFunctionalTestCase


class ClientPublishTraverserTests(TnoEuphorieFunctionalTestCase):
    def ClientPublishTraverser(self, *a, **kw):
        from tno.euphorie.client import ClientPublishTraverser

        return ClientPublishTraverser(*a, **kw)
