from django import forms
from .models import People

class SearchForm(forms.Form):
    min_release_date = forms.DateField(label='Movies minimum release date', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    max_release_date = forms.DateField(label='Movies maximum release date', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    planet_diameter = forms.IntegerField(label='Planet diameter greater than', required=True)
    gender = forms.ChoiceField(label='Character gender', required=True, choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get distinct genders from People model
        genders = People.objects.values_list('gender', flat=True).distinct().exclude(gender__isnull=True).exclude(gender='')
        # Create choices list (value, label)
        self.fields['gender'].choices = [(g, g) for g in genders]
