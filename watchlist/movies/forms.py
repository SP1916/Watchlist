from django.forms import ModelForm
from django import forms

from .models import Movies

class MovieForm(ModelForm):
    class Meta:
        model = Movies
        fields = '__all__'
        exclude = ['user']
                
        labels = {
        'status': 'Watched'
        }