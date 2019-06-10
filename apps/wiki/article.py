from django.contrib.auth.decorators import login_required
from apps.accounts.permission import permission_verify
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from .forms import MDEditorModelForm, ArticleTypeForm
from .models import Article, ArticleType
from apps.cmdb.api import pages
import markdown
from django.db.models import Q


@login_required()
@permission_verify()
def article(request):
    article_type_all = ArticleType.objects.all()
    id = request.GET.get("id")
    article_type_name = request.GET.get('article_type', '')
    keyword = request.GET.get('keyword', '')

    if article_type_name:
        article_type_obj = ArticleType.objects.get(name=article_type_name)
        article_list = Article.objects.filter(article_type_id=article_type_obj.id)  # 这里不能用get，get只返回一条记录，filter支持多条记录
    else:
        article_list = Article.objects.all().order_by("-id")

    # 搜索功能
    if keyword:
        article_list = article_list.filter(
            Q(name__contains=keyword) |
            Q(author__contains=keyword) |
            Q(commit_time__contains=keyword) |
            Q(content__contains=keyword))

    # 分写的对象
    article_list, p, article_list, page_range, current_page, show_first, show_end, end_page = pages(article_list, request)
    return render(request, "wiki/article.html", locals())


@login_required()
@permission_verify()
def article_add(request):

    if request.method == "POST":
        form = MDEditorModelForm(request.POST)
        if form.is_valid():
            form.save()
            tips = "添加成功"
            return HttpResponseRedirect(reverse(article))
        else:
            tips = "添加失败"
            return render(request, "wiki/article_add.html", locals())
    elif request.method == "GET":
        # 初始化设置作者值
        form = MDEditorModelForm(initial={"author": request.user.username})
        return render(request, "wiki/article_add.html", locals())


@login_required()
@permission_verify()
def article_edit(request):
    id = request.GET.get('id')
    project = Article.objects.get(id=id)
    if request.method == "POST":
        form = MDEditorModelForm(request.POST, instance=project)
        if form.is_valid():
            # 前端表单传来的数据全部保存进数据库
            form.save()
            return HttpResponseRedirect(reverse(article))
    elif request.method == "GET":
        form = MDEditorModelForm(instance=project)
        return render(request, "wiki/article_edit.html", locals())


@login_required()
@permission_verify()
def article_del(request):
    if request.method == "POST":
        article_batch = request.GET.get('arg', '')
        article_id_all = request.POST.get('asset_id_all', '')
        if article_batch:
            for article_id in article_id_all.split(','):
                Article.objects.filter(id=article_id).delete()
    return HttpResponse(u'删除成功')


@login_required()
@permission_verify()
def article_detail(request):
    id = request.GET.get('id', '')
    if id:
        article = Article.objects.get(id=id)
        name = article.name
        author = article.author
        commit_time = str(article.commit_time)
        content = markdown.markdown(article.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return render(request, "wiki/article_detail.html", locals())
    else:
        err = "文章不存在"
        return render(request, "wiki/article_detail.html", locals())


@login_required()
@permission_verify()
def article_type(request):
    allgroup = ArticleType.objects.all()
    return render(request, "wiki/article_type.html", locals())


@login_required()
@permission_verify()
def article_type_add(request):
    if request.method == "POST":
        article_type_form = ArticleTypeForm(request.POST)
        if article_type_form.is_valid():
            article_type_form.save()
            return HttpResponseRedirect(reverse(article_type))
    article_type_form = ArticleTypeForm()
    return render(request, 'wiki/article_type_add.html', locals())


@login_required()
@permission_verify()
def article_type_edit(request):
    id = request.GET.get('id')
    project = ArticleType.objects.get(id=id)
    if request.method == "POST":
        article_type_form = ArticleTypeForm(request.POST, instance=project) # 创建一个form实例
        if article_type_form.is_valid():
            article_type_form.save()
            return HttpResponseRedirect(reverse(article_type))
    elif request.method == "GET":
        article_type_form = ArticleTypeForm(instance=project)
        return render(request, 'wiki/article_type_edit.html', locals())


@login_required()
@permission_verify()
def article_type_del(request):
    group_id = request.GET.get('id', '')
    if group_id:
        ArticleType.objects.filter(id=group_id).delete()

    if request.method == 'POST':
        group_items = request.POST.getlist('g_check', [])
        if group_items:
            for n in group_items:
                ArticleType.objects.filter(id=n).delete()
    allgroup = ArticleType.objects.all()
    return render(request, 'wiki/article_type.html', locals())


