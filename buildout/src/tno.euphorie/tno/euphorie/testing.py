from collective.testcaselayer import ptc
from euphorie.deployment.tests.functional import EuphorieLayer
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.PloneTestCase import PloneTestCase


class TnoEuphorieTestLayer(ptc.BasePTCLayer):
    def afterSetUp(self):
        from Testing.ZopeTestCase import installPackage
        from Products.Five import zcml
        from Products.Five import fiveconfigure
        import tno.euphorie

        fiveconfigure.debug_mode = True
        zcml.load_config("configure.zcml", tno.euphorie)
        fiveconfigure.debug_mode = False

        installPackage("tno.euphorie")
        self.addProduct("tno.euphorie")

        import tno.euphorie.model
        assert tno.euphorie.model._instrumented
        from euphorie.client import model
        from z3c.saconfig import Session
        model.metadata.create_all(Session.bind, checkfirst=True)

    def beforeTearDown(self):
        pass
    

TnoEuphorieLayer = TnoEuphorieTestLayer([EuphorieLayer, ptc.ptc_layer])


class TnoEuphorieTestCase(PloneTestCase.PloneTestCase):
    layer = TnoEuphorieLayer


class TnoEuphorieFunctionalTestCase(EuphorieFunctionalTestCase):
    layer = TnoEuphorieLayer

