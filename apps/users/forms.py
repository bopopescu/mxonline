#-*-coding: utf-8 -*-
_author_ = 'HBL'
_date_ = '2020/2/28 9:49'

from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True,min_length=5) #设置必填，最小长度5，不符合不去查数据库。