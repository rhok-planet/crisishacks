import csv
import re
from urllib2 import urlopen, URLError
from apps.hack.models import *

HACKS_CSV = 'data/hack_entries.csv'
# Try hack_import.py http://wiki.rhok.org/CERTS

def get_team(rows):
  team = []
  for r in rows:
    member = r.split(',')[0].split('-')[0].strip()
    team.append(member)
  return ','.join(team)

def HackImporterFactory(uri):
    if re.match(r'^https?://.*', uri, re.I):
      return UrlImporter(uri)
    elif re.match(r'.*\.csv$', uri, re.I):
      return CsvImporter(uri)
    else:
      raise Exception("Unknown URI to import".format(uri))

class HackImporter():

  def execute(self):
    pass

class CsvImporter(HackImporter):
  def __init__(self, uri):
    self.uri = uri
    pass
    
  def execute(self):
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

class UrlImporter(HackImporter):
  def __init__(self, uri):
    self.uri = uri

  def execute(self):
    print "Opening {0}".format(self.uri)
    try:
      self.response = urlopen(self.uri)
    except URLError:
      print "Failed to open url {0}".format(self.uri)
      return

    status = self.response.getcode()
    if status >= 400:
      print "Error fetching url {0} {1}".format(self.uri, status)
      return

    # grep for known repos
    for repo in Repo.objects.filter(is_supported=True):
      print "Checking for {0} repositories".format(repo.title)
      self.importHacks(repo)

  def importHacks(self, repo):
    if not repo.url_regex:
      return

    r = re.compile(repo.url_regex, re.IGNORECASE)

    for line in self.response:
      for url in r.findall(line):
        if Hack.objects.filter(repo_url=url):
          continue

        print "Importing {0}".format(url)
        hack = Hack()
        hack.repo = repo
        hack.repo_url = re.sub(r'^https', 'http', url)
        hack.category = Category.objects.get(id=1)
        hack.created_by = User.objects.get(username='jlivni')
        hack.last_modified_by = User.objects.get(username='jlivni')
        hack.fetch_metadata()
        hack.save()

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Usage: {0} <file|url>".format(sys.argv[0])
    exit(1)

  importer = HackImporterFactory(sys.argv[1])
  importer.execute()
