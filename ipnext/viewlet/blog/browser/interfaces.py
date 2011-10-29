from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager

import zope.interface

class IIPnextBlogViewletLayer(zope.interface.Interface):
    """A layer specific for this add-on product.

    This interface is referred in browserlayers.xml.

    All views and viewlets register against this layer will appear on your Plone site
    only when the add-on installer has been run.
    """

class IBlogViewletManager(IViewletManager):
    """A container for the blog post viewlet"""