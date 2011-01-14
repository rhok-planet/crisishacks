from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


from problemdefinition.forms import ElementForm, FeatureForm, ProblemDefinitionForm, ProblemDefinitionHackForm
from problemdefinition.models import Element, Feature, ProblemDefinition, ProblemDefinitionHack
from hack.models import Hack

def problemdefinitions(request, template_name="problemdefinition/problemdefinitions.html"):
    problemdefinitions = ProblemDefinition.objects.all().annotate(problemdefinitionhack_count=Count('problemdefinitionhack'), feature_count=Count('feature'))
    return render_to_response(
        template_name, {
            'problemdefinitions': problemdefinitions,
        }, context_instance = RequestContext(request)
    )

def problemdefinition_detail(request, slug, template_name="problemdefinition/problemdefinition_detail.html"):
    problemdefinition = get_object_or_404(ProblemDefinition, slug=slug)
    features = problemdefinition.feature_set.all()

    gp = problemdefinition.problemdefinitionhack_set.select_related('problemdefinitionhack', 'hack__repo', 'hack__category')
    problemdefinition_hacks = gp.annotate(usage_count=Count('hack__usage')).order_by('-usage_count', 'hack')

    # Get a list of all elements for this problemdefinition, and then hack them into a
    # dictionary so we can easily lookup the element for every
    # feature/problemdefinition_hack combination.
    elements_mapping = {}
    all_elements = Element.objects.all().filter(feature__in=features, problemdefinition_hack__in=problemdefinition_hacks)
    for element in all_elements:
        problemdefinition_mapping = elements_mapping.setdefault(element.feature_id, {})
        problemdefinition_mapping[element.problemdefinition_hack_id] = element

    return render_to_response(
        template_name, {
            'problemdefinition': problemdefinition,
            'features': features,
            'problemdefinition_hacks': problemdefinition_hacks,
            'elements': elements_mapping,
        }, context_instance = RequestContext(request)
    )

@login_required
def add_problemdefinition(request, template_name="problemdefinition/add_problemdefinition.html"):

    new_problemdefinition = ProblemDefinition()
    form = ProblemDefinitionForm(request.POST or None, instance=new_problemdefinition)

    if form.is_valid():
        new_problemdefinition = form.save()
        return HttpResponseRedirect(reverse('problemdefinition', kwargs={'slug':new_problemdefinition.slug}))

    return render_to_response(template_name, {
        'form': form
        },
        context_instance=RequestContext(request))

@login_required
def edit_problemdefinition(request, slug, template_name="problemdefinition/edit_problemdefinition.html"):

    problemdefinition = get_object_or_404(ProblemDefinition, slug=slug)
    form = ProblemDefinitionForm(request.POST or None, instance=problemdefinition)

    if form.is_valid():
        problemdefinition = form.save()
        return HttpResponseRedirect(reverse('problemdefinition', kwargs={'slug': problemdefinition.slug}))

    return render_to_response(template_name, {
        'form': form,
        'problemdefinition': problemdefinition
        },
        context_instance=RequestContext(request))

@login_required
def add_feature(request, problemdefinition_slug, template_name="problemdefinition/add_feature.html"):

    problemdefinition = get_object_or_404(ProblemDefinition, slug=problemdefinition_slug)
    feature = Feature()
    form = FeatureForm(request.POST or None, instance=feature)

    if form.is_valid():
        feature = Feature(
                    problemdefinition=problemdefinition,
                    title=request.POST['title'],
                    description = request.POST['description']
                )
        feature.save()
        return HttpResponseRedirect(reverse('problemdefinition', kwargs={'slug':feature.problemdefinition.slug}))


    return render_to_response(template_name, {
        'form': form,
        'problemdefinition':problemdefinition
        },
        context_instance=RequestContext(request))

