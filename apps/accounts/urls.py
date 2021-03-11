from django.urls import path
from apps.accounts import user, permission, role


urlpatterns = [
    path('login/', user.login, name='login'),
    path('logout', user.logout, name='logout'),
    path('change/password', user.change_password, name='change_password'),
    path('reset/password/<int:ids>/', user.reset_password, name='reset_password'),

    path('user/manage', user.user_manage, name='user_manage'),
    path('user/add', user.user_add, name='user_add'),
    path('user/del/<int:ids>/', user.user_del, name='user_del'),
    path('user/edit/<int:ids>/', user.user_edit, name='user_edit'),

    path('permission/manage', permission.permission_manage, name='permission_manage'),
    path('permission/add', permission.permission_add, name='permission_add'),
    path('permission/del/<int:ids>/', permission.permission_del, name='permission_del'),
    path('permission/edit/<int:ids>/', permission.permission_edit, name='permission_edit'),
    path('permission/get_user_permission/', permission.get_user_permission, name='get_user_permission'),
    path('permission/permission_deny/', permission.permission_deny, name='permission_deny'),

    path('role/manage', role.role_manage, name='role_manage'),
    path('role/add', role.role_add, name='role_add'),
    path('role/del/<int:ids>/', role.role_del, name='role_del'),
    path('role/edit/<int:ids>/', role.role_edit, name='role_edit'),
]
