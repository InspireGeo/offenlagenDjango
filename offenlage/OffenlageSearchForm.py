from django import forms
from .models import Offenlage



class OffenlageSearchForm(forms.Form):
    search = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))
