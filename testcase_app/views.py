from django.shortcuts import render
from django.http import JsonResponse
from testcase_app.models import TestCase
import requests, json


# Create your views here.

def testcase_manage(request):
    return render(request, "Interface_case.html", {"type": "debug"})


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
        par_text = request.POST.get("par_text", "")
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
                                parameter_body=par_text,
                                assert_type=assert_number,
                                assert_text=assert_text)
        return JsonResponse({"status": 10200, "result": "创建成功"})

    else:
        return JsonResponse({"result": "请求错误"})
