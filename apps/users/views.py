from django.shortcuts import render
# 加载django提供的用户名密码验证方法authenticate login
from django.contrib.auth import authenticate, login
# 加载django提供的ModelBackend方法，用于自定义认证
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View

# 调用我们models.py里自己定义的用户表
from .models import UserProfile
from .forms import LoginForm


class CustomBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username) | Q(email=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None


class LoginView(View):
	def get(self, request):
		return render(request, 'login.html', {})

	def post(self, request):
		login_form = LoginForm(request.POST)
		# 调用form方法，验证用户输入
		if login_form.is_valid():
			user_name = request.POST.get('username', '')
			pass_word = request.POST.get('password', '')
			user = authenticate(username=user_name, password=pass_word)
			if user is not None:
				login(request, user)
				return render(request, 'index.html')
			else:
				return render(request, 'login.html', {'login_form': '用户名或密码错误!!!'})
		else:
			return render(request, 'login.html', {'login_form':login_form})
