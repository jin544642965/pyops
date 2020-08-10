from django import forms
from .models import Certificate
from django.forms.widgets import *

class CertificateForm(forms.ModelForm):
    # widgets负责渲染网页上的html
    class Meta:
        model = Certificate      # 需要关联的ORM模型
        exclude = ("id",)
        widgets = {
            'certificate_name': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'username': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'password': TextInput(attrs={'class': 'form-control','type':'password', 'style': 'width:530px;'}),
            'port': TextInput(attrs={'class': 'form-control', 'type':'number', 'style': 'width:530px;', 'placeholder': u'必填项', 'required': True}),
            'private_key': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'remask': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
        }
