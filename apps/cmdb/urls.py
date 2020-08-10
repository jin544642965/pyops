from apps.cmdb import host, idc, group, api
from django.urls import path

urlpatterns = [
    path('host', host.host, name='host'),
    path('host/add', host.host_add, name='host_add'),
    path('host/del', host.host_del, name='host_del'),
    path('host/edit/<int:ids>/', host.host_edit, name='host_edit'),
    path('host/detail/<int:ids>/', host.host_detail, name='host_detail'),

    # ssh
    path('host/webssh/<int:ids>/', host.webssh, name='webssh'),

    path('idc', idc.idc, name='idc'),
    path('idc/add', idc.idc_add, name='idc_add'),
    path('idc/del', idc.idc_del, name='idc_del'),
    path('idc/edit/<int:idc_id>/', idc.idc_edit, name='idc_edit'),

    path('group', group.group, name='group'),
    path('group/add', group.group_add, name='group_add'),
    path('group/del', group.group_del, name='group_del'),
    path('group/edit/<int:group_id>/', group.group_edit, name='group_edit'),
    path('group/serverlist/<int:group_id>/', group.group_serverlist, name='group_serverlist'),

    path('api/host/add', api.host_add, name='api_host_add'),
    path('api/host/update/<str:intranet_ip>',api.host_update, name='api_host_update'),
    path('api/host_search', api.host_search, name='api_host_search'),

]

