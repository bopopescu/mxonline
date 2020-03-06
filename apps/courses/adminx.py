# -*-coding: utf-8 -*-
_author_ = 'HBL'
_date_ = '2020/2/27 13:39'

from .models import *

import xadmin


# 创建admin的管理类,这里不再是继承admin，而是继承object
# Course的admin管理器
class CourseAdmin(object):
	# 配置后台需要显示的列
	list_display = [
		'name',
		'desc',
		'detail',
		'degree',
		'learn_times',
		'students',
		'fav_nums',
		'image',
		'click_nums',
		'add_time']

	# 配置搜索字段,不做时间搜索
	search_fields = [
		'name',
		'desc',
		'detail',
		'degree',
		'learn_times',
		'students',
		'fav_nums',
		'image',
		'click_nums']
	# 配置筛选字段---过滤器
	list_filter = [
		'name',
		'desc',
		'detail',
		'degree',
		'learn_times',
		'students',
		'fav_nums',
		'image',
		'click_nums',
		'add_time']


class LessonAdmin(object):
	list_display = ['course', 'name', 'add_time']
	search_fields = ['course', 'name']
	list_filter = ['course', 'name', 'add_time']


class VideoAdmin(object):
	list_display = ['lesson', 'name', 'add_time']
	search_fields = ['lesson', 'name']
	list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
	list_display = ['course', 'name', 'download', 'add_time']
	search_fields = ['course', 'name', 'download']
	list_filter = ['course', 'name', 'download', 'add_time']

# 将管理器与model进行注册关联
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
