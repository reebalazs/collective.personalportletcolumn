from zope.interface import implements
from zope.component import adapts, queryUtility

from zope.container.interfaces import INameChooser

from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser

from plone.portlets.interfaces import IPortletManager
from plone.portlets.constants import USER_CATEGORY

from .interfaces import IDefaultPersonalPortlet
from collective.personalportletcolumn.interfaces import IPersonalPortletManager
from zope.interface import providedBy
from plone.app.portlets import portlets

from plone.app.portlets.storage import UserPortletAssignmentMapping

def new_user(principal, event):
    """Initialise the dashboard for a new user
    """

    #import pdb; pdb.set_trace()
    defaults = IDefaultPersonalPortlet(principal, None)
    if defaults is None:
        return

    userid = principal.getId()
    portlets = defaults()

 
    for name in ('plone.rightcolumn', ):
        assignments = portlets.get(name)
        if assignments:
            column = queryUtility(IPortletManager, name=name)
            if column is not None:
                # Add the default portlets only, if this is our manager.
                # We must check this to avoid adding the default portlets 
                # when the product is not installed into the portal
                # (but the event triggers even in this case)
                if IPersonalPortletManager in providedBy(column):
                    category = column.get(USER_CATEGORY, None)
                    if category is not None:
                        manager = category.get(userid, None)
                        if manager is None:
                            manager = category[userid] = UserPortletAssignmentMapping(manager=name,
                                                                                      category=USER_CATEGORY,
                                                                                      name=userid)
                        chooser = INameChooser(manager)
                        for assignment in assignments:
                            manager[chooser.chooseName(None, assignment)] = assignment

class DefaultPersonalPortlet(object):
    """The default default dashboard.
    """

    implements(IDefaultPersonalPortlet)
    adapts(IPropertiedUser)

    def __init__(self, principal):
        self.principal = principal

    def __call__(self):
        return {
            'plone.rightcolumn' : (portlets.calendar.Assignment(), ),
        }

