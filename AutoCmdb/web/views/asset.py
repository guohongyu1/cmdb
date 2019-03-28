#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from repository import models
from web.service import asset


class AssetListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'asset_list.html')


class AssetJsonView(View):
    def get(self, request):
        obj = asset.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = asset.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})
from django.forms import ModelForm
class AssetList(ModelForm):
  class Meta:
    model = models.Asset #对应的Model中的类
    fields = "__all__"   #字段，如果是__all__,就是表示列出所有的字段
    exclude = None     #排除的字段
    labels = None      #提示信息
    help_texts = None    #帮助提示信息
    widgets = None     #自定义插件
    error_messages = None  #自定义错误信息
class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        if request.method=='GET':
            asset_list=AssetList()
            return render(request, 'add_asset.html',{'asset_list':asset_list})
        else:
            asset_list=AssetList(request.POST)
            if asset_list.is_valid():
                asset_list.save()
            return render(request, 'add_asset.html', {'asset_list': asset_list})




