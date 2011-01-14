from django.core.urlresolvers import reverse
from django.core.cache import cache

from homepage.models import Tab, ProblemTab

def problemdefinition_tabs(request):
    cache_key = 'sitewide:problemdefinition_tabs'
    problemdefinition_tabs = cache.get(cache_key)
    if problemdefinition_tabs is None:
        problemdefinition_tabs = ProblemTab.objects.all().select_related('problemdefinition')
        cache.set(cache_key, problemdefinition_tabs, 60 * 5 * 0)
    return {'problemdefinition_tabs': problemdefinition_tabs}

def grid_tabs(request):
    cache_key = 'sitewide:grid_tabs'
    grid_tabs = cache.get(cache_key)
    if grid_tabs is None:
        grid_tabs = Tab.objects.all().select_related('grid')
        cache.set(cache_key, grid_tabs, 60 * 5 * 0)
    return {'grid_tabs': grid_tabs}

def current_path(request):
    """Adds the path of the current page to template context, but only
    if it's not the path to the logout page. This allows us to redirect
    user's back to the page they were viewing before they logged in,
    while making sure we never redirect them back to the logout page!

    """
    context = {}
    if request.path not in (reverse('acct_logout'), reverse('acct_signup')):
        context['current_path'] = request.path
    return context
