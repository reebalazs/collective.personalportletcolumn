from zope.interface import implements
from collective.personalportletcolumn.interfaces import IManagePersonalPortletsView
from plone.app.portlets.browser.manage import ManageDashboardPortlets

class ManagePersonalPortlets(ManageDashboardPortlets):
    implements(IManagePersonalPortletsView)

    # IManagePortletsView implementation

