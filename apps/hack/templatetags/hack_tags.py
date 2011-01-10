from datetime import datetime, timedelta

from django import template

from hack.models import Commit

register = template.Library()

@register.filter
def commits_over_52(hack):

    current = datetime.now()
    weeks = []
    commits = Commit.objects.filter(hack=hack).values_list('commit_date', flat=True)
    for week in range(52):
        weeks.append(len([x for x in commits if x < current and x > (current - timedelta(7))]))
        current -= timedelta(7)

    weeks.reverse()
    weeks = map(str, weeks)
    return ','.join(weeks)
