from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import HttpResponse, redirect
from django.http import JsonResponse
from django.shortcuts import render
from .forms import FolderForm
from django.contrib.auth.decorators import login_required
from apps.accounts.permission import permission_verify
import os
import shutil
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.utils.http import urlquote
from apps.cmdb.api import pages
import time


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)


def getdirsize(dir):

   size = 0
   for root, dirs, files in os.walk(dir):
      size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
   return size


@login_required()
@permission_verify()
def folder_manage(request):
    physical_path = "uploads/dropbox"
    isExists = os.path.exists(physical_path)
    if not isExists:
        os.mkdir(physical_path)
        print("创建成功%s", physical_path)

    # 列出文件列表
    document_list = os.listdir(physical_path)
    document_list.sort()

    folder_dict = {}
    for folder in document_list:
        folderpath = physical_path + '/' + folder
        if os.path.isdir(folderpath):
            namespace = uuid.NAMESPACE_URL
            document_uuid = uuid.uuid3(namespace, folder)

            # 获取文件夹的大小，时间
            document_size = getdirsize(folderpath)
            document_size = sizeof_fmt(document_size)
            document_time = os.path.getctime(folderpath)
            document_time = TimeStampToTime(document_time)

            folder_dict[folder]  = {'type': 'folder', 'uuid': document_uuid, 'document_size': document_size,
                               'document_time': document_time}
    document_dict = folder_dict

    # 分写的对象
    document_list, p, document_list, page_range, current_page, show_first, show_end, end_page = pages(document_list, request)
    return render(request, 'netdisk/folder_manage.html', locals())


@login_required()
@permission_verify()
def folder_del(request):

    if request.method == 'GET':
        document = request.GET.get('document')
        physical_path = "uploads/dropbox/" + document

        if os.path.isdir(physical_path):
            shutil.rmtree(physical_path)
        elif os.path.isfile(physical_path):
            os.remove(physical_path)
        else:
            print("it's a special file(socket,FIFO,device file")
    return HttpResponseRedirect('/netdisk/folder/')


@login_required()
@permission_verify()
def folder_add(request):
    if request.method == "POST":
        folder_form = FolderForm(request.POST)
        folder = request.POST.get('name', '')

        # 去除首位空格
        folder = folder.strip()

        # # 去除尾部\符号
        folder = folder.rstrip("\\")

        physical_path = "uploads/dropbox/" + folder

        # 判断文件夹是否存在
        isExists = os.path.exists(physical_path)
        if not isExists:
            os.mkdir(physical_path)
            print("创建成功%s", physical_path)
            status = 1
        else:
            print("文件已存在")
        return render(request, 'netdisk/folder_add.html', locals())
    else:
        folder_form = FolderForm()
    return render(request, "netdisk/folder_add.html", locals())


@csrf_exempt
@login_required()
@permission_verify()
def folder_edit(request):
    document_newname = request.POST.get('document_newname')
    document_name = request.POST.get('document_name')

    # 去除首位空格
    document_newname = document_newname.strip()

    # # 去除尾部\符号
    document_newname = document_newname.rstrip("\\")

    document_newname_path = "uploads/dropbox/" + document_newname
    document_name_path = "uploads/dropbox/" + document_name
    # 更改文件或目录名
    os.rename(document_name_path, document_newname_path)

    namespace = uuid.NAMESPACE_URL
    document_uuid = uuid.uuid3(namespace, document_newname)
    data = {'result': document_newname, 'uuid': document_uuid}

    return JsonResponse(data)


