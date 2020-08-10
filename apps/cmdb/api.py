#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 2017.3 update by guohongze@126.com
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from apps.cmdb.models import Host
import json
from lib.common import app_token




def page_list_return(total, current=1):
    """
    page
    分页，返回本次分页的最小页数到最大页数列表
    """
    min_page = current - 4 if current - 6 > 0 else 1
    max_page = min_page + 6 if min_page + 6 < total else total

    return range(min_page, max_page + 1)


def pages(post_objects, request):
    """
    page public function , return page's object tuple
    分页公用函数，返回分页的对象元组
    """

    page_len = request.GET.get('page_len', '')
    if not page_len:
        page_len = 10
    paginator = Paginator(post_objects, page_len)
    try:
        current_page = int(request.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(paginator.page_range), current_page)
    end_page = len(paginator.page_range)

    try:
        page_objects = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        page_objects = paginator.page(paginator.num_pages)

    show_first = 0

    show_end = 0

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end, end_page


def get_object(model, **kwargs):
    """
    use this function for query
    使用改封装函数查询数据库
    """
    for value in kwargs.values():
        if not value:
            return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object




# 对于http接口，需要做认证，采用token方式
def host_add(request):
    if request.method == 'POST':
        # 接收post过来的json数据
        recevied_data = json.loads(request.body)
        if recevied_data['token'] == app_token:
            host = recevied_data['host']
            Host.objects.create(**host)
            return HttpResponse(json.dumps(host))

    elif request.method == "GET":
        return HttpResponse(status=403)


def host_update(request, intranet_ip):
    if request.method == 'POST':
        # 将接收的二进制转化为字典
        recevied_data = json.loads(request.body)
        if recevied_data['token'] == app_token:
            update_host = recevied_data['host']
            Host.objects.filter(intranet_ip=intranet_ip).update(hostname=update_host['hostname'],os=update_host['os'], cpu_model=update_host['cpu_model'], cpu_num=update_host['cpu_num'],
                                      memory=update_host['memory'], disk=update_host['disk'], intranet_ip=update_host['intranet_ip'], internet_ip=update_host['internet_ip'], idc_id=update_host['idc_id'])
            return HttpResponse(update_host)

    elif request.method == "GET":
        return HttpResponse(status=403)

def host_search(request):
    if request.method == 'POST':
        recevied_data = json.loads(request.body)
        intranet_ip= recevied_data['intranet_ip']

        if recevied_data['token'] == app_token:
            host = Host.objects.filter(intranet_ip=intranet_ip)
            if host.exists():
                dict = {}
                dict.update(host[0].__dict__)
                dict.pop("_state", None)
                data = {
                    'host': dict,
                    'code': 200
                }
                return HttpResponse(json.dumps(data))
            else:
                data = {
                    'code': 404
                }
                return HttpResponse(json.dumps(data))
    elif request.method == 'GET':
        return HttpResponse(status=403)