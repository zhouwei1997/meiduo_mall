# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/3/22
# @file  constants.py
# @description  常量文件
"""
# 图形验证码有效时间  单位：秒
IMAGE_CODE_REDIS_EXPIRES = 300
# 短信验证码有效时间  单位：秒
SMS_CODE_REDIS_EXPIRES = 300
# 短信模板
SEND_SMS_TEMPLATE_ID = 1
# 60s 内是否重发标记
SEND_SMS_CODE_INTERVAL = 60
