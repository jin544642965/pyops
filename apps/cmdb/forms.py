from django import forms
from .models import Idc, Host
from django.forms.widgets import *
from .models import HostGroup


class AssetForm(forms.ModelForm):

    class Meta:
        model = Host          # 需要关联的ORM模型
        exclude = ("id",)
        widgets = {
            'hostname': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'ip': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'asset_type': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'os': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'vendor': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'cpu_model': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'cpu_num': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'memory': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'disk': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'idc': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'position': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'物理机写位置，虚机写宿主'}),
            'memo': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:530px;'}),
        }


class IdcForm(forms.ModelForm):
    class Meta:
        model = Idc
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'address': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'tel': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'contact': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'contact_phone': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'ip_range': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class GroupForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(GroupForm, self).clean()
        return cleaned_data

    class Meta:
        model = HostGroup
        exclude = ("id", )

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'desc': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:450px;'}),

        }