# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/3/22
# @file  constants.py
# @description  验证码使用的常量 文件
"""
# 图形验证码有效时间  单位：秒
IMAGE_CODE_REDIS_EXPIRES = 300
# 短信验证码有效时间  单位：秒
SMS_CODE_REDIS_EXPIRES = 300
# 短信模板
SEND_SMS_TEMPLATE_ID = 1
# 60s 内是否重发标记
SEND_SMS_CODE_INTERVAL = 60
# 容联云
ACCOUNT_SID = '2c94887686c00d75018709a1f74110c8'
# meiduo_mall子应用的token
AUTH_TOKEN = '811971d5df5634ec054e12718fad0132'
# meiduo_mall的 APP_ID
APP_ID = '2c94887686c00d75018709a551af10d3'