# 文件夹的操作
@login_required()
@permission_verify()
def folder_parent(request, parent):

    physical_path = "uploads/dropbox/" + parent
    isExists = os.path.exists(physical_path)
    if not isExists:
        os.mkdir(physical_path)
        print("创建成功%s", physical_path)

    document_list = os.listdir(physical_path)  # 得到文件夹中的所有文件名称
    document_list.sort()
    file_dict = {}

    for file in document_list:
        filepath = physical_path + '/' + file
        if os.path.isfile(physical_path + '/' + file):
            namespace = uuid.NAMESPACE_URL
            document_uuid = uuid.uuid3(namespace,file)

            # 获取文件的大小
            document_size = os.path.getsize(filepath)
            document_size = sizeof_fmt(document_size)
            # 获取文件的修改时间
            document_time = os.path.getmtime(filepath)
            document_time = TimeStampToTime(document_time)

            file_dict[file] = {'type': 'file', 'uuid': document_uuid, 'document_size': document_size, 'document_time': document_time}

    folder_dict = {}
    for folder in document_list:
        folderpath = physical_path + '/' + folder
        if os.path.isdir(folderpath):
            namespace = uuid.NAMESPACE_URL
            document_uuid = uuid.uuid3(namespace, folder)

            # 获取文件夹的大小，时间
            document_size = getdirsize(folderpath)
            document_size = sizeof_fmt(document_size)
            document_time = os.path.getctime(folderpath)
            document_time = TimeStampToTime(document_time)
            folder_dict[folder] = {'type': 'folder', 'uuid': document_uuid, 'document_size': document_size, 'document_time': document_time}

        # 分写的对象
        document_list, p, document_list, page_range, current_page, show_first, show_end, end_page = pages(document_list, request)

    document_dict = folder_dict.copy()
    document_dict.update(file_dict)
    return render(request, 'netdisk/folder_parent.html', locals())


@login_required()
@permission_verify()
def folder_parent_add(request, parent):
    if request.method == "POST":
        folder_form = FolderForm(request.POST)
        folder = request.POST.get('name', '')

        # 去除首位空格
        folder = folder.strip()

        # # 去除尾部\符号
        folder = folder.rstrip("\\")

        physical_path = "uploads/dropbox/" + parent + '/' + folder

        # 判断文件夹是否存在
        isExists = os.path.exists(physical_path)
        if not isExists:
            os.mkdir(physical_path)
            print("创建成功%s", physical_path)
            status = 1
        else:
            print("文件已存在")
        return render(request, 'netdisk/folder_parent_add.html', locals())
    else:
        folder_form = FolderForm()

    return render(request, "netdisk/folder_parent_add.html", locals())


@login_required()
@permission_verify()
def folder_parent_del(request):
    if request.method == 'GET':
        parent = request.GET.get('parent', '')
        document = request.GET.get('document')
        relative_path = parent + '/' + document
        physical_path = "uploads/dropbox/" + relative_path
        if os.path.isdir(physical_path):
            shutil.rmtree(physical_path)
        elif os.path.isfile(physical_path):
            os.remove(physical_path)
        else:
            print("it's a special file(socket,FIFO,device file")
    return HttpResponseRedirect(parent)




@csrf_exempt
@login_required()
@permission_verify()
def folder_parent_edit(request, parent):
    document_newname = request.POST.get('document_newname')
    document_name = request.POST.get('document_name')

    # 去除首位空格
    document_newname = document_newname.strip()

    # # 去除尾部\符号
    document_newname = document_newname.rstrip("\\")

    document_newname_path = "uploads/dropbox/" + parent + '/' + document_newname
    document_name_path = "uploads/dropbox/" + parent + '/' + document_name
    # 更改文件或目录名
    os.rename(document_name_path, document_newname_path)
    namespace = uuid.NAMESPACE_URL
    document_uuid = uuid.uuid3(namespace, document_newname)

    data = {'result': document_newname, 'uuid': document_uuid}
    return JsonResponse(data)


@csrf_exempt
@login_required()
@permission_verify()
def fileupload(request, parent):
    f = request.FILES['file']
    document_name_path = "uploads/dropbox/" + parent + '/' + f.name
    with open(document_name_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    data = {'result': "上传成功"}
    return JsonResponse(data)




@csrf_exempt
@login_required()
@permission_verify()
def filedownload(request, parent):
    if request.method == 'GET':
        document_name = request.GET.get('document_name')

        document_name_path = "uploads/dropbox/" + parent + '/' + document_name
        file = open(document_name_path, 'rb')
        response = FileResponse(file)

        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        # urlquote解决中文名问题
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(document_name))
        response['Content-Length'] = os.path.getsize(document_name_path)
        response['Content-Type'] = 'application/octet-stream'
        return response
    else:
        return HttpResponse('method must be get')

