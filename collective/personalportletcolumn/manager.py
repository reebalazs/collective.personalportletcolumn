import logging

from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.personalportletcolumn.interfaces import IPersonalPortletManager

from plone.app.portlets.manager import ColumnPortletManagerRenderer

logger = logging.getLogger('portlets')

class PersonalPortletManagerRenderer(ColumnPortletManagerRenderer):
    """
    """

    adapts(Interface, IDefaultBrowserLayer, IBrowserView, IPersonalPortletManager)
    template = ViewPageTemplateFile('browser/templates/personal-portlet.pt')

    
