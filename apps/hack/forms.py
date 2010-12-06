from django.core.validators import URLValidator
from django.forms import ModelForm
from django.template.defaultfilters import slugify

from hack.models import Hack, Deployment 

class HackForm(ModelForm):

    def clean_slug(self):
        return self.cleaned_data['slug'].lower()

    class Meta:
        model = Hack
        fields = ['repo_url', 'title', 'slug', 'repo', 'category', ]


class DeploymentForm(ModelForm):

    class Meta:
        model = Deployment
        fields = ['title', 'url', 'description', 'location', 'number_users', 'lat', 'lng', 'bbox']

class HackExampleModeratorForm(ModelForm):

    class Meta:
        model = Deployment
        fields = ['title', 'url']