@login_required
def edit_feature(request, id, template_name="problemdefinition/edit_feature.html"):

    feature = get_object_or_404(Feature, id=id)
    form = FeatureForm(request.POST or None, instance=feature)

    if form.is_valid():
        feature = form.save()
        return HttpResponseRedirect(reverse('problemdefinition', kwargs={'slug': feature.problemdefinition.slug}))

    return render_to_response(template_name, {
        'form': form,
        'problemdefinition': feature.problemdefinition
        },
        context_instance=RequestContext(request))

@permission_required('problemdefinition.delete_feature')
def delete_feature(request, id, template_name="problemdefinition/edit_feature.html"):

    feature = get_object_or_404(Feature, id=id)
    Element.objects.filter(feature=feature).delete()
    feature.delete()

    return HttpResponseRedirect(reverse('problemdefinition', kwargs={'slug': feature.problemdefinition.slug}))


@permission_required('problemdefinition.delete_problemdefinitionhack')
def delete_problemdefinition_hack(request, id, template_name="problemdefinition/edit_feature.html"):

    hack = get_object_or_404(ProblemDefinitionHack, id=id)
    Element.objects.filter(problemdefinition_hack=hack).delete()
    hack.delete()

    return HttpResponseRedirect(reverse('problemdefinition', kwargs={'slug': hack.problemdefinition.slug}))


@login_required
def edit_element(request, feature_id, hack_id, template_name="problemdefinition/edit_element.html"):

    feature = get_object_or_404(Feature, pk=feature_id)
    problemdefinition_hack = get_object_or_404(ProblemDefinitionHack, pk=hack_id)

    # Sanity check to make sure both the feature and problemdefinition_hack are related to
    # the same problemdefinition!
    if feature.problemdefinition_id != problemdefinition_hack.problemdefinition_id:
        raise Http404

    element, created = Element.objects.get_or_create(
                                    problemdefinition_hack=problemdefinition_hack,
                                    feature=feature
                                    )

    form = ElementForm(request.POST or None, instance=element)

    if form.is_valid():
        element = form.save()
        return HttpResponseRedirect(reverse('problemdefinition', kwargs={'slug': feature.problemdefinition.slug}))

    return render_to_response(template_name, {
        'form': form,
        'feature':feature,
        'hack':problemdefinition_hack.hack,
        'problemdefinition':feature.problemdefinition
        },
        context_instance=RequestContext(request))

@login_required
def add_problemdefinition_hack(request, problemdefinition_slug, template_name="problemdefinition/add_problemdefinition_hack.html"):

    problemdefinition = get_object_or_404(ProblemDefinition, slug=problemdefinition_slug)
    problemdefinition_hack = ProblemDefinitionHack()
    form = ProblemDefinitionHackForm(request.POST or None, instance=problemdefinition_hack)
    message = ''

    if form.is_valid():
        hack = get_object_or_404(Hack, id=request.POST['hack'])
        try:
            ProblemDefinitionHack.objects.get(problemdefinition=problemdefinition, hack=hack)
            message = "Sorry, but '%s' is already in this problemdefinition." % hack.title
        except ProblemDefinitionHack.DoesNotExist:
            hack = ProblemDefinitionHack(
                        problemdefinition=problemdefinition,
                        hack=hack
                    )
            hack.save()
            redirect = request.POST.get('redirect','')
            if redirect:
                return HttpResponseRedirect(redirect)

            return HttpResponseRedirect(reverse('problemdefinition', kwargs={'slug':problemdefinition.slug}))



    return render_to_response(template_name, {
        'form': form,
        'problemdefinition': problemdefinition,
        'message': message
        },
        context_instance=RequestContext(request))


def ajax_problemdefinition_list(request, template_name="problemdefinition/ajax_problemdefinition_list.html"):
    q = request.GET.get('q','')
    problemdefinitions = []
    if q:
        problemdefinitions = ProblemDefinition.objects.filter(title__istartswith=q)
    hack_id = request.GET.get('hack_id','')
    if hack_id:
        problemdefinitions = problemdefinitions.exclude(problemdefinitionhack__hack__id=hack_id)
    return render_to_response(template_name, {
        'problemdefinitions': problemdefinitions
        },
        context_instance=RequestContext(request)
    )
