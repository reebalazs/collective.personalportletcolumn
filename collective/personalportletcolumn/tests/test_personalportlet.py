from zope.event import notify
from zope.component import getUtility
from plone.portlets.interfaces import IPortletManager
from plone.portlets.constants import USER_CATEGORY
from Products.PluggableAuthService.events import PrincipalCreated
from Products.PluggableAuthService.PropertiedUser import PropertiedUser

from collective.personalportletcolumn.tests.base import PersonalPortletsBaseTestCase

class TestPersonalPortlet(PersonalPortletsBaseTestCase):

    def test_default_personalportlet_created_for_new_user(self):

        col = getUtility(IPortletManager, name='plone.rightcolumn')
        user_portlets = col[USER_CATEGORY]
        self.failIf('fakeuser' in user_portlets)

        # This would normally happen when a user is created
        notify(PrincipalCreated(PropertiedUser('fakeuser')))

        # We would expect some portlets to have been created after the
        # event handler has finished processing
        self.failUnless('fakeuser' in user_portlets)
        self.assertEqual(len(user_portlets['fakeuser']), 1)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPersonalPortlet))
    return suite
