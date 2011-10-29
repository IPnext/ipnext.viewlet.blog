from zope import schema
from zope.interface import Interface

from ipnext.viewlet.blog import _

DEFAULT_ENABLED_TYPES = [u'Page', u'Plone Site']

class IIPnextViewletBlogSettings(Interface): 
    """Describes registry records 
    """ 
    allowed_types = schema.List( 
          title=_(u"Content types that display blog posts"), 
          description=_(u"A list of content types that should display" + 
                        u" a relevant blog post in a viewlet."), 
          value_type=schema.TextLine(), 
          default=DEFAULT_ENABLED_TYPES,
          ) 
    
    description_maxchars = schema.Int( 
          title=_(u"Maximum characters to display"), 
          description=_(u"The maximum number of characters to display" + 
                        u" in the blog excerpt."), 
          default=500,
          )
