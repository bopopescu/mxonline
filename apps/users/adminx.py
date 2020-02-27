# -*-coding: utf-8 -*-
_author_ = 'HBL'
_date_ = '2020/2/27 13:22'

import xadmin

from .models import EmailVerifyRecord, Banner
from xadmin import views


# TIP 定义页头页脚
class GlobalSettings(object):
	site_title = '慕学后台管理系统'
	site_footer = '慕学在线网'
	menu_style = 'accordion'  # 左侧导航折叠筐


class BaseSetting(object):
	enable_themes = True
	use_bootswatch = True


class EmailVerifyRecordAdmin(object):
	list_display = ['code', 'email', 'send_type', 'send_time']
	search_fields = ['code', 'email', 'send_type']
	list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
	list_display = ['title', 'image', 'url', 'indx', 'add_time']
	search_fields = ['title', 'image', 'url', 'indx']
	list_filter = ['title', 'image', 'url', 'indx', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)  # 注册到xadmin中
xadmin.site.register(views.CommAdminView, GlobalSettings)  # 注册到xadmin中
