from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User 
from django.core.urlresolvers import reverse 
from django.http import HttpResponseRedirect, Http404 
from django.shortcuts import render_to_response, get_object_or_404 
from django.template import RequestContext 


from grid.forms import ElementForm, FeatureForm, GridForm, GridHackForm
from grid.models import Element, Feature, Grid, GridHack
from hack.models import Hack

def grids(request, template_name="grid/grids.html"):
    grids = Grid.objects.all().annotate(gridhack_count=Count('gridhack'), feature_count=Count('feature'))
    return render_to_response(
        template_name, {
            'grids': grids,
        }, context_instance = RequestContext(request)
    )

def grid_detail(request, slug, template_name="grid/grid_detail.html"):
    grid = get_object_or_404(Grid, slug=slug)
    features = grid.feature_set.all()
    
    gp = grid.gridhack_set.select_related('gridhack', 'hack__repo', 'hack__category')
    grid_hacks = gp.annotate(usage_count=Count('hack__usage')).order_by('-usage_count', 'hack')
    
    # Get a list of all elements for this grid, and then hack them into a
    # dictionary so we can easily lookup the element for every
    # feature/grid_hack combination.
    elements_mapping = {}
    all_elements = Element.objects.all().filter(feature__in=features, grid_hack__in=grid_hacks)
    for element in all_elements:
        grid_mapping = elements_mapping.setdefault(element.feature_id, {})
        grid_mapping[element.grid_hack_id] = element
    
    return render_to_response(
        template_name, {
            'grid': grid,
            'features': features,
            'grid_hacks': grid_hacks,
            'elements': elements_mapping,
        }, context_instance = RequestContext(request)
    )
        
@login_required
def add_grid(request, template_name="grid/add_grid.html"):

    new_grid = Grid()
    form = GridForm(request.POST or None, instance=new_grid)    

    if form.is_valid(): 
        new_grid = form.save()
        return HttpResponseRedirect(reverse('grid', kwargs={'slug':new_grid.slug}))

    return render_to_response(template_name, { 
        'form': form
        },
        context_instance=RequestContext(request))
        
@login_required
def edit_grid(request, slug, template_name="grid/edit_grid.html"):

    grid = get_object_or_404(Grid, slug=slug)
    form = GridForm(request.POST or None, instance=grid)

    if form.is_valid():
        grid = form.save()
        return HttpResponseRedirect(reverse('grid', kwargs={'slug': grid.slug}))

    return render_to_response(template_name, { 
        'form': form,  
        'grid': grid
        }, 
        context_instance=RequestContext(request))  
        
@login_required
def add_feature(request, grid_slug, template_name="grid/add_feature.html"):

    grid = get_object_or_404(Grid, slug=grid_slug)
    feature = Feature()
    form = FeatureForm(request.POST or None, instance=feature)    

    if form.is_valid(): 
        feature = Feature(
                    grid=grid, 
                    title=request.POST['title'],
                    description = request.POST['description']
                )
        feature.save()
        return HttpResponseRedirect(reverse('grid', kwargs={'slug':feature.grid.slug}))


    return render_to_response(template_name, { 
        'form': form,
        'grid':grid
        },
        context_instance=RequestContext(request))           
        
@login_required
def edit_feature(request, id, template_name="grid/edit_feature.html"):

    feature = get_object_or_404(Feature, id=id)
    form = FeatureForm(request.POST or None, instance=feature)

    if form.is_valid():
        feature = form.save()
        return HttpResponseRedirect(reverse('grid', kwargs={'slug': feature.grid.slug}))

    return render_to_response(template_name, { 
        'form': form,
        'grid': feature.grid  
        }, 
        context_instance=RequestContext(request))
        
@permission_required('grid.delete_feature')
def delete_feature(request, id, template_name="grid/edit_feature.html"):

    feature = get_object_or_404(Feature, id=id)
    Element.objects.filter(feature=feature).delete()
    feature.delete()

    return HttpResponseRedirect(reverse('grid', kwargs={'slug': feature.grid.slug}))


@permission_required('grid.delete_gridhack')
def delete_grid_hack(request, id, template_name="grid/edit_feature.html"):

    hack = get_object_or_404(GridHack, id=id)
    Element.objects.filter(grid_hack=hack).delete()
    hack.delete()

    return HttpResponseRedirect(reverse('grid', kwargs={'slug': hack.grid.slug}))

        
@login_required
def edit_element(request, feature_id, hack_id, template_name="grid/edit_element.html"):
    
    feature = get_object_or_404(Feature, pk=feature_id)
    grid_hack = get_object_or_404(GridHack, pk=hack_id)    
    
    # Sanity check to make sure both the feature and grid_hack are related to
    # the same grid!
    if feature.grid_id != grid_hack.grid_id:
        raise Http404
    
    element, created = Element.objects.get_or_create(
                                    grid_hack=grid_hack,
                                    feature=feature
                                    )    
        
    form = ElementForm(request.POST or None, instance=element)

    if form.is_valid():
        element = form.save()
        return HttpResponseRedirect(reverse('grid', kwargs={'slug': feature.grid.slug}))

    return render_to_response(template_name, { 
        'form': form,
        'feature':feature,
        'hack':grid_hack.hack,
        'grid':feature.grid
        }, 
        context_instance=RequestContext(request))        

@login_required
def add_grid_hack(request, grid_slug, template_name="grid/add_grid_hack.html"):

    grid = get_object_or_404(Grid, slug=grid_slug)
    grid_hack = GridHack()
    form = GridHackForm(request.POST or None, instance=grid_hack)    
    message = ''

    if form.is_valid(): 
        hack = get_object_or_404(Hack, id=request.POST['hack'])    
        try:
            GridHack.objects.get(grid=grid, hack=hack)
            message = "Sorry, but '%s' is already in this grid." % hack.title
        except GridHack.DoesNotExist:
            hack = GridHack(
                        grid=grid, 
                        hack=hack
                    )
            hack.save()
            redirect = request.POST.get('redirect','')
            if redirect:
                return HttpResponseRedirect(redirect)
            
            return HttpResponseRedirect(reverse('grid', kwargs={'slug':grid.slug}))
    


    return render_to_response(template_name, { 
        'form': form,
        'grid': grid,
        'message': message
        },
        context_instance=RequestContext(request))
        

def ajax_grid_list(request, template_name="grid/ajax_grid_list.html"):
    q = request.GET.get('q','')
    grids = []
    if q:
        grids = Grid.objects.filter(title__istartswith=q)
    hack_id = request.GET.get('hack_id','')
    if hack_id:
        grids = grids.exclude(gridhack__hack__id=hack_id)
    return render_to_response(template_name, {
        'grids': grids
        },
        context_instance=RequestContext(request)
    )