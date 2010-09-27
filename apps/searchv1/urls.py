from django.conf.urls.defaults import *

from searchv1.views import search, find_grids_autocomplete, find_hacks_autocomplete, search_by_function_autocomplete

urlpatterns = patterns("",
    
    url(
        regex   = '^$',
        view    = search,
        name    = 'search',
    ),    
    url(
        regex   = '^grids/autocomplete/$',
        view    = search_by_function_autocomplete,
        name    = 'search_grids_autocomplete',
        kwargs  = dict(
            search_function=find_grids_autocomplete,        
            )        
        
    ),    
    url(
        regex   = '^hacks/autocomplete/$',
        view    = search_by_function_autocomplete,
        name    = 'search_hacks_autocomplete',
        kwargs  = dict(
            search_function=find_hacks_autocomplete,        
            )        

    ),    
    
)
