from django.db import models
from datetime import datetime
from users.models import UserProfile
from courses.models import Course


# Create your models here.

# 用户我要学习表单
class UserAsk(models.Model):
	name = models.CharField(max_length=20, verbose_name='姓名')
	mobile = models.CharField(max_length=11, verbose_name='手机')
	course_name = models.CharField(max_length=50, verbose_name='课程名')
	add_time = models.TimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name = '用户咨询'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name + ' 咨询 ' + self.course_name


# 用户对于课程评论
class CourseComments(models.Model):
	"""
	课程评论
	"""
	# 会涉及两个外键: 1. 用户， 2. 课程。import进来
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
	course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
	comments = models.CharField(max_length=200, verbose_name='评论')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name = '课程评论'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.user.username + ' 评论' + self.course.name


# 用户对于课程,机构，讲师的收藏
class UserFavorite(models.Model):
	# 会涉及四个外键。用户，课程，机构，讲师import
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
	fav_id = models.IntegerField(default=0, verbose_name='数据id')
	fav_type = models.IntegerField(choices=((1, '课程'), (2, '课程机构'), (3, '讲师')), default=1, verbose_name='收藏类型')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name = '用户收藏'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.user.username + ' 收藏'


# 用户消息
class UserMessage(models.Model):
	# 因为我们的消息有两种:发给全员和发给某一个用户。
	# 所以如果使用外键，每个消息会对应要有用户。很难实现全员消息。
	# 为0发给所有用户，不为0就是发给用户的id
	user = models.IntegerField(default=0, verbose_name='接收用户')
	message = models.CharField(max_length=500, verbose_name='消息内容')
	has_read = models.BooleanField(default=False, verbose_name='是否已读')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name = '用户消息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.message


# 用户学习课程
class UserCourse(models.Model):
	# 会涉及两个外键: 1. 用户， 2. 课程。import进来
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
	course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name = '用户课程'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.user.username + ' 学习 ' + self.course.name
