from django.db import models
from mdeditor.fields import MDTextField


class ArticleType(models.Model):
    name = models.CharField("分类名称", max_length=20)       # 默认必填

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=20, verbose_name="标题")  # 标题
    author = models.CharField(max_length=10, verbose_name="作者", default='')
    commit_time = models.DateField(auto_now_add=False, auto_now=True)
    content = MDTextField(verbose_name='内容')     # 内容
    article_type = models.ForeignKey(
            ArticleType,
            blank=True,
            verbose_name="文章分类",
            on_delete=models.CASCADE,
            default=""
    )












