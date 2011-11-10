from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from plone.testing import z2

from zope.configuration import xmlconfig

class BlogViewletTestingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ipnext.viewlet.blog
        xmlconfig.file('configure.zcml',
            ipnext.viewlet.blog,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ipnext.viewlet.blog:default')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'ipnext.viewlet.blog')


BlogViewletTestingLayer_FIXTURE = BlogViewletTestingLayer()
BlogViewletTestingLayer_INTEGRATION_TESTING = IntegrationTesting(
    bases=(BlogViewletTestingLayer_FIXTURE,),
    name="BlogViewletTestingLayer:Integration",
)
