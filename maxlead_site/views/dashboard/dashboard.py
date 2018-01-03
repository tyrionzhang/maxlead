# -*- coding: utf-8 -*-
import json,datetime,operator
from django.shortcuts import render,HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count,Max
from maxlead_site.models import Listings,UserAsins,Questions,Answers,Reviews,AsinReviews,MenberGroups
from maxlead_site.views.app import App
from maxlead_site.common.excel_world import get_excel_file

class Dashboard:


    def _get_asins(self,user,ownership=''):
        asins = []
        user_asins = UserAsins.objects.values('aid').annotate(count=Count('aid')).filter(review_watcher=1, is_use=1)
        if ownership:
            user_asins = user_asins.filter(ownership=ownership)

        if user.role == 0:
            user_asins = user_asins.filter(user=user.user)
        elif user.role == 1:
            groups = MenberGroups.objects.filter(user=user.user)
            user_list = User.objects.filter(group=groups)
            user_asins = user_asins.filter(user=user_list)
        for val in user_asins:
            asins.append(val['aid'])

        return asins

    def _get_activity_radar(self, others_asins, param={}):
        if param:
            actBgn = param.get('actBgn', '')
            actEnd = param.get('actEnd', '')
        activity_radar = []
        for val in others_asins:
            listing = Listings.objects.filter(asin=val).order_by('-created')[:2]
            if param:
                if actBgn:
                    listing = listing.filter(created__gte=actBgn)
                if actEnd:
                    listing = listing.filter(created__lte=actEnd)

            if len(listing) == 2:
                if not listing[0].price == listing[1].price or not listing[0].title == listing[1].title or not listing[0]. \
                                           image_date == listing[1].image_date or not operator.eq(listing[0].description,
                                           listing[1].description) or not operator.eq(listing[0].feature, listing[1].feature):

                    listing[1].changed = ''
                    if not listing[0].price == listing[1].price:
                        listing[1].changed += 'price,'
                    if not listing[0].image_date == listing[1].image_date:
                        listing[1].changed += 'Gallery,'
                    if not listing[0].title == listing[1].title:
                        listing[1].changed += 'title,'
                    if not listing[0].feature == listing[1].feature or not listing[0].description == listing[
                        1].description:
                        listing[1].changed += 'Promotion,'

                    listing[1].created = listing[1].created.strftime('%Y-%m-%d')
                    if eval(listing[1].buy_box_res):
                        listing[1].buy_box_res = eval(listing[1].buy_box_res)[0]
                    else:
                        listing[1].buy_box_res = ''
                    activity_radar.append(listing[1])
        return activity_radar

    def index(self):
        user = App.get_user_info(self)
        if not user:
            return HttpResponseRedirect("/admin/maxlead_site/login/")

        asins = Dashboard._get_asins(self,user)
        ours_asins = Dashboard._get_asins(self,user,ownership='Ours')
        others_asins = Dashboard._get_asins(self,user,ownership='Others')
        ours_li = []
        others_li = []
        for val in ours_asins[0:6]:
            listing = Listings.objects.filter(asin=val).order_by('-created')[:2]

            if len(listing) == 2:
                rvw_score2 = float(listing[0].rvw_score) - float(listing[1].rvw_score)
            else:
                rvw_score2 = ''
            re = {
                'asin':listing[0].asin,
                'sku':listing[0].user_asin.sku,
                'total_review':listing[0].total_review,
                'rvw_score':float(listing[0].rvw_score),
                'rvw_score2':rvw_score2
            }
            ours_li.append(re)

        activity_radar = Dashboard._get_activity_radar(self,others_asins)
        if activity_radar:
            activity_radar = activity_radar[0:6]
        radar_page = 0
        if len(activity_radar)>=6:
            radar_page = 1

        for val in others_asins[0:6]:
            listing = Listings.objects.filter(asin=val).order_by('-created')[:2]

            if len(listing) == 2:
                rvw_score2 = float(listing[0].rvw_score) - float(listing[1].rvw_score)
            else:
                rvw_score2 = ''
            re = {
                'asin':listing[0].asin,
                'sku':listing[0].user_asin.sku,
                'total_review':listing[0].total_review,
                'rvw_score':float(listing[0].rvw_score),
                'rvw_score2':rvw_score2
            }
            others_li.append(re)

        o_rising_page = 0
        th_rising_page = 0
        if len(ours_asins) > 6:
            o_rising_page = 1
        if len(others_asins) > 6:
            th_rising_page = 1

        reviews = Reviews.objects.filter(created__icontains=Reviews.objects.aggregate(Max('created'))['created__max'],
                                        score__lte=3,asin__in=asins).order_by('-review_date')

        is_page = 0
        if len(reviews) > 6:
            is_page = 1
        if reviews:
            reviews = reviews[0:6]

        for val in reviews:
            if val.review_date:
                val.review_date = val.review_date.strftime("%Y-%m-%d")
            val.sku = UserAsins.objects.get(aid=val.asin).sku

        data = {
            'user': user,
            'avator': user.user.username[0],
            'reviews': reviews,
            'ours_li': ours_li,
            'others_li': others_li,
            'is_page': is_page,
            'th_rising_page': th_rising_page,
            'o_rising_page': o_rising_page,
            'radar_page': radar_page,
            'activity_radar': activity_radar,
        }
        return render(self, 'dashboard/dashboard.html', data)

    @csrf_exempt
    def ajax_get_reviews(self):
        user = App.get_user_info(self)
        if not user:
            return HttpResponse(json.dumps({'code': 0, 'msg': '用户未登录'}),content_type='application/json')
        revBgn = self.GET.get('revBgn', '')
        revEnd = self.GET.get('revEnd', '')
        page = self.GET.get('page', 1)
        offset = (int(page)-1)*6

        asins = Dashboard._get_asins(self,user)
        reviews = Reviews.objects.filter(created__icontains=Reviews.objects.aggregate(Max('created'))['created__max'],
                                         score__lte=3, asin__in=asins).order_by('-review_date')
        if revBgn:
            reviews = reviews.filter(review_date__gte=revBgn)
        if revEnd:
            reviews = reviews.filter(review_date__lte=revEnd)
        if reviews:
            reviews = reviews[offset:offset+6]

            data = []
            for val in reviews:
                if val.review_date:
                    val.review_date = val.review_date.strftime("%Y-%m-%d")
                a = model_to_dict(val)
                a['sku'] = UserAsins.objects.get(aid=val.asin).sku
                data.append(a)
            is_page = 1
            if len(reviews) < 6:
                is_page = 0

            re = {
                'data':data,
                'review_page':page,
                'is_page':is_page
            }

            return HttpResponse(json.dumps({'code': 1, 'data': re}), content_type='application/json')

    @csrf_exempt
    def ajax_rising(self):
        user = App.get_user_info(self)
        if not user:
            return HttpResponse(json.dumps({'code': 0, 'msg': '用户未登录'}), content_type='application/json')
        ourBgn = self.GET.get('ourBgn', '')
        ourEnd = self.GET.get('ourEnd', '')
        othBgn = self.GET.get('othBgn', '')
        othEnd = self.GET.get('othEnd', '')
        type = self.GET.get('type', 'Ours')
        page = self.GET.get('page', 1)
        offset = (int(page) - 1) * 6

        asins = Dashboard._get_asins(self, user, ownership=type)

        res = []
        for val in asins[offset:offset+6]:
            listing = Listings.objects.filter(asin=val)
            if ourBgn:
                listing = listing.filter(created__gte=ourBgn)
            if ourEnd:
                listing = listing.filter(created__lte=ourEnd)
            if othBgn:
                listing = listing.filter(created__gte=othBgn)
            if othEnd:
                listing = listing.filter(created__lte=othEnd)
            listing = listing.order_by('-created')[:2]

            if len(listing) == 2:
                rvw_score2 = float(listing[0].rvw_score) - float(listing[1].rvw_score)
            else:
                rvw_score2 = ''
            re = {
                'asin': listing[0].asin,
                'sku': listing[0].user_asin.sku,
                'total_review': listing[0].total_review,
                'rvw_score': float(listing[0].rvw_score),
                'rvw_score2': rvw_score2
            }
            res.append(re)
        is_page = 1
        if len(res) < 6:
            is_page = 0

        data = {
            'data':res,
            'is_page':is_page,
            'page':page
        }
        return HttpResponse(json.dumps({'code': 1, 'data': data}), content_type='application/json')

    @csrf_exempt
    def ajax_radar(self):
        user = App.get_user_info(self)
        if not user:
            return HttpResponse(json.dumps({'code': 0, 'msg': '用户未登录'}), content_type='application/json')

        page = self.GET.get('page', 1)
        offset = (int(page) - 1) * 6
        asins = Dashboard._get_asins(self, user, ownership='Others')
        res = Dashboard._get_activity_radar(self,asins,page = page, param=self.GET)
        is_page = 1
        if len(res)<6:
            is_page = 0
        data = []
        if res:
            res = res[offset:offset+6]
            for val in res:
                re = {
                    'asin':val.asin,
                    'created':val.created,
                    'changed':val.changed,
                    'buy_box_res':val.buy_box_res
                }
                data.append(re)
            data = {
                'data': data,
                'page': page,
                'is_page': is_page
            }
            return HttpResponse(json.dumps({'code': 1, 'data': data}), content_type='application/json')
        else:
            data = {
                'data': [],
                'page': page,
                'is_page': is_page
            }
            return HttpResponse(json.dumps({'code': 1, 'data': data}), content_type='application/json')

    @csrf_exempt
    def export_dash_reviews(self):
        user = App.get_user_info(self)
        if not user:
            return HttpResponseRedirect("/admin/maxlead_site/login/")

        revBgn = self.GET.get('revBgn', '')
        revEnd = self.GET.get('revEnd', '')

        asins = Dashboard._get_asins(self,user)
        reviews = Reviews.objects.filter(created__icontains=Reviews.objects.aggregate(Max('created'))['created__max'],
                                         score__lte=3, asin__in=asins).order_by('-review_date')
        if revBgn:
            reviews = reviews.filter(review_date__gte=revBgn)
        if revEnd:
            reviews = reviews.filter(review_date__lte=revEnd)

        data = []
        for val in reviews:
            re = {
                'title': val.title,
                'variation': val.variation,
                'asin': val.asin,
                'name': val.name,
                'score': val.score,
                'is_vp': val.is_vp,
                'review_date': val.review_date.strftime("%Y-%m-%d"),
                'content': val.content,
                'review_link': val.review_link,
                'created': val.created.strftime("%Y-%m-%d"),
            }
            data.append(re)

        fields = [
            'Title',
            'Variation',
            'Asin',
            'Name',
            'Score',
            'VP',
            'Review Date',
            'Content',
            'Review Link',
            'Created'
        ]
        data_fields = [
            'title',
            'variation',
            'asin',
            'name',
            'score',
            'is_vp',
            'review_date',
            'content',
            'review_link',
            'created'
        ]
        return get_excel_file(self, data, fields, data_fields)

    @csrf_exempt
    def export_rising(self):
        user = App.get_user_info(self)
        if not user:
            return HttpResponseRedirect("/admin/maxlead_site/login/")

        ourBgn = self.GET.get('ourBgn', '')
        ourEnd = self.GET.get('ourEnd', '')
        othBgn = self.GET.get('othBgn', '')
        othEnd = self.GET.get('othEnd', '')
        type = self.GET.get('type', 'Ours')

        asins = Dashboard._get_asins(self, user, ownership=type)

        res = []
        for val in asins:
            listing = Listings.objects.filter(asin=val)
            if ourBgn:
                listing = listing.filter(created__gte=ourBgn)
            if ourEnd:
                listing = listing.filter(created__lte=ourEnd)
            if othBgn:
                listing = listing.filter(created__gte=othBgn)
            if othEnd:
                listing = listing.filter(created__lte=othEnd)
            listing = listing.order_by('-created')[:2]

            if len(listing) == 2:
                rvw_score2 = float(listing[0].rvw_score) - float(listing[1].rvw_score)
            else:
                rvw_score2 = ''
            re = {
                'asin': listing[0].asin,
                'sku': listing[0].user_asin.sku,
                'brand': listing[0].brand,
                'total_review': listing[0].total_review,
                'rvw_score': float(listing[0].rvw_score),
                'rvw_score2': rvw_score2,
                'created': listing[0].created.strftime('%Y-%m-%d')
            }
            res.append(re)

        fields = [
            'SKU',
            'Asin',
            'Reviews',
            'Growth',
            'Score',
            'Score Change',
            'Created'
        ]
        data_fields = [
            'sku',
            'asin',
            'total_review',
            'brand',
            'rvw_score',
            'rvw_score2',
            'created'
        ]
        return get_excel_file(self, res, fields, data_fields)

    @csrf_exempt
    def export_radar(self):
        user = App.get_user_info(self)
        if not user:
            return HttpResponseRedirect("/admin/maxlead_site/login/")

        asins = Dashboard._get_asins(self, user, ownership='Others')
        res = Dashboard._get_activity_radar(self, asins,param=self.GET)
        data = []
        if res:
            for val in res:
                re = {
                    'asin': val.asin,
                    'title': val.title,
                    'price': val.price,
                    'feature': val.feature,
                    'description': val.description,
                    'image_date': val.image_date.strftime('%Y-%m-%d'),
                    'image_names': val.image_thumbs,
                    'created': val.created,
                    'changed': val.changed,
                    'buy_box_res': val.buy_box_res
                }
                data.append(re)

            fields = [
                'Image Thumbs',
                'Title',
                'Asin',
                'Price',
                'Changed',
                'Feature',
                'Description',
                'Image Date',
                'Buy Box',
                'Created'
            ]
            data_fields = [
                'image_names',
                'title',
                'asin',
                'price',
                'changed',
                'feature',
                'description',
                'image_date',
                'buy_box_res',
                'created'
            ]
            return get_excel_file(self, data, fields, data_fields)
