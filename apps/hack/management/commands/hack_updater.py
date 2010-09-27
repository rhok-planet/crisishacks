import json
from sys import stdout
from time import sleep, gmtime, strftime
from urllib import urlopen

from django.conf import settings
from django.core.management.base import CommandError, NoArgsCommand

from github2.client import Github

from hack.models import Hack, Repo, Commit


class Command(NoArgsCommand):
    
    help = "Updates all the hacks in the system. Commands belongs to django-hacks.apps.hack"    
    
    def handle(self, *args, **options):
        
        print >> stdout, "Commencing hack updating now at %s " % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        
        # set up various useful bits
        github_repo = Repo.objects.get(title__icontains="github")
        bitbucket_repo = Repo.objects.get(title__icontains="bitbucket")    
        
        # instantiate the github connection
        if hasattr(settings, "GITHUB_ACCOUNT") and hasattr(settings, "GITHUB_KEY"):
            github   = Github(username=settings.GITHUB_ACCOUNT, api_token=settings.GITHUB_KEY)
            authed = True
        else:
            github   = Github()
            authed = False

        for index, hack in enumerate(Hack.objects.all()):
            zzz = 5
            
            try:
                if hack.repo == github_repo:
                    # Do github
                    hack.fetch_metadata()
                    for commit in github.commits.list(hack.repo_name(), "master"):
                        commit, created = Commit.objects.get_or_create(hack=hack, commit_date=commit.committed_date)
                    zzz += 1
                elif hack.repo == bitbucket_repo:
                    zzz = 1
                    # do bitbucket
                    hack.fetch_metadata()                    
                    for commit in get_bitbucket_commits(hack):
                        commit, created = Commit.objects.get_or_create(hack=hack, commit_date=commit["timestamp"])
                else:
                    # unsupported so we skip and go on
                    print >> stdout, "%s. Skipped hack '%s' because it uses an unsupported repo" % (index+1,hack.title)
                    continue
            except RuntimeError, e:
                message = "For '%s', too many requests issued to repo threw a RuntimeError: %s" % (hack.title, e)
                raise CommandError(message)
            if not authed:
               sleep(zzz)
            print >> stdout, "%s. Successfully updated hack '%s'" % (index+1,hack.title)

        print >> stdout, "-" * 40
        print >> stdout, "Finished at %s" % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

def get_bitbucket_commits(hack):
    repo_name = hack.repo_name()
    if repo_name.endswith("/"):
        repo_name = repo_name[0:-1]
    target = "http://api.bitbucket.org/1.0/repositories/%s/changesets/?limit=50" % repo_name
    page = urlopen(target).read()
    try:
        data = json.loads(page)
    except ValueError, e:
        # TODO - fix this problem with bad imports from bitbucket
        print >> stdout, "Problems with %s" % hack.title
        print >> stdout, target        
        print >> stdout, e
        data = {}
    return data.get("changesets", [])
    
    