# -*-coding: utf-8 -*-
_author_ = 'HBL'
_date_ = '2020/2/28 9:49'

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
	# 用户名和密码不能为空
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, min_length=5)  # 设置必填，最小长度5，不符合不去查数据库。


class RegisterForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True, min_length=5)
	captcha = CaptchaField()


class ForgetForm(forms.Form):
	email = forms.EmailField(required=True)
	captcha = CaptchaField()


class ModifyPwdForm(forms.Form):
	password1 = forms.CharField(required=True, min_length=5)
	password2 = forms.CharField(required=True, min_length=5)
