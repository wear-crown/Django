"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url    # 包含url和url映射

from app00.views import index, test, get_time, test1   # 导入视图函数

# 对于显示静态文件非常重要
from django.conf import settings
from django.conf.urls.static import static

# 导入app01中的url
from app01 import urls as app01_urls

# 路由（url）映射表
# 一个url对应一个视图函数
urlpatterns = [
    url('admin/', admin.site.urls),
    # url('^$', index),
    # # name参数可以给url起别名， 在模板中和视图中可以通过别名获取url
    # url('^test/$', test, name='test_page'),      # 加上  /  较好
    # url('^get_time/$', get_time, name='get_time'),
    # # url(r'^test1/(\d+)/(\d+)/(\w+)/$', test1),
    # url(r'^test1/(?P<id1>\d+)/(?P<id2>\d+)/(?P<id3>\w+)/$', test1),


    # 下面是url分发
    # 注意：不要写结束符号
    # url('^app01', include(app01_urls)),
    # 命名空间加上namespace
    url('^app01/', include(app01_urls, namespace='student_manage')),

    # 媒体文件处理
    # url(r'^upload/(.*)', serve, {"document_root": os.path.join(settings.MEDIA_ROOT, 'upload')}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
