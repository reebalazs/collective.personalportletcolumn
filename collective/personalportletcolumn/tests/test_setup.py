from zope.site.hooks import setSite, setHooks
from zope.component import getSiteManager, getUtilitiesFor, getUtility

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignable
from plone.portlets.interfaces import IPortletType

from plone.app.portlets.interfaces import IRightColumn

from collective.personalportletcolumn.tests.base import layer_without_profile
from collective.personalportletcolumn.interfaces import IPersonalPortletManager

from Products.PloneTestCase import ptc

class TestProductInstall(ptc.PloneTestCase):
    layer = layer_without_profile 

    def afterSetUp(self):
        setHooks()
        setSite(self.portal)

    def testPortletManagersRegistered(self):
        right = getUtility(IPortletManager, 'plone.rightcolumn')
        self.failUnless(IRightColumn.providedBy(right))
        self.failIf(IPersonalPortletManager.providedBy(right))

        # Install it
        self.addProfile('collective.personalportletcolumn:default')

        right = getUtility(IPortletManager, 'plone.rightcolumn')
        self.failIf(IRightColumn.providedBy(right))
        self.failUnless(IPersonalPortletManager.providedBy(right))

        # Unistall it
        self.addProfile('collective.personalportletcolumn:uninstall')

        right = getUtility(IPortletManager, 'plone.rightcolumn')
        self.failUnless(IRightColumn.providedBy(right))
        self.failIf(IPersonalPortletManager.providedBy(right))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite
