"""
# File       : jinja2_env.py
# Time       ：2023/3/20 16:04
# Author     ：zhouwei
# version    ：1.0.0
# Description：jinja2补充环境
"""
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


def jinja2_environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
