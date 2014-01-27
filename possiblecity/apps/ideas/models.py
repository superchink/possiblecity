# ideas/models.py

import datetime, os

from markdown import markdown

from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import permalink
from django.db.models.signals import post_save
from django.utils.text import slugify

from actstream import action
from actstream.models import followers
from notification import models as notification
from positions.fields import PositionField
from taggit.managers import TaggableManager
from model_utils.managers import PassThroughManager

from apps.lotxlot.models import Lot

from .managers import IdeaQuerySet
from .signals import idea_created, idea_updated

class Idea(models.Model):
    """
       Defines an idea, which consists minimally of 
       a one sentence description (tagline). In addition,
       it may have plans, images, drawings and detailed 
       descriptions of an urban intervention. 
       Users upload ideas which can then be networked with
       other users, other ideas, or locations within the city.
    """

    objects = PassThroughManager.for_queryset_class(IdeaQuerySet)()

    STATUS_PENDING = 1
    STATUS_PUBLISHED = 2
    STATUS_REJECTED = 3
    STATUS_HIDDEN = 4
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_HIDDEN, 'Hidden'),
    )

    VIA_WEB = 1
    VIA_TEXT = 2
    VIA_TWITTER = 3
    VIA_INSTAGRAM = 4
    VIA_CHOICES = (
        (VIA_WEB, 'Web'),
        (VIA_TEXT, 'Text'),
        (VIA_TWITTER, 'Twitter'),
        (VIA_INSTAGRAM, 'Instagram'),
    )

    # Idea owner manages these fields
    title = models.CharField(max_length=100, blank=True)
    hashtag = models.CharField(max_length=40, blank=True)
    tagline = models.CharField(max_length=140,
         help_text="A tweet-length summary of the project.")
    description = models.TextField(blank=True)
    video = models.URLField(blank=True,
        help_text="The url of a YouTube or Vimeo video for this project.")
    website = models.URLField(blank=True,
          help_text="The website or Facebook Page for this project.")

    lots = models.ManyToManyField(Lot, blank=True, null=True, related_name="ideas")

    # Categorization
    tags = TaggableManager(blank=True)
    
    # Site admin manages these fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, help_text="The owner of the idea.", blank=True, null=True)
    via = models.IntegerField(choices=VIA_CHOICES, default=VIA_WEB)
    slug = models.SlugField(unique=True, editable=True)
    status = models.IntegerField(choices=STATUS_CHOICES, 
        default=STATUS_PUBLISHED,
        help_text="Only ideas with published status \
            will be publicly displayed.")
    enable_comments = models.BooleanField(default=True)
    moderate_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    grounded = models.DateField("date grounded", blank=True, null=True)
    floated = models.DateField("date floated", 
        blank=True, null=True)

    # autogenerated fields
    description_html = models.TextField(blank=True,editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-created']    

    def render_markup(self):
        """Turns  markup into HTML"""
        original = self.description_html
        self.description_html = markdown(self.description)
        return self.description_html != original

    def get_lead_image(self):
        if self.ideavisual_set:
            if self.ideavisual_set.filter(lead=True):
                return self.ideavisual_set.filter(lead=True)[0]
            elif self.ideavisual_set.all():
                return self.ideavisual_set.all()[0]
        return None

    def save(self, *args, **kwargs):
        self.render_markup()
        if not self.floated:
             if self.status == self.STATUS_PUBLISHED:
                self.floated = datetime.date.today()

        if not self.pk:
            if self.title:
                s = '%s: %s' % (self.title, self.tagline)
                slug = s[:50]
            else:
                slug = '%s' % (self.tagline[:50])
            self.slug = slugify(slug)

        super(Idea, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.title:
            return u'%s' % (self.title)
        else:
            return u'%s' % (self.tagline)
       
    @permalink
    def get_absolute_url(self):
        return ('ideas_idea_detail', [str(self.slug)])    

class IdeaVisual(models.Model):
    """
        An image used to help describe an idea.
    """
    def get_upload_path(instance, filename):        
        return os.path.join('ideas', str(instance.idea.id), 'images', filename)

    file = models.ImageField(upload_to = get_upload_path)   
    title = models.CharField(max_length=100, blank=True)
    caption = models.CharField(max_length=140, blank=True)

    # relations
    idea = models.ForeignKey(Idea)
    
    # metadata
    order = PositionField(collection='idea', default=0)
    public = models.BooleanField(default=True)    
    lead = models.BooleanField(default=False)

    # autogenerated fields
    added = models.DateField(auto_now_add=True, editable=False)
    modified = models.DateField(auto_now=True, editable=False)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __unicode__(self):
        if self.title:
            return u'%s' % self.title
        else:
            return u'%s' % self.filename 

    def save(self, *args, **kwargs):
        if self.lead:
            related_images = self._default_manager.filter(idea=self.idea)
            related_images.update(lead=False)
                
        return super(IdeaVisual, self).save(*args, **kwargs)


class IdeaFile(models.Model):
    """
    A file related to a project
    """
    def get_upload_path(instance, filename):        
        return os.path.join('ideas', str(instance.idea.id), 'files', filename)

    file = models.ImageField(upload_to = get_upload_path)
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)

    # relations
    idea = models.ForeignKey(Idea)

    # autogenerated fields
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __unicode__(self):
        if self.title:
            return u'%s' % self.title
        else:
            return u'%s' % self.filename


def idea_created_action(sender, idea=None, target=None, **kwargs):
    action.send(idea.user, verb=u'created the project', target=idea)

def idea_updated_action(sender, idea=None, target=None, **kwargs):
    action.send(idea.user, verb=u'updated the project', target=idea)
    notify_list = followers(idea)
    notify_list.append(idea.user)
    notification.send(notify_list, "project_update", { "target": idea, "initiator": idea.user })

idea_created.connect(idea_created_action)
idea_updated.connect(idea_updated_action)

