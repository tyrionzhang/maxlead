# -*- coding: utf-8 -*-
import os,json
from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from max_stock.models import AmazonCode
from maxlead_site.views.app import App
from maxlead import settings
from max_stock.views import views
from django.db.models import Count
from django.core.mail import send_mail

@csrf_exempt
def code_index(request):
    user = App.get_user_info(request)
    if not user:
        return HttpResponseRedirect("/admin/max_stock/login/")
    code_list = AmazonCode.objects.all()
    data = {
        'code_list': code_list,
        'user': user,
        'title': 'AmazonCode',
    }
    return render(request, "Stocks/auto_email/codes.html", data)

@csrf_exempt
def code_save(request):
    user = App.get_user_info(request)
    if not user:
        return HttpResponse(json.dumps({'code': 66}), content_type='application/json')

    if request.method == 'POST':
        id = request.POST.get('id','')
        email = request.POST.get('email','')
        code = request.POST.get('code','')
        if not id:
            code_obj = AmazonCode()
            code_obj.id
            code_obj.email = email
            code_obj.code = code
            code_obj.save()
            if code_obj.id:
                return HttpResponse(json.dumps({'code': 1, 'msg': '保存成功！'}), content_type='application/json')
        else:
            code_obj = AmazonCode.objects.filter(id=id)
            re = code_obj.update(code=code)
            if re:
                return HttpResponse(json.dumps({'code': 1, 'msg': '保存成功！'}), content_type='application/json')

