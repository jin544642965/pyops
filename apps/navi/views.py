from django.shortcuts import render
from .models import Navi
from django.contrib.auth.decorators import login_required
from .forms import navi_form
# Create your views here.


@login_required()
def navi(request):
    allnavi = Navi.objects.all()
    return render(request, "navi/navi.html", locals())


@login_required()
def manage(request):
    allnavi = Navi.objects.all()
    return render(request, "navi/manage.html", locals())


@login_required()
def navi_add(request):
    if request.method == "POST":
        n_form = navi_form(request.POST)
        if n_form.is_valid():
            n_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "navi/navi_add.html", locals())
    else:
        display_control = "none"
        n_form = navi_form()
        return render(request, "navi/navi_add.html", locals())


@login_required()
def navi_del(request):
    if request.method == 'POST':
        navi_items = request.POST.getlist('navi_check', [])
        if navi_items:
            for n in navi_items:
                Navi.objects.filter(id=n).delete()
    allnavi = Navi.objects.all()
    return render(request, "navi/manage.html", locals())


@login_required()
def navi_edit(request):
    if request.method == 'GET':
        item = request.GET.get("id")
        obj = Navi.objects.get(id=item)
    return render(request, "navi/navi_edit.html", locals())


@login_required()
def navi_save(request):
    temp_name = "navi/navi-header.html"
    if request.method == 'POST':
        ids = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        url = request.POST.get('url')
        navi_item = Navi.objects.get(id=ids)
        navi_item.name = name
        navi_item.description = desc
        navi_item.url = url
        navi_item.save()
        status = 1
    else:
        status = 2
    allnavi = Navi.objects.all()
    return render(request, "navi/navi_edit.html", locals())
