from Products.CMFCore.utils import getToolByName

def uninstall(portal, reinstall=False):

    if not reinstall:

        # normal uninstall
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-collective.personalportletcolumn:uninstall')

        return "Ran all uninstall steps."

