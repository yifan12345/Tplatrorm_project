from django.shortcuts import render
from django.http import JsonResponse
from testcase_app.models import TestCase
from moudle_app.models import Module
import requests, json


# Create your views here.

def testcase_manage(request):
    '''
    用例列表
    :param request:
    :return:
    '''
    case_list = TestCase.objects.all()
    return render(request, "case_list.html", {"type": "list", "cases": case_list})


def add_case(request):
    '''
    添加用例
    :param request:
    :return:
    '''
    return render(request, "case_add.html")


def case_delete(request):
    pass


def case_edit(request, cid):
    '''
    编辑用例
    :param request:
    :return:
    '''
    return render(request, "case_edit.html")


def debug(request):
    '''
    用例调试
    :param request:
    :return:
    '''
    if request.method == "POST":
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        header = request.POST.get("header", "")
        type_ = request.POST.get("type_", "")
        parameter = request.POST.get("parameter", "")
        retu_test = None
        if method == "get":
            if header == "":
                r = requests.get(url=url, params=parameter)
                retu_test = r.text
            else:
                try:
                    r = requests.get(url=url, params=parameter, headers=header)
                    retu_test = r.text
                except AttributeError:
                    retu_test = "暂时不支持header类型的请求"
        if method == "post":
            if type_ == "form":
                if header == "":
                    r = requests.post(url=url, data=parameter)
                    retu_test = r.text
                else:
                    try:
                        r = requests.post(url=url, data=parameter, headers=header)
                        retu_test = r.text
                    except AttributeError:
                        retu_test = "暂时不支持header类型的请求"
            if type_ == "json":
                if header == "":
                    r = requests.post(url=url, json=parameter)
                    retu_test = r.text
                else:
                    try:
                        r = requests.post(url=url, json=parameter, headers=header)
                        retu_test = r.text
                    except AttributeError:
                        retu_test = "暂时不支持header类型的请求"
        return JsonResponse({"result": retu_test})
    else:
        return JsonResponse({"result": "qwe"})


def assert_result(request):
    '''
    用例断言
    :param request:
    :return:
    '''
    if request.method == "POST":
        result_text = request.POST.get("result")
        assert_text = request.POST.get("assert")
        assert_type = request.POST.get("assert_type")

        if result_text == "" or assert_text == "":
            return JsonResponse({"result": "断言文本不能为空"})
        print("断言类型" + assert_type)

        if assert_type == "Contains":
            if assert_text in result_text:
                return JsonResponse({"result": "断言通过"})
            else:
                return JsonResponse({"result": "断言失败"})
        elif assert_type == "Mathches":
            if assert_text == result_text:
                return JsonResponse({"result": "断言通过"})
            else:
                return JsonResponse({"result": "断言失败"})
    else:
        return JsonResponse({"result": "请求错误"})


def save_case(request):
    '''
    用例保存
    :param request:
    :return:
    '''
    if request.method == "POST":
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        header = request.POST.get("header", "")
        par_type = request.POST.get("par_type", "")
        par_body = request.POST.get("par_body", "")
        assert_type = request.POST.get("assert_type", "")
        assert_text = request.POST.get("assert_text", "")
        module_id = request.POST.get("mid", "")
        name = request.POST.get("name", "")
        if url == "":
            return JsonResponse({"status": 10101, "message": "URL不能为空"})
        if name == "":
            return JsonResponse({"status": 10101, "message": "用例名称不能为空"})
        if module_id == "":
            return JsonResponse({"status": 10101, "message": "所属模块ID不能为空"})
        if assert_type == "" or assert_text == "":
            return JsonResponse({"status": 10200, "message": "断言类型不能为空"})

        if method == "get":
            method_number = 1
        elif method == "post":
            method_number = 2
        elif method == "delete":
            method_number = 3
        elif method == "put":
            method_number = 4
        else:
            return JsonResponse({"status": 10104, "message": "未知的请求方法"})

        if par_type == "form":
            parameter_number = 1
        elif par_type == "json":
            parameter_number = 2
        else:
            return JsonResponse({"status": 10104, "message": "未知的参数类型"})

        if assert_type == "Contains":
            assert_number = 1
        elif assert_type == "Mathches":
            assert_number = 2
        else:
            return JsonResponse({"status": 10104, "message": "未知的断言类型"})

        TestCase.objects.create(name=name, url=url,
                                module_id=module_id,
                                method=method_number,
                                header=header,
                                parameter_type=parameter_number,
                                parameter_body=par_body,
                                assert_type=assert_number,
                                assert_text=assert_text)
        return JsonResponse({"status": 10200, "result": "创建成功"})

    else:
        return JsonResponse({"result": "请求错误"})


def get_case_info(request):
    '''
    获取接口数据
    :param request:
    :return:
     header = models.TextField("请求头", null=False)
    parameter_type = models.IntegerField("参数类型", null=False)  # 1:form_data,2:json
    parameter_body = models.TextField("参数内容", null=False)
    result = models.TextField("结果", null=False)
    assert_type = models.IntegerField("断言类型", null=False)  # 1:包含，2：匹配
    assert_text = models.TextField("断言结果", null=False)
    creat_time = models.DateTimeField("创建时间", auto_now_add=True)

    '''

    if request.method == "POST":
        cid = request.POST.get("cid", "")
        case = TestCase.objects.get(id=cid)
        module = Module.objects.get(id=case.module.id)
        project_id = module.project.id
        case_dict = {
            "id": case.id,
            "url": case.url,
            "case_name": case.name,
            "method": case.method,
            "header": case.header,
            "par_type": case.parameter_type,
            "par_body": case.parameter_body,
            "assert_type": case.assert_type,
            "assert_text": case.assert_text,
            "module_id": case.module.id,
            "project_id":project_id,

        }
        return JsonResponse({"status": 10200, "massage": "请求成功", "data": case_dict})
    else:
        return JsonResponse({"status": 10101, "massage": "请求失败"})
