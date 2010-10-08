from django.core.validators import URLValidator
from django.forms import ModelForm
from django.template.defaultfilters import slugify

from hack.models import Hack, HackExample

class HackForm(ModelForm):

    def clean_slug(self):
        return self.cleaned_data['slug'].lower()

    class Meta:
        model = Hack
        fields = ['repo_url', 'title', 'slug', 'repo', 'category', ]


class HackExampleForm(ModelForm):

    class Meta:
        model = HackExample
        fields = ['title', 'url']

class HackExampleModeratorForm(ModelForm):

    class Meta:
        model = HackExample
        fields = ['title', 'url', 'active']
