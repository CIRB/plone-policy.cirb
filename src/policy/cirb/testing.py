from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class PolicyCirb(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import policy.cirb
        xmlconfig.file('configure.zcml',
                       policy.cirb,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'policy.cirb:default')

POLICY_CIRB_FIXTURE = PolicyCirb()
POLICY_CIRB_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(POLICY_CIRB_FIXTURE, ),
                       name="PolicyCirb:Integration")