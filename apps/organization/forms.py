# -*-coding: utf-8 -*-
_author_ = 'HBL'
_date_ = '2020/3/6 15:57'
from django import forms

from operation.models import UserAsk


# 继承ModelForm进行表单验证
class UserAskForm(forms.ModelForm):
	class Meta:
		# 继承UserAsk
		model = UserAsk

		# 选取要比对的属性
		fields = ['name', 'mobile', 'course_name']
