from random import choice

from zope.component import queryUtility 

from Products.CMFPlone.utils import getToolByName
from plone.registry.interfaces import IRegistry 

from ipnext.viewlet.blog.interfaces import IIPnextViewletBlogSettings

# If something goes wrong with Registry, just set a standard max chars
DEFAULT_MAX_CHARS = 500

def getPublicMemberPortrait(member):
    """
    Fetch the portrait for a member.
    """
    return member.getPersonalPortrait(id=member.id)

def excerptize(text, max_chars):
    """
    Return a brief excerpt from a string of plain text.
    """
    cont_snip = '...'
    words = text[:max_chars].split(' ')[:-1]
    return ' '.join(words + [' ', cont_snip])
    

class PortalBlogQuery(object):
    
    def __init__(self, context):
        self.context = context
        registry = queryUtility(IRegistry)
        maxchars = DEFAULT_MAX_CHARS
        if registry:
            settings = registry.forInterface(
                IIPnextViewletBlogSettings, check=False)
            maxchars = getattr(settings, 'description_maxchars',
                               DEFAULT_MAX_CHARS)
        self.maxchars = maxchars

    def html_to_text(self, data):
        """
        Convert HTML formatted data to plain text.
        """
        ptrans = getToolByName(self, 'portal_transforms')
        transformed = ptrans.convertTo(
            'text/plain', data,
            mimetype='text/-x-web-intelligent'
        )
        return transformed.getData()
    
    def get_author_image_url(self, member):
        """
        Fetch the author avatar image url accoding to name.
        """
        if member:
            img_url = getPublicMemberPortrait(member).absolute_url()
        else:
            img_url = '/'.join((self.context.absolute_url(), mtool.default_portrait))
        return img_url
        
    def get_relevant_post(self, tags):
        """
        Query the catalog and retrieve a relevant post (News Item).
        """
        # Build the query to the catalog
        catalog = getToolByName(self.context, 'portal_catalog')
        relevant_posts = catalog(
            portal_type='News Item',
            Subject=tags,
        )
        
        # Return a random relevant post
        if relevant_posts:
            post = choice(relevant_posts)
            #import pdb; pdb.set_trace()
            author_id = post.Creator
            post_description = post.Description
            
            mtool = getToolByName(self.context, 'portal_membership')
            member = mtool.getMemberById(author_id)
            
            author_info = mtool.getMemberInfo(member.id)
            author_name = author_info.get('fullname', author_id)
            author_home_url = author_info.get('home_page', None)
            author_img_url = self.get_author_image_url(member)
            
            # If the post doesn't have a description, generate one
            # using the content text.
            if post_description == '':
                obj = post.getObject()
                html_txt = obj.getText()
                post_description = self.html_to_text(html_txt)
            
            # Build the post data slug
            post_data = {
                'title': post.Title,
                'author_name': author_name if author_name else author_id, 
                'author_home_url': author_home_url,
                'description': excerptize(post_description, self.maxchars),
                'document_url': post.getURL(),
                'portrait_url': author_img_url,
                'effective_date': post.effective,
            }
            
            # Return the slug to the view
            return post_data
