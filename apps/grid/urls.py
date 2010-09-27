from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_index

from grid.models import Grid

from grid.views import (
        add_feature,
        add_grid,
        add_grid_hack,
        ajax_grid_list,
        delete_feature,
        delete_grid_hack,
        edit_element,
        edit_grid,
        edit_feature,
        grid_detail, 
        grids
    )

urlpatterns = patterns("",

    
    url(
        regex = '^add/$',
        view    = add_grid,
        name    = 'add_grid',
    ),    
    
    url(
        regex = '^(?P<slug>[-\w]+)/edit/$',
        view    = edit_grid,
        name    = 'edit_grid',
    ),    
    
    url(
        regex = '^g/(?P<slug>[-\w]+)/$',
        view    = grid_detail,
        name    = 'grid',
    ), 
    
    url(
        regex = '^element/(?P<feature_id>\d+)/(?P<hack_id>\d+)/$',
        view    = edit_element,
        name    = 'edit_element',
    ),  
    
    url(
        regex = '^feature/add/(?P<grid_slug>[a-z0-9\-\_]+)/$',
        view    = add_feature,
        name    = 'add_feature',
    ),         
    
    url(
        regex = '^feature/(?P<id>\d+)/$',
        view    = edit_feature,
        name    = 'edit_feature',
    ), 
    
    url(
        regex = '^feature/(?P<id>\d+)/delete/$',
        view    = delete_feature,
        name    = 'delete_feature',
    ),       

    url(
        regex = '^hack/(?P<id>\d+)/delete/$',
        view    = delete_grid_hack,
        name    = 'delete_grid_hack',
    ),       

    url(
        regex = '^(?P<grid_slug>[a-z0-9\-\_]+)/hack/add/$',
        view    = add_grid_hack,
        name    = 'add_grid_hack',
    ),       

    url(
        regex = '^ajax_grid_list/$',
        view    = ajax_grid_list,
        name    = 'ajax_grid_list',
    ),    

    url(
        regex   = r"^latest/$",
        view    = archive_index,
        name    = "latest_grids",
        kwargs  = dict(
            queryset=Grid.objects.select_related(),     
            date_field='created'   
            )            
    ),

    url(
        regex = '^$',
        view    = grids,
        name    = 'grids',
    ),    
    
    
    
)
