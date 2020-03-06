from django.shortcuts import render
# 加载django提供的用户名密码验证方法authenticate login
from django.contrib.auth import authenticate, login
# 加载django提供的ModelBackend方法，用于自定义认证
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
# 调用我们models.py里自己定义的用户表
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, ForgetForm, ModifyPwdForm
from .forms import RegisterForm
from utils.email_send import send_register_email


# 重新复写认证方法
class CustomBackend(ModelBackend):
	"""
	重新复写认证方法
	加入同时可以认证用户名和和邮箱的Q方法
	user = UserProfile.objects.get(Q(username=username) | Q(email=username))
	"""

	# 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username) | Q(email=username))
			# django的后台中密码加密：所以不能password==password
			# UserProfile继承的AbstractUser中有def check_password(self, raw_password)

			if user.check_password(password):  # 数据库中密码进行解密与传进来的password比较
				return user
		except Exception as e:
			return None


# 用户登录视图
class LoginView(View):
	"""
	用户登录
	"""

	def get(self, request):
		return render(request, 'login.html', {})

	def post(self, request):
		login_form = LoginForm(request.POST)  # 调用form方法，验证用户输入 没有错误err属性长度为0
		if login_form.is_valid():
			user_name = request.POST.get('username', '')
			pass_word = request.POST.get('password', '')
			user = authenticate(username=user_name, password=pass_word)  # 认证成功返回user对象，失败返回null
			if user is not None:
				if user.is_active:  # 判断此用户是否应被视为活动用户
					login(request, user)  # 在请求中持久化用户id和后端。这样，用户就不必对每个请求进行重新处理。注意，匿名会话期间的数据集在用户登录时被保留。
					return render(request, 'index.html')
				else:
					return render(request, 'login.html', {'msg': '用户未激活'})
			else:
				return render(request, 'login.html', {'msg': '用户名或密码错误!!!'})
		else:
			return render(request, 'login.html', {'login_form': login_form})


# 用户注册视图
class RegisterView(View):
	"""
	用户注册
	"""

	def get(self, request):
		register_form = RegisterForm()  # 调用form方法，验证用户输入 没有错误err属性长度为0
		return render(request, 'register.html', {'register_form': register_form})

	# get()方法中传递register_form是为了在html中调取register_form验证码属性

	def post(self, request):
		register_form = RegisterForm(request.POST)
		# 调用form方法，验证用户输入 没有错误err属性长度为0
		if register_form.is_valid():
			user_name = request.POST.get('email', '')
			if UserProfile.objects.filter(email=user_name):
				# 查找数据库中UserProfile表中匹配email=user_name的对象
				return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
			pass_word = request.POST.get('password', '')
			user_profile = UserProfile()
			user_profile.username = user_name
			user_profile.email = user_name
			user_profile.password = make_password(pass_word)  # 密码进行加密存入数据库
			user_profile.is_active = False  # 设置用户未激活状态
			user_profile.save()  # 存入数据库

			send_register_email(user_name, 'register')  # 调用发送邮件激活用户

			return render(request, 'login.html', {'msg': '请查收邮件激活用户'})
		else:
			return render(request, 'register.html', {'register_form': register_form})


# 激活用户视图
class AciveUserView(View):
	"""
	激活用户
	"""

	def get(self, request, active_code):
		all_records = EmailVerifyRecord.objects.filter(code=active_code)
		# 查找数据库中EmailVerifyRecord表中匹配code=active_code的对象
		if all_records:
			for record in all_records:
				email = record.email
				user = UserProfile.objects.get(email=email)
				# 查找数据库中UserProfile表中匹配email=email的对象
				user.is_active = True  # 修改用户激活状态
				user.save()
		else:
			return render(request, 'active_fail.html')  # 跳转激活失败页面
		return render(request, 'login.html', {'msg': '用户以激活请登录'})


# 忘记密码视图
class ForgetPwdView(View):
	"""
	忘记密码
	"""

	def get(self, request):
		forget_form = ForgetForm()
		# 调用form方法，验证用户输入 没有错误err属性长度为0
		return render(request, 'forgetpwd.html', {'forget_form': forget_form})

	def post(self, request):
		forget_form = ForgetForm(request.POST)
		if forget_form.is_valid():
			email = request.POST.get('email', '')
			send_register_email(email, 'forget')  # 调用发送邮件类型是找回密码
			return render(request, 'send_success.html')
		else:
			return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 重置密码get方法视图
class ResetView(View):
	"""
	（涉及到跳转页面传递active_code参数如果把get和post写到一个类里
	调用post方法时不会传递active_code参数就会报错）
	重置密码get方法
	"""

	def get(self, request, active_code):
		all_records = EmailVerifyRecord.objects.filter(code=active_code)
		# 查找数据库中EmailVerifyRecord表中匹配code=active_code的对象
		if all_records:
			for record in all_records:
				email = record.email
				return render(request, 'pwdreset.html', {'email': email})
		else:
			return render(request, 'active_fail.html')


# 重置密码post方法视图
class ModifyPwdView(View):
	"""
	重置密码post方法
	"""

	def post(self, request):
		modif_Form = ModifyPwdForm(request.POST)
		# 调用form方法，验证用户输入 没有错误err属性长度为0
		if modif_Form.is_valid():
			pwd1 = request.POST.get('password1', '')
			pwd2 = request.POST.get('password2', '')
			email = request.POST.get('email', '')
			# 如果两次密码不相等，返回错误信息
			if pwd1 != pwd2:
				return render(request, 'pwdreset.html', {'email': email, 'msg': '密码不一致请重新输入'})
			else:
				user = UserProfile.objects.get(email=email)
				# 通过邮箱查找到对应用户
				user.password = make_password(pwd2)  # 修改密码
				user.save()
				return render(request, 'pwdreset.html', {'email': email, 'msg': '密码修改成功请重新登录'})
		else:
			email = request.POST.get('email', '')
			return render(request, 'pwdreset.html', {'email': email, 'modif_Form': modif_Form})
