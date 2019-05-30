from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from project_app.forms import ProjectForms
from project_app.models import Project
from django.http import JsonResponse


@login_required
def project(request):
    '''
    管理页面，登陆成功
    :param request:
    :return:
    '''
    project_all = Project.objects.all()
    return render(request, "project.html", {"pro": project_all, "type": "list"})


@login_required
def add_project(request):
    '''
    添加项目
    :param requests:
    :return:
    '''
    if request.method == "GET":
        return render(request, "project.html", {"type": "add"})
    else:
        name = request.POST.get("name", "")
        describe = request.POST.get("describe", "")
        status = request.POST.get("status", "")
        if name == "":
            return render(request, "project.html", {"type": "add",
                                                    "name_error": "项目名称不能为空"})
        Project.objects.create(name=name, describe=describe, status=status)

        return HttpResponseRedirect("/project/")


@login_required
def edit_project(request, pid):
    '''
    编辑项目
    :param requests:
    :return:
    '''
    if request.method == "GET":
        if pid:
            form = ProjectForms(instance=Project.objects.get(id=pid))
            return render(request, "project.html", {"type": "edit",
                                                    "form": form,
                                                    "id": pid})
    elif request.method == "POST":
        form = ProjectForms(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']
            p = Project.objects.get(id=pid)
            p.name = name
            p.describe = describe
            p.status = status
            p.save()
        return HttpResponseRedirect("/project/")


@login_required
def delete_project(request, pid):
    '''
    删除项目
    :param request:
    :param pid:
    :return:
    '''
    if request.method == "GET":
        try:
            porject = Project.objects.get(id=pid)
        except Project.DoesNotExist:
            HttpResponseRedirect("/project/")
        else:
            porject.delete()

        return HttpResponseRedirect("/project/")
    else:
        return HttpResponseRedirect("/project/")


def get_project_list(request):
    '''
    接口：获取项目列表数据
    :param requests:
    :return:
    '''

    if request.method == "GET":
        # featList = [pro.name for pro in proj]
        proj = Project.objects.all()
        project_list = []
        for pro in proj:
            project_dict = {
                "id":pro.id,
                "name":pro.name
            }
            project_list.append(project_dict)


        return JsonResponse({"status": 10200,
                             "message": "请求成功",
                             "data": project_list})

    else:
        return JsonResponse({"status": 10101, "message": "请求方法错误"})
