
from django.conf.urls import include, url    # 包含url和url映射
from app01 import views

# 处理媒体文件
from django.views.static import serve
import os
from django.conf import settings
from django.urls import path, re_path

# 路由（url）映射表
# 一个url对应一个视图函数

app_name = '[student_manage]'
urlpatterns = [
    # 注意：如果还要写其他路径，就不要加开始符号
    url('^$', views.index),
    url(r'home_page$', views.home_page, name='home_page'),

    url(r'login$', views.login, name='login'),
    url(r'register$', views.register, name='register'),
    url(r'logout$', views.logout, name='logout'),

    # url(r'model$', views.model),

    url(r'bootcss$', views.bootcss, name='index'),
    url(r'manage$', views.manage, name='manage'),
    url(r'config$', views.config, name='config'),
    url(r'other$', views.other, name='other'),
    url(r'class_add$', views.ClassAdd.as_view(), name='class_add'),
    url(r'cla$', views.ClassManage.as_view(), name='cla'),
    url(r'del$', views.del_stu, name='del'),
    url(r'update$', views.update_stu, name='update'),
    url(r'del_class$', views.del_class, name='del_class'),
]
