from zope.interface import implements, Interface
from zope.component import adapts
from plone.portlets.interfaces import IPortletRetriever
from collective.personalportletcolumn.interfaces import IPersonalPortletManager
from plone.portlets.retriever import PortletRetriever

class PersonalPortletRetriever(PortletRetriever):
    """The personal portlet retriever.

    This will aggregate the contextual portlets, and then
    the contextless user (personal) portlets.
    """

    implements(IPortletRetriever)
    adapts(Interface, IPersonalPortletManager)
