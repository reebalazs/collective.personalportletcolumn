from zope.interface import implements
from zope.component import adapts, getUtility
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.http import IHTTPRequest
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignable
from plone.portlets.constants import USER_CATEGORY
from collective.personalportletcolumn.storage import PersonalPortletAssignmentMapping


class PersonalPortletsNamespace(object):
    """Used to traverse to a portlet assignable for the current user for
    the dashboard.
    """
    implements(ITraversable)
    adapts(ILocalPortletAssignable, IHTTPRequest)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        col, user = name.split('+')
        column = getUtility(IPortletManager, name=col)
        category = column[USER_CATEGORY]
        manager = category.get(user, None)
        if manager is None:
            manager = category[user] = PersonalPortletAssignmentMapping(manager=col,
                                                                    category=USER_CATEGORY,
                                                                    name=user)

        # XXX: For graceful migration
        if not getattr(manager, '__manager__', None):
            manager.__manager__ = col
        if not getattr(manager, '__category__', None):
            manager.__category__ = USER_CATEGORY
        if not getattr(manager, '__name__', None):
            manager.__name__ = user



        return manager

