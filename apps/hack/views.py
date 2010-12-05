from random import randrange
import simplejson
import urllib

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.conf import settings
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string


from hack.forms import HackForm, DeploymentForm
from hack.models import Category, Hack, Deployment, Repo

def repos_for_js():
    repos = {}
    for repo in Repo.objects.all():
        repos[repo.url] = repo.id
    return simplejson.dumps(repos)

@login_required
def add_hack(request, template_name="hack/hack_form.html"):

    new_hack = Hack()
    form = HackForm(request.POST or None, instance=new_hack)

    if form.is_valid():
        new_hack = form.save()
        new_hack.created_by = request.user
        new_hack.last_modified_by = request.user
        new_hack.save()
        new_hack.fetch_metadata()
        return HttpResponseRedirect(reverse("hack", kwargs={"slug":new_hack.slug}))

    return render_to_response(template_name, {
        "form": form,
        "repos": repos_for_js(),
        "action": "add",
        },
        context_instance=RequestContext(request))

@login_required
def edit_hack(request, slug, template_name="hack/hack_form.html"):

    hack = get_object_or_404(Hack, slug=slug)
    form = HackForm(request.POST or None, instance=hack)

    if form.is_valid():
        modified_hack = form.save()
        modified_hack.last_modified_by = request.user
        modified_hack.save()

        return HttpResponseRedirect(reverse("hack", kwargs={"slug": modified_hack.slug}))

    return render_to_response(template_name, {
        "form": form,
        "hack": hack,
        "repos": repos_for_js(),
        "action": "edit",
        },
        context_instance=RequestContext(request))

@login_required
def update_hack(request, slug):

    hack = get_object_or_404(Hack, slug=slug)
    hack.fetch_metadata()

    return HttpResponseRedirect(reverse("hack", kwargs={"slug": hack.slug}))



def add_deployment(request, slug, template_name="hack/add_deployment.html"):

    hack = get_object_or_404(Hack, slug=slug)
    new_hack_example = Deployment()
    form = DeploymentForm(request.POST or None, instance=new_hack_example)
    
    if form.is_valid() and request.POST:
        hack_example = Deployment(hack=hack,
                title=form.cleaned_data["title"],
                url=form.cleaned_data["url"],
                location=form.cleaned_data["location"],
                description=form.cleaned_data["description"],
                number_users=form.cleaned_data["number_users"],
                created_by=request.user)
        hack_example.save()
        return HttpResponseRedirect(reverse("hack", kwargs={"slug":hack_example.hack.slug}))

    return render_to_response(template_name, {
        "form": form,
        "hack":hack
        },
        context_instance=RequestContext(request))


def edit_example(request, slug, id, template_name="hack/edit_example.html"):

    hack_example = get_object_or_404(Deployment, id=id)
    form = DeploymentForm(request.POST or None, instance=hack_example)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("hack", kwargs={"slug": hack_example.hack.slug}))

    return render_to_response(template_name, {
        "form": form,
        "hack":hack_example.hack
        },
        context_instance=RequestContext(request))


def hack_autocomplete(request):
    """
    Provides Hack matching based on matches of the beginning
    """
    titles = []
    q = request.GET.get("q", "")
    if q:
        titles = (x.title for x in Hack.objects.filter(title__istartswith=q))

    response = HttpResponse("\n".join(titles))

    setattr(response, "djangologging.suppress_output", True)
    return response

def category(request, slug, template_name="hack/category.html"):
    category = get_object_or_404(Category, slug=slug)
    hacks = category.hack_set.annotate(usage_count=Count("usage")).order_by("-repo_watchers", "title")
    return render_to_response(template_name, {
        "category": category,
        "hacks": hacks,
        },
        context_instance=RequestContext(request)
    )

def ajax_hack_list(request, template_name="hack/ajax_hack_list.html"):
    q = request.GET.get("q","")
    hacks = []
    if q:
        django_dash = "django-%s" % q
        django_space = "django %s" % q
        hacks = Hack.objects.filter(
                        Q(title__istartswith=q) |
                        Q(title__istartswith=django_dash) |
                        Q(title__istartswith=django_space)
                    )
    return render_to_response(template_name, {
        "hacks": hacks
        },
        context_instance=RequestContext(request)
    )

def usage(request, slug, action):
    success = False
    # Check if the user is authenticated, redirecting them to the login page if
    # they're not.
    if not request.user.is_authenticated():
        url = settings.LOGIN_URL + '?next=%s' % reverse('usage', args=(slug, action))
        url += urllib.quote_plus('?next=/%s' % request.META['HTTP_REFERER'].split('/', 3)[-1])
        if request.is_ajax():
            response = {}
            response['success'] = success
            response['redirect'] = url
            return HttpResponse(simplejson.dumps(response))
        return HttpResponseRedirect(url)

    hack = get_object_or_404(Hack, slug=slug)

    # Update the current user's usage of the given hack as specified by the
    # request.
    if hack.usage.filter(username=request.user.username):
        if action.lower() == 'remove':
            hack.usage.remove(request.user)
            success = True
            template_name = 'hack/add_usage_button.html'
            change = -1
    else:
        if action.lower() == 'add':
            hack.usage.add(request.user)
            success = True
            template_name = 'hack/remove_usage_button.html'
            change = 1

    # Invalidate the cache of this users's used_hacks_list.
    if success:
        cache_key = "sitewide:used_hacks_list:%s" % request.user.pk
        cache.delete(cache_key)

    # Return an ajax-appropriate response if necessary
    if request.is_ajax():
        response = {'success': success}
        if success:
            response['change'] = change
            response['body'] = render_to_string(
                template_name,
                {"hack": hack},
            )
        return HttpResponse(simplejson.dumps(response))

    # Intelligently determine the URL to redirect the user to based on the
    # available information.
    next = request.GET.get('next') or request.META.get("HTTP_REFERER") or reverse("hack", kwargs={"slug": hack.slug})
    return HttpResponseRedirect(next)

def packaginate(request):
    """ Special project method - DO NOT TOUCH!!! """

    hacks = Hack.objects.all()
    hack = hacks[randrange(0, hacks.count())]
    response = dict(
            title = hack.title,
            url = hack.get_absolute_url(),
            description=hack.repo_description
        )
    return HttpResponse(simplejson.dumps(response))
