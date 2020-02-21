# coding:utf8
import os
from audioop import reverse

from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required    # 导入登录验证
from django.views.generic import View, ListView   # 视图基类
from datetime import datetime
import hashlib
# 导入模型
from app01 import models

from django.conf import settings

# 创建模板对象
from django.template import Template, Context

# 导入分页类
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# Create your views here.


def index(request):
    return HttpResponse('app01 page')


def home_page(request):
    context = {
        'username_now': username_now,
    }
    return render(request, 'bootcss/home_page.html', context)


# 设置全局变量username_now保存当前登录的用户
def login(request):
    global username_now
    print("login访问时间点：%s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    if request.method =='GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        context = {
            'message': ''
        }
        # 用户提交表单
        username = request.POST.get('username')
        username_now = username
        password = request.POST.get('password')
        user = models.User.objects.filter(name=username).first()
        if user:
            if user.password == password:
                context['message'] = '登录成功'
                # 服务器设置sessionid和其他用户信息。sessionid(服务器给访问它的浏览器的身份证)自动生成的
                request.session['is_login'] = True
                request.session['username'] = user.name
                request.session['user_id'] = user.id
                return HttpResponseRedirect('http://127.0.0.1:8000/app01/home_page')
            else:
                context['message'] = '密码错误，请重新输入'
                return render(request, 'login.html', context=context)
        else:
            context['message'] = '用户未注册，请先进行注册'
            return render(request, 'login.html', context=context)
    # return redirect('/index/')


# 用户注册
def register(request):
    if request.method =='GET':
        # 注册表单
        # 写数据库
        return render(request, 'register.html')
    elif request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # 简单后端表单验证（正则最合适）
        # 写入数据库
        # 相当于 'insert into login_user(name,password,email) values(%s,%s,%s)'% ('','','')
        user = models.User.objects.filter(email=email).first()
        if user:
            return render(request, 'register.html', context={'message': '用户已经注册,点击此处去登录界面'})
        # 加密密码
        hash_password = _hash_password(password)
        try:
            user = models.User(name=username, password=password, hash_password=hash_password, email=email)
            user.save()
            print('注册成功')
            return render(request, 'register.html', context={'message': '注册成功,去登录页面'})
        except Exception as e:
            print('注册失败')
            return redirect('app01/register/', context={'message': '注册失败'})


def logout(request):
    # 清除session 登出
    request.session.flush()  # 清除此用户sessionid 对应的所有sessiondata

    return HttpResponseRedirect('http://127.0.0.1:8000/app01/login')


def _hash_password(password):
    sha = hashlib.sha256()
    sha.update(password.encode('utf-8'))
    return sha.hexdigest()


def upload_avatar(file):
    file_type = file.content_type
    file_name = file.name
    file_size = file.size

    if file_size/1024/1024 < 2:    # 文件大小小于2兆
        if file_type == 'image/jpg' or file_type == 'image/png' or file_type == 'image/jpeg':
            filepath = os.path.join(settings.BASE_DIR, 'upload') + '/avatar/' + file_name
            # 数据库中存的路径
            dbpath = 'avatar/' + file_name
            with open(filepath, 'wb') as f:
                # 读取文件
                file_content = file.read()
                f.write(file_content)
            return True, '上传成功', dbpath
        else:
            return False, '照片格式不正确'
    else:
        return False, '照片不能超过2M'


# 添加学生
def bootcss(request):
    context = {
        'bootcss': 'active'
    }
    if request.method == "POST":
        number = request.POST['number']
        name = request.POST['name']
        age = request.POST['age']
        score = request.POST['score']
        cls = request.POST['cls']
        email = request.POST['email']
        avatar = request.FILES.get('avatar')
        result = upload_avatar(avatar)
        if result[0] is True:    # 判断文件是否上传成功
            try:
                models.Student.objects.create(number=number, name=name, age=age, score=score, cls_id=cls,
                                              email=email, avatar=result[2])
            except Exception:
                return render(request, 'bootcss/Dashboard .html', {'error': '数据填写错误，请重新填写'})
            return render(request, 'bootcss/Dashboard .html', context)
        else:
            return render(request, 'bootcss/Dashboard .html', {'error': result[1]})
    elif request.method == "GET":
        classes = models.Class.objects.all()
        text = {
            'bootcss': 'active',
            'classes': classes,
        }
        return render(request, 'bootcss/Dashboard .html', text)


