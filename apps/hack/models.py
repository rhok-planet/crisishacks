# TODO - cleanup regex to do proper string subs
# TODO - add is_other field to repo
# TODO - add repo.user_url

import logging
import os
import re
import sys
from urllib import urlopen

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from github2.client import Github

from hack.handlers import github
from hack.fields import CreationDateTimeField, ModificationDateTimeField
from hack.utils import uniquer


class BaseModel(models.Model):
    """ Base abstract base class to give creation and modified times """
    created     = CreationDateTimeField(_('created'))
    modified    = ModificationDateTimeField(_('modified'))

    class Meta:
        abstract = True

class Category(BaseModel):

    title = models.CharField(_("Title"), max_length="50")
    slug  = models.SlugField(_("slug"))
    description = models.TextField(_("description"), blank=True)
    title_plural = models.CharField(_("Title Plural"), max_length="50", blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title

REPO_CHOICES = (
    ("hack.handlers.unsupported", "Unsupported"),
    ("hack.handlers.bitbucket", "Bitbucket"),
    ("hack.handlers.github", "Github")
)

class Repo(BaseModel):

    is_supported = models.BooleanField(_("Supported?"), help_text="Does Django Hacks support this repo site?", default=False)
    title        = models.CharField(_("Title"), max_length="50")
    description  = models.TextField(_("description"), blank=True)
    url          = models.URLField(_("base URL of repo"))
    is_other     = models.BooleanField(_("Is Other?"), default=False, help_text="Only one can be set this way")
    user_regex   = models.CharField(_("User Regex"), help_text="Regex to calculate user's name or id",max_length="100", blank=True)
    repo_regex   = models.CharField(_("Repo Regex"), help_text="Regex to get repo's name", max_length="100", blank=True)
    slug_regex   = models.CharField(_("Slug Regex"), help_text="Regex to get repo's slug", max_length="100", blank=True)
    url_regex    = models.CharField(_("Url Regex"), help_text="Regex to identify a repo's url", max_length="100", blank=True)
    handler      = models.CharField(_("Handler"),
        help_text="Warning: Don't change this unless you know what you are doing!",
        choices=REPO_CHOICES,
        max_length="200",
        default="hack.handlers.unsupported")

    class Meta:
        ordering = ['-is_supported', 'title']

    def __unicode__(self):
        if not self.is_supported:
            return '%s (unsupported)' % self.title

        return self.title

downloads_re = re.compile(r'<td style="text-align: right;">[0-9]{1,}</td>')

repo_url_help_text = "Enter your project repo hosting URL here.<br />Example: http://github.com/rhok-planet/crisishacks"
category_help_text = ""

class Hack(BaseModel):

    title           = models.CharField(_("Title"), max_length="100")
    slug            = models.SlugField(_("Slug"), help_text="Slugs will be lowercased", unique=True)
    description     = models.SlugField(_("Slug"), help_text="Slugs will be lowercased")
    category        = models.ForeignKey(Category, verbose_name="Installation", help_text=category_help_text)
    repo            = models.ForeignKey(Repo, null=True)
    repo_description= models.TextField(_("Repo Description"), blank=True)
    repo_url        = models.URLField(_("repo URL"), help_text=repo_url_help_text, blank=True)
    repo_watchers   = models.IntegerField(_("repo watchers"), default=0)
    repo_forks      = models.IntegerField(_("repo forks"), default=0)
    repo_commits    = models.IntegerField(_("repo commits"), default=0)
    related_hacks    = models.ManyToManyField("self", blank=True)
    participants    = models.TextField(_("Participants"),
                        help_text="List of collaborats/participants on the project", blank=True)
    usage           = models.ManyToManyField(User, blank=True)
    created_by = models.ForeignKey(User, blank=True, null=True, related_name="creator")
    last_modified_by = models.ForeignKey(User, blank=True, null=True, related_name="modifier")

    def active_examples(self):
        return self.hackexample_set.filter(active=True)

    def grids(self):

        return (x.grid for x in self.gridhack_set.all())

    def repo_name(self):
        return self.repo_url.replace(self.repo.url + '/','')

    def participant_list(self):

        return self.participants.split(',')

    def fetch_metadata(self, *args, **kwargs):

        # Get the repo watchers number
        base_handler = __import__(self.repo.handler)
        handler = sys.modules[self.repo.handler]

        self = handler.pull(self)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-populate an empty slug field from the Hack title and
        if it conflicts with an existing slug then append a number and try
        saving again.
        """
        if not self.slug:
          self.slug = slugify(self.title)
        while True:
          try:
            super(Hack, self).save(*args, **kwargs)
          # Assuming the IntegrityError is due to a slug fight
          except IntegrityError:
            match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
            if match_obj:
              next_int = int(match_obj.group(2)) + 1
              self.slug = match_obj.group(1) + '-' + str(next_int)
            else:
              self.slug += '-2'
          else:
            break

    @models.permalink
    def get_absolute_url(self):
        return ("hack", [self.slug])


class HackExample(BaseModel):

    hack = models.ForeignKey(Hack)
    title = models.CharField(_("Title"), max_length="100")
    url = models.URLField(_("URL"))
    active = models.BooleanField(_("Active"), default=True, help_text="Moderators have to approve links before they are provided")

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

class Commit(BaseModel):

    hack      = models.ForeignKey(Hack)
    commit_date  = models.DateTimeField(_("Commit Date"))

    class Meta:
        ordering = ['-commit_date']

    def __unicode__(self):
        return "Commit for '%s' on %s" % (self.hack.title, unicode(self.commit_date))

class Version(BaseModel):

    hack = models.ForeignKey(Hack, blank=True, null=True)
    number = models.CharField(_("Version"), max_length="100", default="", blank="")
    downloads = models.IntegerField(_("downloads"), default=0)
    license = models.CharField(_("Version"), max_length="100")
    hidden = models.BooleanField(_("hidden"), default=False)

    class Meta:
        ordering = ['-number']

    def __unicode__(self):
        return "%s: %s" % (self.hack.title, self.number)

class Deployment(BaseModel):
    """Where is this Hack being used"""
    hack = models.ForeignKey(Hack)
    title = models.CharField(_("Title"), max_length="100")
    url = models.URLField(_("URL"), blank=True, null=True)
    location = models.CharField("Location", max_length="50")
    created_by = models.ForeignKey(User, blank=True, null=True)
    description = models.TextField("Description", max_length="500")
    number_users = models.IntegerField("Number Users", blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    bbox = models.CharField(blank=True, null=True, max_length="50")

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title
