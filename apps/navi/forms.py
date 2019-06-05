from django import forms
from .models import Navi


class navi_form(forms.ModelForm):
    def clean(self):
        cleaned_data = super(navi_form, self).clean()
        value = cleaned_data.get('name')
        try:
            Navi.objects.get(name=value)
            self._errors['name']=self.error_class(["%s的信息已经存在" % value])
        except Navi.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = Navi
        exclude = ("id",)