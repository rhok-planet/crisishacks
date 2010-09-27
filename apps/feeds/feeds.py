from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from hack.models import Hack

class RssLatestHacksFeed(Feed):
    title = "Latest Django hacks added"
    link = "/hacks/latest/"
    description = "The last 15 hacks added"

    def items(self):
        return Hack.objects.all().order_by("-created")[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.repo_description
        
    def item_pubdate(self, item):
        return item.created
        
class AtomLatestHacksFeed(RssLatestHacksFeed):
    feed_type = Atom1Feed
    subtitle = RssLatestHacksFeed.description