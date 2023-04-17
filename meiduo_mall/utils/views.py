# -*- coding:utf-8 -*-
"""
# @author ZhouWei
# @date  2023/4/17
# @file  views.py
# @description
"""
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin

from meiduo_mall.utils.response_code import RETCODE


class LoginRequiredJSONMinxin(LoginRequiredMixin):
    """自定义判断用户是否登录的扩展类；返回JSON"""

    def handle_no_permission(self):
        """直接响应JSON"""
        return http.JsonResponse({
            'code': RETCODE.SESSIONERR,
            'errmsg': '用户未登录'
        })


"""
def handle_no_permission(self):
    if self.raise_exception:
        raise PermissionDenied(self.get_permission_denied_message())
    return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class LoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
"""
