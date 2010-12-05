from django.core.cache import cache

def used_hacks_list(request):
    context = {}
    if request.user.is_authenticated():
        cache_key = "sitewide:used_hacks_list:%s" % request.user.pk
        used_hacks_list = cache.get(cache_key)
        if used_hacks_list is None:
            used_hacks_list = request.user.hack_set.values_list("pk", flat=True)
            cache.set(cache_key, used_hacks_list, 60 * 60 * 24 * 0)
        context['used_hacks_list'] = used_hacks_list
    return context
