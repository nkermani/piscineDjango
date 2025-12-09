from django import forms


class HistoryForm(forms.Form):
    entry = forms.CharField(label="Your entry", max_length=255)
