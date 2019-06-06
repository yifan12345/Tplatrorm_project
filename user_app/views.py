from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
# MTV view
def index(request):
    """
    登陆首页
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "index.html")
    else:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == "" or password == "":
            return render(request, "index.html", {
                "error": "用户名或密码为空"})

        user = auth.authenticate(username=username, password=password)
        if user is None:
            return render(request, "index.html", {
                "error": "用户名或密码错误"})
        else:
            auth.login(request, user)  # 记录用户的登陆状态
            return HttpResponseRedirect("/project/")


@login_required
def module(requests):
    '''
    模块管理页面
    :param requests:
    :return:
    '''
    return render(requests, "module.html")


@login_required
def interface_case(requests):
    '''
    任务管理页面
    :param requests:
    :return:
    '''
    return render(requests, "case_add.html")


@login_required
def task_management(requests):
    '''
    任务管理页面
    :param requests:
    :return:
    '''
    return render(requests, "task_management.html")


@login_required
def mock_server(requests):
    '''
    mock_server
    :param requests:
    :return:
    '''
    return render(requests, "mock_server.html")


@login_required
def test_tools(requests):
    '''
    测试工具页面
    :param requests:
    :return:
    '''
    return render(requests, "test_tools.html")


def logout(request):
    '''
    退出登录状态
    :param request:
    :return:
    '''
    auth.logout(request)
    return HttpResponseRedirect("/index/")
