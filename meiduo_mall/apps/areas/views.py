# Create your views here.
import logging

from django.http import JsonResponse
from django.views import View

from areas.models import Area
from meiduo_mall.utils.response_code import RETCODE

logger = logging.getLogger('django')


class AreaView(View):
    """省市区数据"""

    def get(self, request):
        """提供省市区数据"""
        area_id = request.GET.get('area_id')
        if not area_id:
            # 提供省份数据
            try:
                province_model_list = Area.objects.filter(parent_isnull=True)
                # 序列化省级数据
                province_list = []
                for province_model in province_model_list:
                    province_list.append({
                        'id': province_model.id,
                        'name': province_model.name
                    })
                # 响应省份数据
                return JsonResponse({
                    'code': RETCODE.OK,
                    'errmsg': 'OK',
                    'province_list': province_list
                })
            except Exception as e:
                logger.error(e)
                return JsonResponse({
                    'code': RETCODE.DBERR,
                    'errmsg': '省份数据错误'
                })
        else:
            # 提供市级数据
            pass

