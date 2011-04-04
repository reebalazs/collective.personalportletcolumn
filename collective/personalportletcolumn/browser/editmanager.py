
from zope.component import adapts
from zope.interface import Interface
from collective.personalportletcolumn.interfaces import IManagePersonalPortletsView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from collective.personalportletcolumn.interfaces import IPersonalPortletManager
from plone.app.portlets.browser.editmanager import EditPortletManagerRenderer

class PersonalPortletsEditPortletManagerRenderer(EditPortletManagerRenderer):
    """Render a portlet manager in edit mode for the dashboard"""
    adapts(Interface, IDefaultBrowserLayer,  IManagePersonalPortletsView, IPersonalPortletManager)


