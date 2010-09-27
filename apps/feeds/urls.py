from django.conf.urls.defaults import *

from feeds import *

urlpatterns = patterns("",
    (r'^hacks/latest/rss/$', RssLatestHacksFeed()),
    (r'^hacks/latest/atom/$', AtomLatestHacksFeed()),    
)