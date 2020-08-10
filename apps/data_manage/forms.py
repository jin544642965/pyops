from django import forms

class SyncForm(forms.Form):
    mobile_no = forms.CharField(label="", max_length=11, min_length=11, error_messages={"min_length": "太短了", 'max_length':"太长了"}, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"输入手机号"}))
