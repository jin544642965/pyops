from django import forms
from .models import Article, ArticleType
from django.forms.widgets import HiddenInput


class MDEditorModelForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MDEditorModelForm, self).__init__(*args, **kwargs)
	    # 表单隐藏作者字段
        self.fields['author'].widget = HiddenInput()


class ArticleTypeForm(forms.ModelForm):

    class Meta:
        model = ArticleType
        fields = '__all__'
