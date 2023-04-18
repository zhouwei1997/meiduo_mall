# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/4/17
# @file  tasks.py
# @description  定义发送邮件任务
"""
import logging

from django.conf import settings
from django.core.mail import send_mail

from celery_tasks.main import celery_app

logger = logging.getLogger('django')


@celery_app.task(name='send_verify_email')
def send_verify_email(to_email, verify_url):
    """
    定义发送邮件任务
    :param to_email: 收件人
    :param verify_url: 激活连接
    :return:
    """
    subject = "美多商城邮箱验证"
    html_message = '<p>尊敬的用户，您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此连接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s</p>' % (to_email, verify_url, verify_url)

    # try:
    #     send_mail(subject, '', settings.EMAIL_FROM, [to_email], html_message=html_message)
    # except Exception as e:
    #     # 触发错误重试：最多重新3次
    #     raise self.retry(exc=e, max_retries=3)
    send_mail(subject, '', settings.EMAIL_FROM, [to_email], html_message=html_message)
    # send_mail(subject, '', '美多商城<hengyu19971023@163.com>', [to_email], html_message=html_message)
