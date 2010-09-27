import simplejson

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 

from grid.models import Grid
from hack.models import Hack

from searchv1.forms import SearchForm

def find_hacks_autocomplete(q):
    django_dash = 'django-%s' % q
    django_space = 'django %s' % q    
    return Hack.objects.filter(
                Q(title__istartswith=q) | 
                Q(title__istartswith=django_dash) |
                Q(title__istartswith=django_space))[:15]

def find_grids_autocomplete(q):
    return Grid.objects.filter(title__istartswith=q)[:15]

def search_by_function_autocomplete(request, search_function):
    """
    Searches in Grids and Hacks
    """
    q = request.GET.get('term', '')
    form = SearchForm(request.GET or None)  
    if q:
        objects    = search_function(q)
        objects    = objects.values_list('title', flat=True)    
        json_response = simplejson.dumps(list(objects))
    else:
        json_response = simplejson.dumps([])

    return HttpResponse(json_response, mimetype='text/javascript')

def search(request, template_name='searchv1/search.html'):
    """
    Searches in Grids and Hacks
    """
    grids = []
    hacks = []
    q = request.GET.get('q', '')
    if q:
        django_dash = 'django-%s' % q
        django_space = 'django %s' % q                
        hacks = Hack.objects.filter(
                    Q(title__icontains=q) | 
                    Q(title__istartswith=django_dash) |
                    Q(title__istartswith=django_space) |                    
                    Q(repo_description__icontains=q))        
        grids    = Grid.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
        
    form = SearchForm(request.GET or None)
        
    return render_to_response(template_name, {
        'grids': grids,
        'hacks': hacks,
        'form':form
        },
        context_instance=RequestContext(request)
    )