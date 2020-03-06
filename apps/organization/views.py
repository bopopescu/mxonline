from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict


# Create your views here.

class OrgView(View):
	def get(self, request):
		# 课程机构
		all_orgs = CourseOrg.objects.all()

		# 城市
		all_citys = CityDict.objects.all()

		# 机构类别
		all_category = list(map(lambda x: {'code': x[0], 'explain': x[1]}, CourseOrg.choices))

		# 处理城市筛选，取回的是city的ID
		city_id = request.GET.get('city', '')
		if city_id:
			all_orgs = all_orgs.filter(city_id=city_id)

		# 处理类别筛选，取回的是字符串
		category = request.GET.get('category', '')
		if category:
			all_orgs = all_orgs.filter(category=category)

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

		return render(request, 'org-list.html', {
			# 在html中遍历（for org inall_orgs.object_list）取出要用的值
			'all_orgs': all_orgs,
			'all_citys': all_citys,
			'org_nums': org_nums,
			'city_id': city_id,  # 传进来的城市id

			'all_category': all_category,  # 机构类别
			'category_id':category # 传进来的类别id
		})
