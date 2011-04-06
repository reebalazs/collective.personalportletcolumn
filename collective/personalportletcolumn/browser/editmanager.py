
from zope.component import adapts
from zope.interface import Interface
from collective.personalportletcolumn.interfaces import IManagePersonalPortletsView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from collective.personalportletcolumn.interfaces import IPersonalPortletManager
from plone.app.portlets.browser.interfaces import IManageContextualPortletsView
from plone.app.portlets.browser.editmanager import EditPortletManagerRenderer
from plone.app.portlets.browser.editmanager import ContextualEditPortletManagerRenderer
from AccessControl import Unauthorized
from zope.component import getUtilitiesFor
from plone.portlets.interfaces import IPortletType
from plone.app.portlets.interfaces import IColumn

class PersonalPortletsEditPortletManagerRenderer(EditPortletManagerRenderer):
    """Render a portlet manager in edit mode for the personal column

    This is the edit renderer that is active in our @@manage-personal-portlets view
    """
    adapts(Interface, IDefaultBrowserLayer,  IManagePersonalPortletsView, IPersonalPortletManager)


class PersonalPortletsContextualEditPortletManagerRenderer(ContextualEditPortletManagerRenderer):
    """Render a portlet manager in edit mode for the personal column

    This is the edit renderer that is active in the old @@manage-portlets view

    This view makes it possible for the admin only, to manage the contextual portlets
    that will appear above the personal portlets in the same column.

    But we want to make all the portlets, normally registered for IColumn, to be
    addable here. If we omit the redefinition of this manager, then only
    the portlets registered for IPersonalPortletManager, would be available for adding here.
    So, we need some customization here to get the desired behaviour.
    """
    adapts(Interface, IDefaultBrowserLayer,  IManageContextualPortletsView, IPersonalPortletManager)

    def _addable_portlet_types(self):
        # in the original class, we had:
        #      portlets = self.manager.getAddablePortletTypes()
        # ... we would get the portlets registered for IPersonalPortletManager.
        # Instead, we query the ones registered for IColumn, in a hardcoded way.
        # 
        manager_interface = IColumn
        portlet_types = [ p for (_name, p) in getUtilitiesFor(IPortletType) 
                          if manager_interface in p.for_ ]
        return portlet_types

    # This needs to be copypasted just for plugging in
    # _addable_portlet_types.
    def addable_portlets(self):
        baseUrl = self.baseUrl()
        addviewbase = baseUrl.replace(self.context_url(), '')
        def sort_key(v):
            return v.get('title')
        def check_permission(p):
            addview = p.addview
            if not addview:
                return False

            addview = "%s/+/%s" % (addviewbase, addview,)
            if addview.startswith('/'):
                addview = addview[1:]
            try:
                self.context.restrictedTraverse(str(addview))
            except (AttributeError, KeyError, Unauthorized,):
                return False
            return True

        portlets =  [{
            'title' : p.title,
            'description' : p.description,
            'addview' : '%s/+/%s' % (addviewbase, p.addview)
            } for p in self._addable_portlet_types() if check_permission(p)]
            
        portlets.sort(key=sort_key)
        return portlets
