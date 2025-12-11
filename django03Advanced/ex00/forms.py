from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Article, UserFavouriteArticle

class PublishForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'synopsis', 'content']

class FavouriteForm(forms.ModelForm):
    class Meta:
        model = UserFavouriteArticle
        fields = ['article']
        widgets = {
            'article': forms.HiddenInput()
        }
