from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from hack.models import Category, Hack
from homepage.models import Dpotw, Gotw, Tab

def homepage(request, template_name="homepage.html"):

    categories = []
    for category in Category.objects.annotate(hack_count=Count("hack")):
        element = {
            "title":category.title,
            "description":category.description,
            "count": category.hack_count,
            "slug": category.slug,
            "title_plural": category.title_plural,
            "hacks": category.hack_set.annotate(usage_count=Count("usage")).order_by("-repo_watchers", "title")[:9]
        }
        categories.append(element)

    return render_to_response(template_name, {
        "categories": categories,
        "dpotw": Dpotw.objects.get_current(),
        "gotw": Gotw.objects.get_current(),
        "tab": Tab.objects.all()
        },
        context_instance=RequestContext(request)
        )
