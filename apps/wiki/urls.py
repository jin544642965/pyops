from django.urls import path
from apps.wiki import article

urlpatterns = [
    path('article', article.article, name='article'),
    path('article/add', article.article_add, name='article_add'),
    path('article/edit', article.article_edit, name='article_edit'),
    path('article/del', article.article_del, name='article_del'),
    path('article/detail', article.article_detail, name='article_detail'),

    path('article_type', article.article_type, name='article_type'),
    path('article_type/add', article.article_type_add, name='article_type_add'),
    path('article_type/edit', article.article_type_edit, name='article_type_edit'),
    path('article_type/del', article.article_type_del, name='article_type_del'),
]

