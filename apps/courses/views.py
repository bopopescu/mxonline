import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from operation.models import UserFavorite
from .models import Course


# 课程列表展示
class CourseListView(View):
	"""
	课程列表展示
	"""

	def get(self, request):

		# 取出所以课程 (.order_by("-add_time"))按照添加时间倒序排列取出
		all_courses = Course.objects.all().order_by("-add_time")
		# 热门课程推荐
		hot_courses = Course.objects.all().order_by("-click_nums")[:3]

		sort = request.GET.get('sort', '')
		if sort:
			if sort == "students":
				all_courses = Course.objects.all().order_by("-students")
			elif sort == "click_nums":
				all_courses = Course.objects.all().order_by("-click_nums")

		# 对课程进行分页
		# 尝试获取前台get请求传递过来的page参数
		# 如果是不合法的配置参数默认返回第一页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1

		# 从列表中取几个出来，也就是每页显示几个
		p = Paginator(all_courses, 9, request=request)
		courses = p.page(page)

		return render(request, 'course-list.html', locals())  # locals()区域变量


# 课程详情页
class CourseDetailView(View):
	"""
	课程详情页
	"""

	def get(self, request, course_id):
		# 用课程的ID查找对应课程信息
		course_detail = Course.objects.get(id=course_id)
		# 记录每次浏览的点击数
		course_detail.click_nums += 1
		course_detail.save()
		# 通过点击数推荐课程
		hot_course = (Course.objects.all().order_by('-click_nums')[:1])[0]

		# 用于判断课程是否收藏
		has_fav_course = False
		# 用于判断机构是否收藏
		has_fav_org = False
		# 判断用户是否登录
		if request.user.is_authenticated:
			if UserFavorite.objects.filter(user=request.user, fav_id=course_detail.id, fav_type=1):
				has_fav_course = True

			if UserFavorite.objects.filter(user=request.user, fav_id=course_detail.course_org.id, fav_type=2):
				has_fav_org = True

		# 标签用户找出同一类型的课程
		tag = course_detail.tag
		# 判断是否有同类型课程存在，不存在返回空列表
		if tag:
			same_tag = Course.objects.filter(tag=tag).exclude(id=course_id).order_by('-click_nums')[:1]

		else:
			same_tag = []
		return render(request, 'course-detail.html', locals())
