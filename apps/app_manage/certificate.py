from django.shortcuts import render
from apps.accounts.permission import permission_verify
from django.contrib.auth.decorators import login_required
from .forms import CertificateForm
from .models import Certificate
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.cmdb.api import pages
from django.db.models import Q

@login_required()
@permission_verify()
def certificate(request):
    certificate_list =  Certificate.objects.all()
    keyword = request.GET.get('keyword', '')
    # 搜索功能
    if keyword:
        certificate_list = certificate_list.filter(
            Q(certificate_name__contains=keyword) |
            Q(remask__contains=keyword))

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    certificate_list, p, certificate_list, page_range, current_page, show_first, show_end, end_page = pages(certificate_list, request)

    return render(request, 'app_manage/certificate.html', locals())


@login_required()
@permission_verify()
def certificate_add(request):


    if request.method == "POST":
        certificate_form = CertificateForm(request.POST)
        if certificate_form.is_valid():
            certificate_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "app_manage/certificate_add.html", locals())
    else:
        display_control = "none"
        certificate_form = CertificateForm()

        return render(request, 'app_manage/certificate_add.html', locals())


@login_required()
@permission_verify()
def certificate_del(request):
    certificate_id = request.GET.get('id', '')

    # # 单选删除
    # if certificate_id:
    #     Certificate.objects.filter(id=certificate_id).delete()

    #复选框删除
    if request.method == 'POST':
        # 获取数组，复选框，不存在则设为空
        certificate_items = request.POST.getlist('certificate_checkbox', [])
        if certificate_items:
            for n in certificate_items:
                Certificate.objects.filter(id=n).delete()
    certificate_list = Certificate.objects.all()

    return render(request, "app_manage/certificate.html", locals())


@login_required()
@permission_verify()
def certificate_edit(request, certificate_id):
    # 获取modelfrom对象
    project = Certificate.objects.get(id=certificate_id)

    if request.method == 'POST':
        # 修改时需要instance，如果没有则默认就是增加数据的
        form = CertificateForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('certificate'))
    else:
        form = CertificateForm(instance=project)

    display_control = "none"
    results = {
        'certificate_form': form,
        'certificate_id': certificate_id,
        'request': request,
        'display_control': display_control,
    }


    return render(request, 'app_manage/certificate_add.html', results)