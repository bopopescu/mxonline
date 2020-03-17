import json

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
from .forms import UserAskForm

from operation.models import UserFavorite


# Create your views here.
# 显示课程机构列表
class OrgView(View):
	"""
	显示课程机构列表
	"""

	def get(self, request):
		# 课程机构
		all_orgs = CourseOrg.objects.all()

		# 热门机构排名取前3个变量前要加-号
		hot_orgs = all_orgs.order_by('-click_nums')[:3]

		# 城市
		all_citys = CityDict.objects.all()

		# 机构类别
		all_category = list(map(lambda x: {'code': x[0], 'explain': x[1]}, CourseOrg.choices))

		# 处理城市筛选，取回的是city的ID
		city_id = request.GET.get('city', '')
		if city_id:
			all_orgs = all_orgs.filter(city_id=city_id)

		# 处理类别筛选，取回的是字符串
		category_id = request.GET.get('category', '')
		if category_id:
			all_orgs = all_orgs.filter(category=category_id)

		# 学习人数和课程数排名
		sort = request.GET.get('sort', '')
		if sort:
			if sort == 'students':
				all_orgs = all_orgs.order_by('-students')
			elif sort == 'courses':
				all_orgs = all_orgs.order_by('-course_nums')

		# 机构数量
		org_nums = all_orgs.count()

		# 对课程机构进行分页
		# 尝试获取前台get请求传递过来的page参数
		# 如果是不合法的配置参数默认返回第一页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		# 从列表中取5个出来，也就是每页显示5个
		p = Paginator(all_orgs, 5, request=request)
		all_orgs = p.page(page)

		return render(request, 'org-list.html',
		              # {
		              #    # 在html中遍历（for org inall_orgs.object_list）取出要用的值
		              #    # 'all_orgs': all_orgs,
		              #    # 'all_citys': all_citys,
		              #    # 'org_nums': org_nums,
		              #    # 'city_id': city_id,  # 传进来的城市id
		              #    #
		              #    # 'all_category': all_category,  # 机构类别
		              #    # 'category_id': category_id,  # 传进来的类别id
		              #    # 'hot_orgs': hot_orgs,  # 热门机构排名
		              #    # 'sort': sort  # 学习人数和课程数排名
		              # }
		              locals()
		              )


# 用户添加我要学习视图
class AddUserAskView(View):
	def post(self, request):
		userask_form = UserAskForm(request.POST)
		# 判断form是否有效
		if userask_form.is_valid():
			# 这里是modelform和form的区别
			# 它有model的属性
			# 当commit为true进行真正保存
			user_ask = userask_form.save(commit=True)
			# 这样就不需要把一个一个字段取出来然后存到model的对象中之后save
			# 如果保存成功,返回json字符串,后面content type是告诉浏览器的
			# 返回json字符串需使用方法转换json.dumps({字典，字典，..})
			return HttpResponse(json.dumps({'status123': 'success', 'msg': '添加成功'}), content_type='application/json')
		# return JsonResponse("{'status123':'success'}", self=None)

		else:
			return HttpResponse(
				json.dumps({'status123': 'fail', 'msg': '添加出错'}),
				content_type='application/json')


# 机构首页
class OrgHomeView(View):
	"""
	机构首页
	"""

	def get(self, request, org_id):
		# 判断导航栏选中
		current_page = "home"
		# 通过传过来的机构di查找机构
		course_org = CourseOrg.objects.get(id=int(org_id))

		# 用户收藏状态
		has_fav = False
		# 用户收藏状态
		has_fav = False
		# 判断用户是否登录
		if request.user.is_authenticated:
			# 判断用户收藏记录是否存在
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
				# 存储收藏状态变成True
				has_fav = True

		# 通过course课程modes里设置的外键
		# org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所属机构')
		# 可以让course_org反向找出机构下所有课程内容
		all_courses = course_org.course_set.all()[:3]

		# 通过Teacher教师modes里设置的外键
		# org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所属机构')
		# 可以让course_org反向找出机构下所有教师
		all_teachers = course_org.teacher_set.all()[:2]

		return render(request, 'org-detail-homepage.html', {
			'all_courses': all_courses,
			'all_teachers': all_teachers,
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav,
		})


# 机构简介
class OrgDescView(View):
	"""
	机构简介
	"""

	def get(self, request, org_id):
		# 判断导航栏选中
		current_page = "desc"

		# 通过传过来的机构di查找机构
		course_org = CourseOrg.objects.get(id=int(org_id))

		# 用户收藏状态
		has_fav = False
		# 判断用户是否登录
		if request.user.is_authenticated:
			# 判断用户收藏记录是否存在
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
				# 存储收藏状态变成True
				has_fav = True

		return render(request, 'org-detail-desc.html', {

			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav,
		})


# 机构讲师
class OrgTeacherView(View):
	"""
	机构讲师
	"""

	def get(self, request, org_id):
		# 判断导航栏选中
		current_page = "teacher"

		# 通过传过来的机构di查找机构
		course_org = CourseOrg.objects.get(id=int(org_id))
		# 查找出机构下所有讲师
		all_teachers = course_org.teacher_set.all()

		# 用户收藏状态
		has_fav = False
		# 判断用户是否登录
		if request.user.is_authenticated:
			# 判断用户收藏记录是否存在
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
				# 存储收藏状态变成True
				has_fav = True

		return render(request, 'org-detail-teachers.html', {
			'all_teachers': all_teachers,
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav,
		})


# 机构课程
class OrgCourseView(View):
	"""
	机构课程
	"""

	def get(self, request, org_id):
		# 判断导航栏选中
		current_page = "course"

		# 通过传过来的机构di查找机构
		course_org = CourseOrg.objects.get(id=int(org_id))
		# 查找出机构下所有课程
		all_courses = course_org.course_set.all()

		# 用户收藏状态
		has_fav = False
		# 判断用户是否登录
		if request.user.is_authenticated:
			# 判断用户收藏记录是否存在
			if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
				# 存储收藏状态变成True
				has_fav = True

		return render(request, 'org-detail-course.html', {
			'all_courses': all_courses,
			'course_org': course_org,
			'current_page': current_page,
			'has_fav': has_fav,
		})


# 用户收藏机构，用户取消收藏
class AddFavView(View):
	"""
	用户收藏机构，用户取消收藏
	"""

	def post(self, request):
		fav_id = request.POST.get('fav_id', '')
		fav_type = request.POST.get('fav_type', '')

		if not request.user.is_authenticated:
			# 判断用户登录状态
			return HttpResponse(
				json.dumps({'status123': 'user_none', 'msg': '用户未登录请登录'}),
				content_type='application/json')
		# 查找用户对应收藏是否存在
		exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
		if exist_records:
			# 存在删除收藏
			exist_records.delete()

			return HttpResponse(
				json.dumps({'status123': 'fail', 'msg': '收藏'}),
				content_type='application/json')
		else:
			# 不存在添加收藏
			user_fav = UserFavorite()
			if int(fav_id) > 0 and int(fav_type) > 0:
				user_fav.fav_id = int(fav_id)
				user_fav.fav_type = int(fav_type)
				user_fav.user = request.user
				user_fav.save()
				return HttpResponse(
					json.dumps({'status123': 'fail', 'msg': '已收藏'}),
					content_type='application/json')
			else:
				return HttpResponse(
					json.dumps({'status123': 'fail', 'msg': '收藏出错'}),
					content_type='application/json')
