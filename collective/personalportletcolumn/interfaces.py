from plone.portlets.interfaces import IPlacelessPortletManager
from zope.interface import Interface
from plone.app.portlets.browser.interfaces import IManageDashboardPortletsView

class IPersonalPortletManager(IPlacelessPortletManager):
    """xxxx xxxx """

class IManagePersonalPortletsView(IManageDashboardPortletsView):
    """xxxx xxxx """

class IDefaultPersonalPortlet(Interface):
    """Define an adapter from the user/principal type (by default, this is
    Products.PluggableAuthService.interfaces.authservice.IBasicUser) to
    this interface and implement __call__ to return a mapping of dashboard
    settings. When a new user is created, this adapter will be invoked to
    build a default dashboard.
    """

    def __call__(self):
        """Create and return dashboard portlet assignments. Should be a
        mapping of dashboard column names ('plone.dashboard1',
        'plone.dashboard2', 'plone.dashboard3' and/or 'plone.dashboard4')
        and a list of portlet assignmen instances.
        """
