# -*-coding: utf-8 -*-
_author_ = 'HBL'
_date_ = '2020/3/6 16:05'

from django.urls import path, re_path

from .views import OrgView, AddUserAskView, OrgHomeView, OrgDescView, OrgTeacherView, OrgCourseView, AddFavView

app_name = 'organization'
urlpatterns = (

	# 课程机构列表页
	path('list/', OrgView.as_view(), name='list'),
	# 添加我也学习
	path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
	# 课程机构>机构首页
	re_path('home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
	# 课程机构>机构介绍
	re_path('desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
	# 课程机构>机构讲师
	re_path('teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
	# 课程机构>机构课程
	re_path('course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),

	# 机构收藏
	path('add_fav/', AddFavView.as_view(), name='add_fav'),
)
