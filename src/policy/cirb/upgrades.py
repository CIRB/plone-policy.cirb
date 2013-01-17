import logging
from plone import api
from Products.CMFCore.utils import getToolByName

PROFILE = "profile-policy.cirb:default"
BLACKLIST_UPGRADES = ('PloneHelpCenter',)


def empty_portalskins_custom(context):
    logger = logging.getLogger(PROFILE)
    portal_skins = getToolByName(context, 'portal_skins')
    custom_folder = portal_skins.custom
    customs = custom_folder.keys()
    portal_skins.custom.manage_delObjects(customs)
    logger.info('custom folder is now empty')


def quickinstall_addons(context, install=None, uninstall=None, upgrades=None):
    logger = logging.getLogger(PROFILE)
    qi = getToolByName(context, 'portal_quickinstaller')

    if install is not None:
        for addon in install:
            if qi.isProductInstallable(addon):
                qi.installProduct(addon)
            else:
                logger.error('%s can t be installed' % addon)

    if uninstall is not None:
        qi.uninstallProducts(uninstall)

    if upgrades is not None:
        if upgrades in ("all", True):
            #TODO: find which addons should be upgrades
            installedProducts = qi.listInstalledProducts(showHidden=True)
            upgrades = [p['id'] for p in installedProducts
                        if p not in BLACKLIST_UPGRADES]
        logger.info(upgrades)
        for upgrade in upgrades:
            # do not try to upgrade myself -> recursion
            if upgrade in ('policy.cirb', 'PloneHelpCenter'):
                continue
            try:
                qi.upgradeProduct(upgrade)
            except KeyError:
                logger.error('can t upgrade %s' % upgrade)


def common(context):
    logger = logging.getLogger(PROFILE)

    # remove everythings from the portal_skins/custom
    # empty_portalskins_custom(context)

    # upgrade Plone itself:
    portal_migration = getToolByName(context, 'portal_migration')
    portal_migration.upgrade()
    logger.info("Ran Plone Upgrade")

    #upgrades installed addons
    quickinstall_addons(context, upgrades=True)

    context.runAllImportStepsFromProfile(PROFILE)
    logger.info("Apply %s" % PROFILE)

    migrate_to_cirb_blog(context)


def migrate_to_cirb_blog(context):
    portal = api.portal.get()
    blog = None
    if 'blog' in portal.objectIds():
        blog = portal.blog
        if blog.portal_type == 'Link':
            api.content.delete(blog)
            blog = None
    if blog is None:
        blog = api.content.create(portal, 'Folder', 'blog', 'Blog')
    #call the blog setup view
    blog.restrictedTraverse('cirb_blog_setup')()
