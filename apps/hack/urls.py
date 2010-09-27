from django.conf.urls.defaults import *
from django.db.models import Count
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.date_based import archive_index
from django.views.generic.simple import direct_to_template

from hack.models import Hack
from hack.views import (
                            add_example, 
                            add_hack, 
                            ajax_hack_list,                             
                            edit_hack, 
                            edit_example, 
                            update_hack,
                            usage
                            )

urlpatterns = patterns("",
    url(
        regex   = r"^$",
        view    = object_list,
        name    = "hacks",
        kwargs  = dict(
            queryset=Hack.objects.annotate(usage_count=Count("usage")).order_by('-pypi_downloads', '-repo_watchers', 'title')
            )            
    ),
    
    url(
        regex   = r"^latest/$",
        view    = archive_index,
        name    = "latest_hacks",
        kwargs  = dict(
            queryset=Hack.objects.select_related(),     
            date_field="created"   
            )            
    ),
    
    
    url(
        regex   = "^add/$",
        view    = add_hack,
        name    = "add_hack",
    ),    

    url(
        regex = "^(?P<slug>[-\w]+)/edit/$",
        view    = edit_hack,
        name    = "edit_hack", 
    ),    
    
    url(
        regex = "^(?P<slug>[-\w]+)/fetch-data/$",
        view    = update_hack,
        name    = "fetch_hack_data", 
    ),    

    url(
        regex = "^(?P<slug>[-\w]+)/example/add/$",
        view    = add_example,
        name    = "add_example", 
    ),    
    
    url(
        regex = "^(?P<slug>[-\w]+)/example/(?P<id>\d+)/edit/$",
        view    = edit_example,
        name    = "edit_example", 
    ),    
    
    url(
        regex = "^p/(?P<slug>[-\w]+)/$",
        view    = object_detail,
        name    = "hack",
        kwargs=dict(
            queryset=Hack.objects.select_related(),
            template_name="hack/hack.html",
            #template_object_name="hack",
            )    
    ),    
    
    url(
        regex = "^ajax_hack_list/$",
        view    = ajax_hack_list,
        name    = "ajax_hack_list",
    ),
    
    url(
        regex = "^usage/(?P<slug>[-\w]+)/(?P<action>add|remove)/$",
        view    = usage,
        name    = "usage",
    ),    
        
)
