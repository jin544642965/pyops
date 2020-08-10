from django.shortcuts import render
from . import forms
from .sync_sql_mobile import start_sync
from django.contrib.auth.decorators import login_required
from apps.accounts.permission import permission_verify


@login_required
@permission_verify()
def sync_data(request):
    # 当表单提交时
    if request.method == "POST":
        # form包含提交的表单数据
        form = forms.SyncForm(request.POST)
        # 如果提交的数据合法
        if form.is_valid():
            mobile_no = form.cleaned_data["mobile_no"]
            sync_process = start_sync(mobile_no)
            return render(request, 'data_manage/index.html', locals())
    else:
        form = forms.SyncForm()
    return render(request, 'data_manage/index.html', locals())



