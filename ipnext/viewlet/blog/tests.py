import unittest2 as unittest

import transaction

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing.z2 import Browser

from Products.CMFCore.utils import getToolByName

from ipnext.viewlet.blog.testing import \
        BlogViewletTestingLayer_INTEGRATION_TESTING

class TestSetup(unittest.TestCase):

    layer = BlogViewletTestingLayer_INTEGRATION_TESTING

    def test__verify_installation(self):
        """Check if installed"""
        portal = self.layer['portal']
        tool = getToolByName(portal, 'portal_quickinstaller')
        self.assertTrue(tool.isProductInstalled('ipnext.viewlet.blog'))
