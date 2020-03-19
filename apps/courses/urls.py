#-*-coding: utf-8 -*-
_author_ = 'HBL'
_date_ = '2020/3/17 16:45'


from django.urls import path, re_path

from .views import CourseListView

app_name = 'course'
urlpatterns = (

	# 课程列表页
	path('list/', CourseListView.as_view(), name='course_list'),

)
