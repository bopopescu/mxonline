from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.

# 用户信息
class UserProfile(AbstractUser):
	nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
	birday = models.DateField(verbose_name='生日', null=True, blank=True)
	gender = models.CharField(
		max_length=6,
		choices=(('male', '男'), ('female', '女')),
		default='female',
		verbose_name="性别")
	address = models.CharField(max_length=100, default='', verbose_name="地址")
	mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
	image = models.ImageField(upload_to='image/%y/%m', default='image/default.png', verbose_name="用户头像")

	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.username


# 邮箱验证码
class EmailVerifyRecord(models.Model):
	code = models.CharField(max_length=20, verbose_name='验证码', null=True)
	email = models.EmailField(max_length=50, verbose_name='邮箱', null=True)
	send_type = models.CharField(verbose_name='验证类型', max_length=10, choices=(('register', '注册'), ('forget', '找回密码')))
	# 这里的now得去掉(), 不去掉会根据编译时间。而不是根据实例化时间
	send_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

	class Meta:
		verbose_name = '邮箱验证码'
		verbose_name_plural = verbose_name

	def __str__(self):
		return '{0}({1})'.format(self.code, self.email)


# 1、图片 2. 点击图片地址 3. 轮播图序号(控制前后)
class Banner(models.Model):
	title = models.CharField(max_length=100, verbose_name='标题')
	image = models.ImageField(max_length=100, upload_to='banner/%y/%m', verbose_name='轮播图')
	url = models.URLField(max_length=200, verbose_name='访问地址')
	indx = models.ImageField(default=100, verbose_name='顺序')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name = '轮播图'
		verbose_name_plural = verbose_name
