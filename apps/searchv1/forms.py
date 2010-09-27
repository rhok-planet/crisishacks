from django import forms

class SearchForm(forms.Form):
    
    q            = forms.CharField(label="Search Grids and Hacks", max_length=100)
    #hack      = forms.BooleanField(label="Search hacks?", initial=True)
    #grid         = forms.BooleanField(label="Search hacks?", initial=True)