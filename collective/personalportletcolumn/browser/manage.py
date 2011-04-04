from zope.interface import implements
from plone.portlets.constants import USER_CATEGORY
from zope.component import getMultiAdapter, getUtility
from plone.portlets.interfaces import IPortletManager
from collective.personalportletcolumn.interfaces import IManagePersonalPortletsView
from plone.app.portlets.browser.manage import ManageDashboardPortlets
from collective.personalportletcolumn.storage import PersonalPortletAssignmentMapping


class ManagePersonalPortlets(ManageDashboardPortlets):
    implements(IManagePersonalPortletsView)

    # IManagePortletsView implementation

    def getAssignmentMappingUrl(self, manager):
        baseUrl = str(getMultiAdapter((self.context, self.request), name='absolute_url'))
        userId = self._getUserId()
        return '%s/++personalportlets++%s+%s' % (baseUrl, manager.__name__, userId)

    def getAssignmentsForManager(self, manager):
        userId = self._getUserId()
        column = getUtility(IPortletManager, name=manager.__name__)
        category = column[USER_CATEGORY]
        mapping = category.get(userId, None)
        if mapping is None:
            mapping = category[userId] = PersonalPortletAssignmentMapping(manager=manager.__name__,
                                                                      category=USER_CATEGORY,
                                                                      name=userId)
        return mapping.values()

