# -*-coding: utf-8 -*-
_author_ = 'HBL'
_date_ = '2020/2/27 14:05'

from .models import *
import xadmin


class CityDictAdmin(object):
	list_display = ['name', 'desc', 'add_time']
	search_fields = ['name', 'desc']
	list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
	list_display = ['city', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'add_time']
	search_fields = ['city', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'address']
	list_filter = ['city', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'add_time']


class TeacherAdmin(object):
	list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
	                'add_time']
	search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
	list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
	               'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
