from django import forms
from .models import *

class ImageForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = '__all__'
        exclude = ['user']
