from zope.interface import implements
from plone.app.portlets.storage import PortletAssignmentMapping
from collective.personalportletcolumn.interfaces import IPersonalPortletAssignmentMapping

class PersonalPortletAssignmentMapping(PortletAssignmentMapping):
    """An assignment mapping for personal portlets
    """

    implements(IPersonalPortletAssignmentMapping)

    @property
    def id(self):
        manager = self.__manager__
        key = self.__name__

        return "++personalportlets++%s+%s" % (manager, key,)

