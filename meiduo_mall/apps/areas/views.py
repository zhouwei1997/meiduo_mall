# Create your views here.
import logging

from django import http
from django.core.cache import cache
from django.views import View

from areas.models import Area
from meiduo_mall.utils.response_code import RETCODE

logger = logging.getLogger('django')


class AreaView(View):
    """省市区数据"""

    def get(self, request):
        """
        提供省市区数据
        :param request:
        :return: JSON
        """
        area_id = request.GET.get('area_id')
        if not area_id:
            # 获取并判断是否有缓存
            province_list = cache.get('province_list')
            if not province_list:
                # 提供省份数据
                try:
                    province_model_list = Area.objects.filter(
                        parent__isnull=True)
                    # 序列化省级数据
                    province_list = []
                    for province_model in province_model_list:
                        province_list.append({
                            'id': province_model.id,
                            'name': province_model.name
                        })
                    # 缓存省份字典列表数据
                    cache.set('province_list', province_list, 3600)
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({
                        'code': RETCODE.DBERR,
                        'errmsg': '省份数据错误'
                    })
                    # 响应省份数据
            return http.JsonResponse({
                'code': RETCODE.OK,
                'errmsg': 'OK',
                'province_list': province_list
            })
        else:
            sub_data = cache.get('sub_area_' + area_id)
            if not sub_data:
                try:
                    # 提供市级或区县数据
                    parent_model = Area.objects.get(id=area_id)
                    sub_model_list = parent_model.subs.all()
                    subs = []
                    for sub_model in sub_model_list:
                        sub_dict = {
                            "id": sub_model.id,
                            "name": sub_model.name
                        }
                        subs.append(sub_dict)
                    # 子级JSON数据
                    sub_data = {
                        'id': parent_model.id,
                        'name': parent_model.name,
                        'subs': subs
                    }
                    cache.set('sub_area_' + area_id, sub_data, 3600)
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({
                        'code': RETCODE.DBERR,
                        'errmsg': '城市或区县数据错误'
                    })
            return http.JsonResponse({
                'code': RETCODE.OK,
                'errmsg': 'OK',
                'sub_data': sub_data
            })
