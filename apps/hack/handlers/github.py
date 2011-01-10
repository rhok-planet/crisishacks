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
      if not cur_hack.title: cur_hack.title = repo.name
      if not cur_hack.description: cur_hack.description = repo.description
    except:
      print 'unable to get repo'

    try:
      collaborators = github.repos.list_collaborators(repo_name) + [x['login'] for x in github.repos.list_contributors(repo_name)]
      if collaborators:
        cur_hack.participants = ','.join(uniquer(collaborators))
    except:
      print 'unable to get collaborators'

    try:
      local_commits = cur_hack.commit_set.all()
      commits = github.commits.list(repo_name)
      for commit in commits:
        if not local_commits or commit.committed_date > local_commits[0]:
          c = hack.models.Commit()
          c.commit_date = commit.committed_date
          c.hack = cur_hack
          c.save()
    except:
      print 'unable to get commits'


    return cur_hack
