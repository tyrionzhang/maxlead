# -*- coding: utf-8 -*-
import json
from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from max_stock.models import Menus,Roles
from maxlead_site.models import UserProfile
from max_stock import update_res
from maxlead_site.views.app import App
from django.db.models import Q


@csrf_exempt
def index(request):
    user = App.get_user_info(request)
    if not user:
        return HttpResponseRedirect("/admin/max_stock/login/")
    user_id = request.GET.get('user_id', '')
    list = Menus.objects.all()
    user_list = User.objects.filter(userprofile__role=99)
    index_user = user_list[0]
    if user_id:
        index_user = User.objects.get(id=user_id)
    role_list = Roles.objects.all()
    checked_role = 0
    for val in role_list:
        val.is_checked = 0
        if val.code == index_user.userprofile.stocks_role:
            val.is_checked = 1
            checked_role = val.id
    role_menus = Menus.objects.filter(roles__id=checked_role)
    role_ids = []
    if role_menus:
        for val in role_menus:
            role_ids.append(val.elem_id)

    for val in list:
        val.is_checked = 0
        if val.elem_id in role_ids:
            val.is_checked = 1

    data = {
        'list': list,
        'user': user,
        'user_id': user_id,
        'user_list': user_list,
        'role_list': role_list,
        'title': 'Setting',
    }
    return render(request, "Stocks/settings/index.html", data)

@csrf_exempt
def update_menus(request):
    user = App.get_user_info(request)
    if not user:
        return HttpResponse(json.dumps({'code': 66}), content_type='application/json')
    menus = update_res.MENUS
    querysetlist = []
    for val in  menus:
        menu = Menus.objects.filter(name=val['name'],elem_id=val['elem_id'])
        if not menu:
            querysetlist.append(Menus(name=val['name'], elem_id=val['elem_id'], url=val['url']))
    if querysetlist:
        Menus.objects.bulk_create(querysetlist)
    return HttpResponse(json.dumps({'code': 1, 'msg': 'Work is done!'}), content_type='application/json')

@csrf_exempt
def add_role(request):
    user = App.get_user_info(request)
    if not user:
        return HttpResponse(json.dumps({'code': 66}), content_type='application/json')
    if request.method == 'POST':
        role_name = request.POST.get('role_name','')
        role_code = request.POST.get('role_code','')
        menu_ids = request.POST.get('menu_ids','')
        if not role_code or not role_name or not menu_ids:
            return HttpResponse(json.dumps({'code': 0, 'msg': 'Code/Name is empty!'}), content_type='application/json')
        role_obj = Roles()
        role_obj.id
        role_obj.name = role_name
        role_obj.code = role_code
        role_obj.save()
        for val in eval(menu_ids):
            menu_obj = Menus.objects.get(id=int(val))
            menu_obj.roles.add(role_obj)
        return HttpResponse(json.dumps({'code': 1, 'msg': 'Work is done!'}), content_type='application/json')

@csrf_exempt
def change_role(request):
    user = App.get_user_info(request)
    if not user:
        return HttpResponse(json.dumps({'code': 66}), content_type='application/json')
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '')
        role_code = request.POST.get('role_user_code', '')
        box_menu_ids = request.POST.get('box_menu_ids', '')
        user_obj = UserProfile.objects.filter(user_id=user_id)
        role_obj = Roles.objects.filter(code=role_code)
        if not user_obj or not role_obj:
            return HttpResponse(json.dumps({'code': 0, 'msg': 'User/Role is not exits!'}), content_type='application/json')
        user_obj.update(stocks_role=role_code)
        res = role_obj[0].menus_set.all()
        for val in res:
            val.roles.filter(code=role_code).delete()
        objs = Menus.objects.filter(id__in=eval(box_menu_ids))
        if objs:
            for val in objs:
                val.roles.add(role_obj[0])
        return HttpResponse(json.dumps({'code': 1, 'msg': 'Work is done!'}), content_type='application/json')

