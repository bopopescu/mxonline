from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course


class CourseListView(View):
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
		p = Paginator(all_courses, 1, request=request)
		courses = p.page(page)

		return render(request, 'course-list.html', locals())
