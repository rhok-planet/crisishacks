import csv
from apps.hack.models import *

HACKS_CSV = 'data/hack_entries.csv'


def get_team(rows):
  team = []
  for r in rows:
    member = r.split(',')[0].split('-')[0].strip()
    team.append(member)
  return ','.join(team)


class HacksImporter():
  def __init__(self):
    pass

  def setHacksFromCsv(self):
    data = csv.reader(open(HACKS_CSV))
    headers = data.next()
    for row in data:
      hack = Hack()
      hack.title = row[headers.index('Team Name')]
      print 'working on',hack.title
      hack.category = Category.objects.get(id=1) # app

      try:
        repo_url = row[headers.index('Code Repository')]
      except:
        print 'unable to get repo url, skipping'
        continue
      if 'code.google.com' in repo_url:
        repo = Repo.objects.filter(title='Google Code')
      if 'github' in repo_url:
        repo = Repo.objects.filter(title='Github')
      hack.repo = repo[0]
      hack.repo_url = repo_url

      desc = row[headers.index('Short description of hack')]
      try:
        other = row[headers.index('Other Online Resources')]
      except:
        other = ''
      hack.description = desc + '\n\n' +  other
      hack.original_team = get_team(row[headers.index('Team participants')])
      hack.created_by = User.objects.filter(username='jlivni')[0]
      hack.last_modified_by = User.objects.filter(username='jlivni')[0]
      try:hack.fetch_metadata()
      except:
        print 'unable to fetch metadata'
      hack.save()
