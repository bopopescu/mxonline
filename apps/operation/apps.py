from django.apps import AppConfig


class OperationConfig(AppConfig):
    name = 'operation'
    verbose_name = '用户操作'  # 配置中文别名，还需在__init__中配置