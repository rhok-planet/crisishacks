from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_index

from problemdefinition.models import ProblemDefinition

from problemdefinition.views import (
        add_feature,
        add_problemdefinition,
        add_problemdefinition_hack,
        ajax_problemdefinition_list,
        delete_feature,
        delete_problemdefinition_hack,
        edit_element,
        edit_problemdefinition,
        edit_feature,
        problemdefinition_detail,
        problemdefinitions
    )

urlpatterns = patterns("",


    url(
        regex = '^add/$',
        view    = add_problemdefinition,
        name    = 'add_problemdefinition',
    ),

    url(
        regex = '^(?P<slug>[-\w]+)/edit/$',
        view    = edit_problemdefinition,
        name    = 'edit_problemdefinition',
    ),

    url(
        regex = '^g/(?P<slug>[-\w]+)/$',
        view    = problemdefinition_detail,
        name    = 'problemdefinition',
    ),

    url(
        regex = '^element/(?P<feature_id>\d+)/(?P<hack_id>\d+)/$',
        view    = edit_element,
        name    = 'edit_element',
    ),

    url(
        regex = '^feature/add/(?P<problemdefinition_slug>[a-z0-9\-\_]+)/$',
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
        view    = delete_problemdefinition_hack,
        name    = 'delete_problemdefinition_hack',
    ),

    url(
        regex = '^(?P<problemdefinition_slug>[a-z0-9\-\_]+)/hack/add/$',
        view    = add_problemdefinition_hack,
        name    = 'add_problemdefinition_hack',
    ),

    url(
        regex = '^ajax_problemdefinition_list/$',
        view    = ajax_problemdefinition_list,
        name    = 'ajax_problemdefinition_list',
    ),

    url(
        regex   = r"^latest/$",
        view    = archive_index,
        name    = "latest_problemdefinitions",
        kwargs  = dict(
            queryset=ProblemDefinition.objects.select_related(),
            date_field='created'
            )
    ),

    url(
        regex = '^$',
        view    = problemdefinitions,
        name    = 'problemdefinitions',
    ),



)
