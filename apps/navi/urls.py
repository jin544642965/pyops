from django.urls import path
from apps.navi import views

urlpatterns = [
    path('', views.navi, name='navi'),
    path('add', views.navi_add, name='navi_add'),
    path('del', views.navi_del, name='navi_del'),
    path('edit', views.navi_edit, name='navi_edit'),
    path('save', views.navi_save, name='navi_save'),
    path('manage', views.manage, name='manage'),
]

