#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import importlib
from django.views import View
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from utils import auth
from api import config
from repository import models
from api.service import asset

@auth.api_auth
def asset(request):
    pass


class AssetView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AssetView, self).dispatch(request, *args, **kwargs)

    @method_decorator(auth.api_auth)
    def get(self, request, *args, **kwargs):
        """
        获取今日未更新的资产 - 适用SSH或Salt客户端
        """

        response = asset.get_untreated_servers()
        return JsonResponse(response.__dict__)

    @method_decorator(auth.api_auth)
    def post(self, request, *args, **kwargs):
        """
        更新或者添加资产信息
        :return: 1000 成功;1001 接口授权失败;1002 数据库中资产不存在
        """

        server_info = json.loads(request.body.decode('utf-8'))
        server_info = json.loads(server_info)
        hostname = server_info['hostname']

        ret = {'code': 1000, 'message': '[%s]更新完成' % hostname}
        server_obj = modelss.Server.objects.filter(hostname=hostname).select_related('asset').first()
        if not server_obj:
            ret['code'] = 1002
            ret['message'] = '[%s]资产不存在' % hostname
            return JsonResponse(ret)

        return JsonResponse(ret)