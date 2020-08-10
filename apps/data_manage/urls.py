from django.urls import path
from apps.data_manage import data_manage
urlpatterns = [
    path('sync_data', data_manage.sync_data, name='sync_data'),
]