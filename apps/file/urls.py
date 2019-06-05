from django.urls import path, re_path
from apps.file import file

urlpatterns = [
    # 资料库添加
    path('folder/', file.folder, name='folder'),
    path('folder/add', file.folder_add, name="folder_add"),   # 和下面的parent有点冲突，所以精确匹配，最后面加/
    path('folder/del', file.folder_del, name="folder_del"),
    path('folder/edit', file.folder_edit, name="folder_edit"),

    # 对文件夹的操作
    path('folder/<path:parent>/', file.folder_parent, name='folder_parent'),
    path('folder/<path:parent>/folder_parent_add', file.folder_parent_add, name="folder_parent_add"),
    path('folder/folder_parent_del', file.folder_parent_del, name="folder_parent_del"),
    path('folder/<path:parent>/edit', file.folder_parent_edit, name="folder_parent_edit"),

    path('folder/<path:parent>/fileupload', file.fileupload, name='fileupload'),
    path('folder/<path:parent>/filedownload', file.filedownload, name='filedownload'),
]

