import json

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
from .forms import UserAskForm


# Create your views here.

class OrgView(View):
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
