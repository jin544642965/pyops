from django.contrib.auth.decorators import login_required
from apps.accounts.permission import permission_verify
from django.shortcuts import HttpResponse, render
from .models import Idc, HostGroup, ASSET_TYPE, Host
from apps.cmdb.api import get_object, pages
from django.db.models import Q
from .forms import AssetForm


# 主机资产列表
@login_required
@permission_verify()
def host(request):
    # webssh_domain = get_dir("webssh_domain")
    asset_find = []
    idc_info = Idc.objects.all()
    group_info = HostGroup.objects.all()
    asset_types = ASSET_TYPE
    idc_name = request.GET.get('idc', '')
    page_len = request.GET.get('page_len', '')
    group_name = request.GET.get('group', '')
    asset_type = request.GET.get('asset_type', '')
    status = request.GET.get('status', '')
    keyword = request.GET.get('keyword', '')
    group_id = request.GET.get("group_id", '')
    cabinet_id = request.GET.get("cabinet_id", '')
    idc_id = request.GET.get("idc_id", '')
    asset_id_all = request.GET.getlist("id", '')

    if group_id:
        group = get_object(HostGroup, id=group_id)
        if group:
            asset_find = Host.objects.filter(group=group)
    elif idc_id:
        idc = get_object(Idc, id=idc_id)
        if idc:
            asset_find = Host.objects.filter(idc=idc)
    else:
        asset_find = Host.objects.all()

    if idc_name:
        asset_find = asset_find.filter(idc__name__contains=idc_name)
    if group_name:
        get_group = HostGroup.objects.get(name=group_name)
        asset_find = get_group.serverList.all()
    if asset_type:
        asset_find = asset_find.filter(asset_type__contains=asset_type)

    if keyword:
        asset_find = asset_find.filter(
            Q(hostname__contains=keyword) |
            Q(internet_ip__contains=keyword) |
            Q(intranet_ip__contains=keyword) |
            Q(os__contains=keyword) |
            Q(vendor__contains=keyword) |
            Q(cpu_model__contains=keyword) |
            Q(cpu_num__contains=keyword) |
            Q(memory__contains=keyword) |
            Q(disk__contains=keyword) |
            Q(position__contains=keyword) |
            Q(memo__contains=keyword))

    assets_list, p, assets, page_range, current_page, show_first, show_end, end_page = pages(asset_find, request)
    return render(request, 'cmdb/host.html', locals())


@login_required
@permission_verify()
def host_add(request):
    if request.method == "POST":
        a_form = AssetForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "cmdb/host_add.html", locals())
    else:
        display_control = "none"
        a_form = AssetForm()

        return render(request, "cmdb/host_add.html", locals())


@login_required
@permission_verify()
def host_del(request):
    if request.method == 'POST':
        asset_batch = request.GET.get('arg', '')
        asset_id_all = str(request.POST.get('asset_id_all', ''))

        if asset_batch:
            for asset_id in asset_id_all.split(','):
                asset_item = get_object(Host, id=asset_id)
                asset_item.delete()

    return HttpResponse(u'删除成功')


@login_required
@permission_verify()
def host_edit(request, ids):
    status = 0
    asset_types = ASSET_TYPE
    obj = get_object(Host, id=ids)

    if request.method == 'POST':
        af = AssetForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = AssetForm(instance=obj)

    return render(request, 'cmdb/host_edit.html', locals())


@login_required
@permission_verify()
def host_detail(request, ids):
    host = Host.objects.get(id=ids)
    try:
        disk = eval(host.disk)
    except Exception as e:
        print(e)
    return render(request, 'cmdb/host_detail.html', locals())


@login_required
@permission_verify()
def webssh(request, ids):
    host = Host.objects.get(id=ids)

    # 安全验证，登录后也只有超级用户才有权限ssh
    if not request.user.is_superuser:
        group = host.hostgroup_set.all()
        perms = request.user.role.webssh.all()

        for p in perms:
            if p not in group:
                return HttpResponse("forbidden! you have no permissions.", status=403)

    return render(request,'cmdb/webssh.html', locals())