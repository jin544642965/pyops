from django.urls import path
from apps.wiki import article

urlpatterns = [
    path('article', article.article, name='article'),
    path('article/add', article.article_add, name='article_add'),
    path('article/edit', article.article_edit, name='article_edit'),
    path('article/del', article.article_del, name='article_del'),
    path('article/detail', article.article_detail, name='article_detail'),

    path('article_group', article.article_group, name='article_group'),
    path('article_group/add', article.article_group_add, name='article_group_add'),
    path('article_group/edit', article.article_group_edit, name='article_group_edit'),
    path('article_group/del', article.article_group_del, name='article_group_del'),
]

