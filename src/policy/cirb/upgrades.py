import logging
from plone import api

from Products.CMFCore.utils import getToolByName

from zope.app.container.interfaces import INameChooser
from zope.site.hooks import getSite
from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from plone.app.portlets.portlets import navigation


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
    clean_old_interfaces(context)

    # remove everythings from the portal_skins/custom
    # empty_portalskins_custom(context)

    # upgrade Plone itself:
    portal_migration = getToolByName(context, 'portal_migration')
    portal_migration.upgrade()
    logger.info("Ran Plone Upgrade")

    quickinstall_addons(context, install=['cirb.blog'])

    #upgrades installed addons
    quickinstall_addons(context, upgrades=True)

    context.runAllImportStepsFromProfile(PROFILE)
    logger.info("Apply %s" % PROFILE)

    migrate_to_cirb_blog(context)
    logger.info("End upgrade policy cirb")


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


def clean_old_interfaces(context):
    log = logging.getLogger("policy CIRB clean old interfaces")

    registry = context.getImportStepRegistry()
    old_steps = ["cirb.site.various", "setupFolderNav"]
    for old_step in old_steps:
        if old_step in registry.listSteps():
            registry.unregisterStep(old_step)
            # Unfortunately we manually have to signal the context
            # (portal_setup)
            # that it has changed otherwise this change is not persisted.
            context._p_changed = True
            log.info("Old %s import step removed from import registry.",
                        old_step)

    # XXX clean some unused skins !
    adapters = getSite().getSiteManager().adapters._adapters
    # 'IThemeSpecific' from module 'cirb.site.browser.interfaces
    for adapter in adapters:
        if adapter.keys():
            if adapter.keys()[0].__module__ == 'zope.interface':
                dic = adapter.values()[0]
                for key in dic.keys():
                    if key.__module__ == 'cirb.site.browser.interfaces':
                        del dic[key]
                        log.info("delete {0} ".format(key.__module__))
                        getSite().getSiteManager().adapters._p_changed = True

    getSite().getSiteManager().adapters._adapters = adapters
    context._p_jar.sync()


def migrate_to_fr_nl_folder(context):
    if not getattr(context, 'fr'):
        return
    home_fr = getattr(context.fr, 'start-1-fr').homepage
    home_nl = getattr(context.nl, 'start-1').home
    home_en = getattr(context.en, 'start-1-en').homepage

    api.content.move(source=home_fr, target=context.fr)
    api.content.move(source=home_nl, target=context.nl)
    api.content.move(source=home_en, target=context.en)

    context.fr.setDefaultPage('homepage')
    context.nl.setDefaultPage('home')
    context.en.setDefaultPage('homepage')


