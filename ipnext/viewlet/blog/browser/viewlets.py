from zope.component import getMultiAdapter
from zope.component import queryUtility 

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry 

from ipnext.viewlet.blog.browser.controllers import PortalBlogQuery
from ipnext.viewlet.blog.interfaces import IIPnextViewletBlogSettings

class RelevantBlogViewlet(ViewletBase):
    """
    Renders a pretty box with the latest relevant post on a WP blog
    """
    index = ViewPageTemplateFile('templates/blog_viewlet.pt')
    
    def render(self):
        """
        """
        super(RelevantBlogViewlet, self).update() 
        self.controller = PortalBlogQuery(self.context)
        
        return self.index()
    
    @property
    def is_enabled_content(self):
        """
        Check if we are rendering in a View of a "Blog viewlet" enabled content
        
        This is controlled in the Content settings
        """
        return True # TODO
        ## Provide functionality to selectively disable blog viewlets
        ## for specific content objects.
        ## Already implemented in our website; it will be added 
        ## here at a later time.
        #try:
        #    status = self.context.blog_post_display
        #except AttributeError, e:
        #    # Ignore types that are not aware of this product
        #    # and don't have this field set (extended) in their schema
        #    return False
        #
        #return status
        
    @property
    def is_enabled_type(self):
        """
        Check if we are rendering in a View of a "Blog viewlet" enabled type
        
        This is controlled in the Plone Control Panel
        """
        registry = queryUtility(IRegistry) 
        if registry is None: 
            # Don't show if the registry is not found
            return False
        settings = registry.forInterface(IIPnextViewletBlogSettings, 
                                         check=False) 
        _types = getattr(settings, 'allowed_types', '')
        this_type = self.context.Type()
        
        return this_type in _types
        
    def view_blog(self):
        """
        Check if the author wants to display a blog post here.
        """
    
    def obj_categories(self):
        """
        Return the categories tagged to the context object
        """
        return self.context.Subject()
    
    def post_contents(self):
        """
        Query the catalog for the first relevant post, return None if not found.
        """
        tags = self.context.Subject()
        contents = self.controller.get_relevant_post(tags)
        if not contents:
            return None
        
        # Localize time
        localize_time = self.context.toLocalizedTime
        contents['effective_date'] = localize_time(contents['effective_date'])
        return contents