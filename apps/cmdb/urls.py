from apps.cmdb import asset, idc, group
from django.urls import path

urlpatterns = [
    path('asset', asset.asset, name='cmdb'),
    path('asset/add', asset.asset_add, name='asset_add'),
    path('asset/del', asset.asset_del, name='asset_del'),
    path('asset/edit/<int:ids>/', asset.asset_edit, name='asset_edit'),
    path('asset/detail/<int:ids>/', asset.asset_detail, name='asset_detail'),

    path('idc', idc.idc, name='idc'),
    path('idc/add', idc.idc_add, name='idc_add'),
    path('idc/del', idc.idc_del, name='idc_del'),
    path('idc/edit/<int:idc_id>/', idc.idc_edit, name='idc_edit'),

    path('group', group.group, name='group'),
    path('group/add', group.group_add, name='group_add'),
    path('group/del', group.group_del, name='group_del'),
    path('group/edit/<int:group_id>/', group.group_edit, name='group_edit'),
    path('group/serverlist/<int:group_id>/', group.group_serverlist, name='group_serverlist'),
]

