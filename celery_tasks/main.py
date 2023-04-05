# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/4/5
# @file  main.py
# @description celery 程序的入口文件
"""
from celery import Celery

# 创建celery实例
celery_app = Celery('meiduo')
# 加载celery配置文件
celery_app.config_from_object('celery_tasks.config')
# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])
