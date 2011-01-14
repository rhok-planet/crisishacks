from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer

from homepage.views import homepage
from hack.views import hack_autocomplete, category, packaginate

handler500 = "pinax.views.server_error"


urlpatterns = patterns("",

    url(r"^$", homepage, name="home"),


    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/(.*)", PinaxConsumer()),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r"^hacks/", include("hack.urls")),
    url(r"^grids/", include("grid.urls")),
    url(r"^problemdefinitions/", include("problemdefinition.urls")),
    url(r"^search/", include("searchv1.urls")),
    url(r"^feeds/", include("feeds.urls")),

    url(r"^categories/(?P<slug>[-\w]+)/$", category, name="category"),
    url(r"^categories/$", homepage, name="categories"),
    url(r"^packaginator/$",
                direct_to_template,
                {'template': 'hack/packaginator.html'},
                name="packaginator"),

    url(r"^packaginate/$",
                packaginate,
                name="packaginate"),

    url(
        regex = '^autocomplete/hack/$',
        view = hack_autocomplete,
        name    = 'hack_autocomplete',
    )

)

from tastypie.api import Api
from apiv1.resources import (
                    GotwResource, DpotwResource,
                    HackResource, CategoryResource, RepoResource,
                    GridResource, HackResourceBase
                    )

v1_api = Api()
v1_api.register(HackResourceBase())
v1_api.register(HackResource())
v1_api.register(CategoryResource())
v1_api.register(RepoResource())
v1_api.register(GridResource())
v1_api.register(GotwResource())
v1_api.register(DpotwResource())

urlpatterns += patterns('',
    url(r"^api/", include(v1_api.urls)),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
