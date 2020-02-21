from django.shortcuts import render, HttpResponse
import datetime

# Create your views here,


def index(request):    # request获取http 请求信息
    return HttpResponse('hello, 你好')    # 响应的基类， 响应一段字符串


def test(request):
    print(request.user)     # 获取请求用户（没有登陆就是匿名用户）
    print(request.path)     # 请求路径
    print(request.get_full_path())    # 请求的uri（路径+查询参数）
    print(request.get_host())     # 主机地址
    print(request.method)         # 请求方法
    print(request.GET)     # 获取get的查询参数
    return HttpResponse("This is test page!!!")


def test1(request, id1, id2, id3):
    # print(id1, id2, id3)
    return HttpResponse("This is test1 page  !!!")


def get_time(request):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(now_time)
