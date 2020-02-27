from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '用户资源'  # 配置中文别名，还需在__init__中配置
