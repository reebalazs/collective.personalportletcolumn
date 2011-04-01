from zope.component import queryUtility
from zope.component import getUtilitiesFor
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletType
from plone.portlets.manager import PortletManager
from zope.interface import alsoProvides
from collective.personalportletcolumn.interfaces import IPersonalPortletManager
from plone.portlets.constants import USER_CATEGORY
from plone.portlets.constants import GROUP_CATEGORY
from plone.portlets.constants import CONTENT_TYPE_CATEGORY
from plone.portlets.storage import PortletCategoryMapping
from zope.interface import providedBy

def setupVarious(context):

    if context.readDataFile('collective.personalportletcolumn_import_various_install_marker.txt') is not None:
        # Marker file present - install
        setupVarious_install(context)

    if context.readDataFile('collective.personalportletcolumn_import_various_uninstall_marker.txt') is not None:
        # Marker file present - uninstall
        setupVarious_uninstall(context)
    
    # if no marker present - do nothing
    
def setupVarious_install(context):
    name = 'plone.rightcolumn'
    site = context.getSite()
    site.getSiteManager()
    sm = site.getSiteManager()

    u = queryUtility(IPortletManager, name=name)
    our_interface = False
    if u is not None:
        # Remove the utility only if it is not ours already.
        # This assures that Reinstall does not purge the portlet data.
        our_interface = IPersonalPortletManager in providedBy(u)
        if not our_interface:
            sm.unregisterUtility(provided=IPortletManager, name=name)
    
    assert our_interface or queryUtility(IPortletManager, name=name) is None

    # Create the utility only if needed
    if not our_interface:

        # Create our portlet manager
        manager = PortletManager()
        
        alsoProvides(manager, IPersonalPortletManager)
       
        manager[USER_CATEGORY] = PortletCategoryMapping()
        manager[GROUP_CATEGORY] = PortletCategoryMapping()
        manager[CONTENT_TYPE_CATEGORY] = PortletCategoryMapping()

        sm.registerUtility(component=manager, provided=IPortletManager, name=name)


def setupVarious_uninstall(context):
    # We must remove the manager interface from all portlets where it has been added.
    # If we miss to do this, the product could never be removed from the instance.
    portlets = getUtilitiesFor(IPortletType)
    for name, portlet_type in portlets:
        # if it has our interface: remove it
        if IPersonalPortletManager in portlet_type.for_:
            portlet_type.for_.remove(IPersonalPortletManager)
            # IMPORTANT to make this dirty for ZODB
            portlet_type.for_ = portlet_type.for_
