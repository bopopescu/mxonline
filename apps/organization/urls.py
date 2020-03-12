# -*-coding: utf-8 -*-
_author_ = 'HBL'
_date_ = '2020/3/6 16:05'

from django.urls import path

from .views import OrgView, AddUserAskView

app_name = 'organization'
urlpatterns = (

	# 课程机构首页
	path('list/', OrgView.as_view(), name='list'),

	path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
)
