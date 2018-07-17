# -*- coding: utf-8 -*-
import json
from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from max_stock.models import Menus
from max_stock import update_res
from maxlead_site.views.app import App
from django.db.models import Q


@csrf_exempt
def index(request):
    user = App.get_user_info(request)
    if not user:
        return HttpResponseRedirect("/admin/max_stock/login/")
    user_id = request.GET.get('user_id', '')
    if not user_id:
        user_id = user.user_id
    list = Menus.objects.all()
    user_list = User.objects.filter(userprofile__role=99)
    users = User.objects.filter(id=user_id)

    data = {
        'list': list,
        'user': user,
        'user_list': user_list,
        'title': 'Setting',
    }
    return render(request, "Stocks/settings/index.html", data)

@csrf_exempt
def update_menus(request):
    user = App.get_user_info(request)
    if not user:
        return HttpResponseRedirect("/admin/max_stock/login/")
    menus = update_res.MENUS
    querysetlist = []
    for val in  menus:
        menu = Menus.objects.filter(name=val['name'],elem_id=val['elem_id'])
        if not menu:
            querysetlist.append(Menus(name=val['name'], elem_id=val['elem_id'], url=val['url']))
    if querysetlist:
        Menus.objects.bulk_create(querysetlist)
    return HttpResponse(json.dumps({'code': 1, 'msg': 'Work is done!'}), content_type='application/json')