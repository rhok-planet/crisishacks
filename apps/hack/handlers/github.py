from django.conf import settings
from github2.client import Github
from hack.utils import uniquer
import hack

def pull(cur_hack):

    if hasattr(settings, "GITHUB_ACCOUNT") and hasattr(settings, "GITHUB_KEY"):
        github   = Github(username=settings.GITHUB_ACCOUNT, api_token=settings.GITHUB_KEY)
        print 'NO GITHUB ACCT'
    else:
        github   = Github()

    repo_name = cur_hack.repo_name()
    try:
      repo         = github.repos.show(repo_name)
      cur_hack.repo_watchers    = repo.watchers
      cur_hack.repo_forks       = repo.forks
      cur_hack.repo_description = repo.description
    except:
      print 'unable to get repo'

    try:
      collaborators = github.repos.list_collaborators(repo_name) + [x['login'] for x in github.repos.list_contributors(repo_name)]
      if collaborators:
        cur_hack.participants = ','.join(uniquer(collaborators))
    except:
      print 'unable to get collaborators'

    try:
      commits = github.commits.list(repo_name)
    except:
      print 'unable to get commits'
    for commit in commits:
      c = hack.models.Commit()
      c.commit_date = commit.committed_date
      c.hack = cur_hack
      c.save()


    return cur_hack