# 学生管理
def manage(request):
    # 搜索字段
    keyword = request.GET.get('keyword', '')

    # 获取排序字段
    order = request.GET.get('order', None)
    ruler = request.GET.get('ruler', None)

    # 获取分页字段
    pn = request.GET.get('pn', None)
    if pn:
        pn = int(pn)
    else:
        pn = 1
    print('page 参数为：', pn)

    if keyword is not None:
        # 忽略大小写的模糊查询
        stu1 = models.Student.objects.filter(name__icontains=keyword).all()
        stu2 = models.Student.objects.filter(number__icontains=keyword).all()
        stu3 = models.Student.objects.filter(age__icontains=keyword).all()
        stu4 = models.Student.objects.filter(score__icontains=keyword).all()
        # 集合的使用
        stuinfo_list_obj = stu1 | stu2 | stu3 | stu4
    else:  # 获取所有
        stuinfo_list_obj = models.Student.objects.all()

    # 排序
    if order is not None:  # 排序字段不为空
        if order == '':
            order = 'number'
        if ruler == 'up':  # 升序
            stuinfo_list_obj = stuinfo_list_obj.order_by(order)
        elif ruler == 'down':
            stuinfo_list_obj = stuinfo_list_obj.order_by('-' + order)

    # 分页
    # 获取每页记录条数
    per_page = request.COOKIES.get('per_page', 5)
    per_page = int(per_page)
    paginator = Paginator(stuinfo_list_obj, per_page)    # a1:查询结果集 a2:每页显示记录数
    # 获得列表被分页处理后，总共被分为多少页
    page_num = paginator.num_pages
    print(page_num)

    # 显示5个数字，当前页放在中间
    if page_num > 5:
        if pn <= 2:
            start = 1
            end = 6
        elif pn > page_num - 2:
            start = page_num - 4
            end = page_num + 1
        else:
            start = pn - 2
            end = pn + 3
    else:
        start = 1
        end = page_num + 1
    page_number = range(start, end)

    try:
        stuinfo_list_obj = paginator.page(pn)   # 获取某一页
    except (EmptyPage, InvalidPage, PageNotAnInteger) as e:
        pn = 1
        stuinfo_list_obj = paginator.page(pn)  # 获取某一页
    # 判断是否存在下一页
    if stuinfo_list_obj.has_next():
        next_page = pn + 1
    else:
        next_page = pn
    # 是否存在上一页
    if stuinfo_list_obj.has_previous():
        previous_page = pn - 1
    else:
        previous_page = pn

    context = {
        'manage': 'active',
        'stuinfo_list': stuinfo_list_obj,
        'keyword': keyword,
        'next_page': next_page,
        'previous_page': previous_page,
        'page_num': page_num,
        'page_number': page_number,
        'pn': pn,
    }
    return render(request, 'bootcss/manage.html', context)


# 系统配置
def config(request):
    per_page = request.GET.get('per_page', None)    # 获取用户提交配置项
    if per_page is None:
        context = {
            'config': 'active'
        }
        return render(request, 'bootcss/config.html', context)
    else:   # per_page  存在
        rep = HttpResponseRedirect('http://127.0.0.1:8000/app01/config')
        rep.set_cookie('per_page', per_page, max_age=3600*24*365)   # 设置一个长时间有效的cookies
        return rep


def other(request):
    context = {
        'other': 'active'
    }
    return render(request, 'bootcss/other.html', context)


def del_stu(request):
    # 获取学生学号
    id = request.GET.get('id')
    models.Student.objects.filter(id=id).delete()
    return HttpResponseRedirect('http://127.0.0.1:8000/app01/manage')


# 设置一个全局变量保存 id
def update_stu(request):
    if request.method == 'GET':
        classes = models.Class.objects.all()
        id = request.GET.get('id')
        global stu_id
        stu_id = id
        stu_detail = models.Student.objects.get(id=id)
        context = {
            'stu_detail': stu_detail,
            'classes': classes
        }
        return render(request, 'bootcss/update.html', context=context)
    if request.method == "POST":
        number = request.POST['number']
        name = request.POST['name']
        age = request.POST['age']
        score = request.POST['score']
        cls = request.POST['cls']
        email = request.POST['email']
        avatar = request.FILES.get('avatar')
        result = upload_avatar(avatar)
        if result[0] is True:  # 判断文件是否上传成功
            try:
                models.Student.objects.filter(id=stu_id).update(number=number, name=name, age=age, score=score,
                                                                cls_id=cls,
                                                                email=email, avatar=result[2])
            except Exception:
                return render(request, 'bootcss/update.html', {'error': '数据填写错误，请重新填写'})

            return HttpResponseRedirect('http://127.0.0.1:8000/app01/manage')
        else:
            return render(request, 'bootcss/update.html', {'error': result[1]})


# 班级添加
class ClassAdd(View):
    # 直接处理GET请求
    def get(self, request):
        context = {
            'class_add': 'active'
        }
        return render(request, 'bootcss/class_add.html', context)

    # 处理POST请求
    def post(self, request):
        name = request.POST.get('name', None)
        if name is not None and name != '':
            models.Class.objects.create(name=name)
            return render(request, 'bootcss/class_add.html')
        else:
            return render(request, 'bootcss/class_add.html', {'error': '班级名不能为空'})


# 班级管理
# class ClassManage(View):
#     def get(self, request):
#         context = {
#             'cla': 'active'
#         }
#         return render(request, 'bootcss/cla.html', context)
#
#     def post(self, request):
#         pass

# 视图列表
class ClassManage(ListView):
    # 自动渲染模板
    template_name = 'bootcss/cla.html'
    context_object_name = 'class_list'

    def get_queryset(self):   # 需要返回查询数据集
        return models.Class.objects.all()

    # 自定义模板变量
    def get_context_data(self, *, object_list=None, **kwargs):
        # 重写方法， 生成上下文对象
        context = super(ClassManage, self).get_context_data(**kwargs)
        context['cla'] = 'active'
        return context


# 班级的删除
def del_class(request):
    # 获取班级name
    name = request.GET.get('name')
    models.Class.objects.filter(name=name).delete()
    return HttpResponseRedirect('http://127.0.0.1:8000/app01/cla')


