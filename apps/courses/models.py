from django.db import models
from datetime import datetime

from organization.models import CourseOrg


# Create your models here.
# 课程信息表
class Course(models.Model):
	course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='课程机构', null=True, blank=True)
	name = models.CharField(max_length=50, verbose_name='课程名')
	desc = models.CharField(max_length=300, verbose_name='课程描述')
	detail = models.TextField(verbose_name='课程详情')
	degree = models.CharField(max_length=2, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')))
	learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟表示）')
	students = models.IntegerField(default=0, verbose_name='学习人数')
	fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
	image = models.ImageField(max_length=100, upload_to='courses/%y/%m', verbose_name='封面图片')
	click_nums = models.IntegerField(default=0, verbose_name='点击数')
	category = models.CharField(default='后端开发', max_length=20, verbose_name='课程类别')
	tag = models.CharField(default='基础知识学习', max_length=20, verbose_name='课程标签')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name = '课程'
		verbose_name_plural = verbose_name

	def get_zj_nums(self):
		# 获取课程章节数量
		return self.lesson_set.all().count()

	def get_learn_users(self):
		# 获取课程章节数量
		return self.usercourse_set.all()[:5]

	def __str__(self):
		return self.name


# 课程章节
class Lesson(models.Model):
	# 在引用外键是要添加on_delete=models.CASCADE否则会报错
	course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
	name = models.CharField(max_length=100, verbose_name='章节名')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name = '章节'
		verbose_name_plural = verbose_name

	def __str__(self):
		return '课程 ' + self.course.name + '的章节：' + self.name


# 课程视频
class Video(models.Model):
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='章节')
	name = models.CharField(max_length=100, verbose_name='视频名')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name = '视频'
		verbose_name_plural = verbose_name


# 课程资源
class CourseResource(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
	name = models.CharField(max_length=100, verbose_name='名称')
	# 下载的是文件，需要用到文件下载FileField，在后台管理中会自动生成文件上传的按钮
	download = models.FileField(max_length=100, upload_to='course/resource/%y/%m', verbose_name='资源文件')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

	class Meta:
		verbose_name = '课程资源'
		verbose_name_plural = verbose_name
