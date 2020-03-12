# -*-coding: utf-8 -*-
_author_ = 'HBL'
_date_ = '2020/3/6 15:57'
from django import forms

from operation.models import UserAsk
import re


# 继承ModelForm进行表单验证
class UserAskForm(forms.ModelForm):
	class Meta:
		# 继承UserAsk
		model = UserAsk

		# 选取要比对的属性
		fields = ['name', 'mobile', 'course_name']

	# 要以clean开头加_属性名调用userask_form.is_valid()方法时会自动执行自己写的验证方法
	def clean_mobile(self):
		mobile = self.cleaned_data['mobile']
		REGEX_MOBILE = "^1[345678]\d{9}$|^147\d{8}$|^176\d{8}$"
		p = re.compile(REGEX_MOBILE)
		if p.match(mobile):
			return mobile
		else:
			raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")
