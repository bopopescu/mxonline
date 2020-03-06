# -*-coding: utf-8 -*-
_author_ = 'HBL'
_date_ = '2020/3/3 13:34'
from random import Random
from django.core.mail import send_mail
from mxonline.settings import EMAIL_FROM

from users.models import EmailVerifyRecord


# 生成随机字符串
def random_str(randomlength=8):
	str = ''
	# 生成字符串的可选字符串
	chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str += chars[random.randint(0, length)]
	return str


# 发送注册邮件
def send_register_email(email, send_type='register'):
	# 发送之前先保存到数据库，到时候查询链接是否存在

	# 实例化一个EmailVerifyRecord对象
	email_record = EmailVerifyRecord()
	# 生成随机的code放入链接
	code = random_str(16)
	email_record.code = code
	email_record.email = email
	email_record.send_type = send_type
	email_record.save()

	# 定义邮件内容
	email_title = ''
	email_body = ''

	if send_type == 'register':
		email_title = '慕学在线网站注册激活连接'
		# request_uri='http://127.0.0.1:8000/register/'
		email_body = '请点击下方的链接激活你的账户：http://127.0.0.1:8000/active/{0}'.format(code)

		# 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
		send_staus = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_staus:
			pass
	elif send_type == 'forget':
		email_title = '慕学在线网找回密码连接'
		email_body = '请点击下方的链接找回密码：http://127.0.0.1:8000/reset/{0}'.format(code)

		send_staus = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_staus:
			pass
