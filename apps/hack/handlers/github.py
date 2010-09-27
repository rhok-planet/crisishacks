from django.conf import settings

from github2.client import Github

from hack.utils import uniquer

def pull(hack):
    
    if hasattr(settings, "GITHUB_ACCOUNT") and hasattr(settings, "GITHUB_KEY"):
        github   = Github(username=settings.GITHUB_ACCOUNT, api_token=settings.GITHUB_KEY)
    else:
        github   = Github()
        
    repo_name = hack.repo_name()
    repo         = github.repos.show(repo_name)
    hack.repo_watchers    = repo.watchers
    hack.repo_forks       = repo.forks
    hack.repo_description = repo.description

    collaborators = github.repos.list_collaborators(repo_name) + [x['login'] for x in github.repos.list_contributors(repo_name)]
    if collaborators:
        hack.participants = ','.join(uniquer(collaborators))
        
    return hack
