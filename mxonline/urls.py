"""mxonline URL Configuration

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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve

from users.views import LoginView, RegisterView, AciveUserView, ForgetPwdView, ResetView, ModifyPwdView
from organization.views import OrgView
from mxonline.settings import MEDIA_ROOT

urlpatterns = (

	path('xadmin/', xadmin.site.urls),  # xadmin
	# 直接调用HTML页面TemplateView.as_view(template_name='index.html')
	path('', TemplateView.as_view(template_name='index.html'), name='index'),
	# 基于类方法实现登录,这里是调用它的方法
	path('login/', LoginView.as_view(), name='login'),  # 登录
	path('register/', RegisterView.as_view(), name='register'),  # 注册
	path(r'captcha/', include('captcha.urls')),  # 验证码就这么写
	# re_path('active/(?P<active_code>.*)获取active/后所有参数当做参数，参数名为active_code
	re_path('active/(?P<active_code>.*)/', AciveUserView.as_view(), name='user_active'),  # 激活用户
	path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),  # 忘记密码
	re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),  # 重置密码get方法
	path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),  # 重置密码post方法

	# 课程机构首页
	path('org_list/', OrgView.as_view(), name='org_list'),

	# 配置上传文件的访问处理函数
	re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT})
)
