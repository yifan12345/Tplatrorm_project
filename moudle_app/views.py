from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from moudle_app.forms import ModuletForms
from moudle_app.models import Module
from django.http import JsonResponse
from project_app.models import Project


@login_required
def module(request):
    '''
    模块管理页面视图
    :param requests:
    :return:
    '''
    if request.method == "GET":
        module_all = Module.objects.all()
        return render(request, "module.html", {"modules": module_all, "type": "list"})


@login_required
def add_module(request):
    '''
    添加模块
    :param requests:
    :return:
    '''
    if request.method == "GET":
        module = ModuletForms()
        return render(request, "module.html", {"form": module, "type": "add"})

    if request.method == "POST":
        form = ModuletForms(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']

            Module.objects.create(project=project, name=name, describe=describe)
            return HttpResponseRedirect("/module/")


@login_required
def edit_module(request, mid):
    '''
    编辑模块
    :param request:
    :param mid:
    :return:
    '''
    if request.method == "GET":
        module = Module.objects.get(id=mid)

        form = ModuletForms(instance=module)
        return render(request, "module.html", {"form": form, "id": module.id, "type": "edit"})

    if request.method == "POST":
        form = ModuletForms(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']

            m = Module.objects.get(id=mid)
            m.name = name
            m.describe = describe
            m.project = project
            m.save()

            return HttpResponseRedirect("/module/")


def delete_module(request, mid):
    '''
    删除模块
    :param request:
    :param mid:
    :return:
    '''
    if request.method == "GET":
        try:
            module = Module.objects.get(id=mid)
        except Module.DoesNotExist:
            HttpResponseRedirect("/module/")
        else:
            module.delete()

        return HttpResponseRedirect("/module/")
    else:
        return HttpResponseRedirect("/module/")


def get_modiule_list(request):
    '''
    接口：根据项目ID，返回对于的模块列表
    :param request:
    :param mid:
    :return:
    '''

    if request.method == "POST":
        # featList = [pro.name for pro in proj]
        mid = request.POST.get("pid", "")
        if mid == "":
            return JsonResponse({"status": 10200, "message": "项目ID不能为空", })

        proj = Module.objects.filter(project=mid)
        module_list = []
        for pid in proj:
            module_dict = {
                "id": pid.id,
                "name": pid.name
            }
            module_list.append(module_dict)

        return JsonResponse({"status": 10200,
                             "message": "请求成功",
                             "data": module_list})
    else:
        return JsonResponse({"status": 10101, "message": "请求方法错误"})
