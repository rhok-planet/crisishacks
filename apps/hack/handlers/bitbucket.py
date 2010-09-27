import re
from urllib import urlopen
from warnings import warn

try:
    import simplejson as json
except ImportError:
    import json

from hack.utils import uniquer

API_TARGET = "http://api.bitbucket.org/1.0/repositories/"

descendants_re = re.compile(r"Forks/Queues \((?P<descendants>\d+)\)")


def pull(hack):
    
    # prep the target name
    repo_name = hack.repo_name()
    target = API_TARGET + repo_name
    if not target.endswith("/"):
        target += "/"
    
    # open the target and read the content
    response = urlopen(target)
    response = response.read()
    
    # dejsonify the results
    try:
        data = json.loads(response)
    except json.decoder.JSONDecodeError:
        # TODO - log this better
        message = "%s had a JSONDecodeError during bitbucket.repo.pull" % (hack.title)
        warn(message)
        return hack

    hack.repo_watchers    = data.get("followers_count",0)
    hack.repo_description = data.get("description","")
    
    # screen scrape to get the repo_forks off of bitbucket HTML pages
    target = hack.repo_url
    if not target.endswith("/"):
        target += "/"
    target += "descendants"
    html = urlopen(target)
    html = html.read()
    try:
        hack.repo_forks = descendants_re.search(html).group("descendants")
    except AttributeError:
        hack.repo_forks = 0
    
    try:
        hack.participants = hack.repo_url.split("/")[3] # the only way known to fetch this from bitbucket!!!
    except IndexError:
        hack.participants = ""
        
    return hack
