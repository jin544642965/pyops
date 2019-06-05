from django import forms
from .models import Folder
from django.forms.widgets import *


class FolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
        }