from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _ 

from hack.models import BaseModel, Hack


class Grid(BaseModel):

    title        = models.CharField(_('Title'), max_length=100)
    slug         = models.SlugField(_('Slug'), help_text="Slugs will be lowercased", unique=True)    
    description  = models.TextField(_('Description'), blank=True, help_text="Lines are broken and urls are urlized")
    is_locked    = models.BooleanField(_('Is Locked'), default=False, help_text="Moderators can lock grid access")
    hacks     = models.ManyToManyField(Hack, through="GridHack")
    
    def elements(self):
        elements = []
        for feature in self.feature_set.all(): 
            for element in feature.element_set.all(): 
                elements.append(element)
        return elements
                    
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("grid", [self.slug])
        
    class Meta:
        ordering = ['title']

class GridHack(BaseModel):
    """ These are Hacks on one side of the grid 
        Have to make this intermediary table to get things to work right
        Otherwise would have used ManyToMany field
    """
    
    grid        = models.ForeignKey(Grid)
    hack     = models.ForeignKey(Hack)
    
    class Meta:
        verbose_name = 'Grid Hack'
        verbose_name_plural = 'Grid Hacks'        
        
    def __unicode__(self):
        return '%s : %s' % (self.grid.slug, self.hack.slug)
    
class Feature(BaseModel):
    """ These are the features measured against a grid """
    
    grid         = models.ForeignKey(Grid)
    title        = models.CharField(_('Title'), max_length=100)
    description  = models.TextField(_('Description'), blank=True)
    
    def __unicode__(self):
        return '%s : %s' % (self.grid.slug, self.title)    
    
help_text = """
Linebreaks are turned into 'br' tags<br />
Urls are turned into links<br />
You can use just 'check', 'yes', 'good' to place a checkmark icon.<br />
You can use 'bad', 'negative', 'evil', 'sucks', 'no' to place a negative icon.<br />
Plus just '+' or '-' signs can be used but cap at 3 multiples to protect layout<br/>

"""
    
class Element(BaseModel):
    """ The individual table elements """
    
    grid_hack = models.ForeignKey(GridHack)
    feature      = models.ForeignKey(Feature)
    text         = models.TextField(_('text'), blank=True, help_text=help_text)
    
    class Meta:
        
        ordering = ["-id"]
    
    def __unicode__(self):
        return '%s : %s : %s' % (self.grid_hack.grid.slug, self.grid_hack.hack.slug, self.feature.title)
    
    
