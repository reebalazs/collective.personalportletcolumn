from Products.PloneTestCase import ptc
from collective.testcaselayer import ptc as tcl_ptc
from collective.testcaselayer import common
from Testing import ZopeTestCase

class LayerWithoutProfile(tcl_ptc.BasePTCLayer):
     """Install collective.personalportletcolumn"""

     def afterSetUp(self):
         ZopeTestCase.installPackage('collective.personalportletcolumn')

         import collective.personalportletcolumn
         self.loadZCML('configure.zcml', package=collective.personalportletcolumn)

layer_without_profile = LayerWithoutProfile([common.common_layer])


class Layer(tcl_ptc.BasePTCLayer):
     """Install collective.personalportletcolumn"""

     def afterSetUp(self):

         self.addProfile('collective.personalportletcolumn:default')

layer = Layer([layer_without_profile])


class PersonalPortletsBaseTestCase(ptc.PloneTestCase):
    layer = layer

