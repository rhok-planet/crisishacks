from django.forms import ModelForm

from problemdefinition.models import  Element, Feature, ProblemDefinition, ProblemDefinitionHack

class ProblemDefinitionForm(ModelForm):

    def clean_slug(self):
        return self.cleaned_data['slug'].lower()

    class Meta:
        model = ProblemDefinition
        fields = ['title', 'slug', 'description']

class ElementForm(ModelForm):

    class Meta:
        model = Element
        fields = ['text',]

class FeatureForm(ModelForm):

    class Meta:
        model = Feature
        fields = ['title', 'description',]

class ProblemDefinitionHackForm(ModelForm):

    class Meta:
        model = ProblemDefinitionHack
        fields = ['hack']
