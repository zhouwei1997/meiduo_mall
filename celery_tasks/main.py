# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/4/5
# @file  main.py
# @description celery 程序的入口文件
"""

"""
启动celery任务
linux:celery -A celery_tasks.main worker -l info
windows:ModuleNotFoundError: celery -A celery_tasks.main worker -l info -P eventlet
"""
import os

from celery import Celery

# if __name__ == "__main__":
#     # 指定配置文件路径
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.meiduo_mall.settings.settings-dev")

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.settings-dev'

# 创建celery实例
celery_app = Celery('meiduo')
# 加载celery配置文件
celery_app.config_from_object('celery_tasks.config')
# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])
