"""maxlead URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from maxlead_site.views.users.login import Logins
# views of max_stock
from max_stock.views import views as stock_views
from max_stock.views import users as stock_users
from max_stock.views import users_sku as skus
from max_stock.views import stocks
from django.views import static
from maxlead import settings

urlpatterns = [
    # url(r'^admin/warehouse/spider/', warehouse_views.home),
    url(r'^static/(?P<path>.*)$', static.serve,{ 'document_root': settings.STATIC_URL }),
    url(r'^download/(?P<path>.*)$', static.serve,{ 'document_root': settings.DOWNLOAD_URL }),
    url(r'^admin/maxlead_site/login/', Logins.userLogin),
    url(r'^$', stocks.index),

    # urls of max_stock
    url('^admin/max_stock/stock_spiders/', stock_views.stock_spiders),
    url('^admin/max_stock/empty_data/', stock_views.empty_data),
    url('^admin/max_stock/login/', stock_users.userLogin),
    url('^admin/max_stock/user_list/', stock_users.user_list),
    url('^admin/max_stock/user_save/', stock_users.user_save),
    url('^admin/max_stock/users_import/', stock_users.users_import),
    url('^admin/max_stock/users_del/', stock_users.users_del),
    url('^admin/max_stock/logout/', stock_users.logout),
    url('^admin/max_stock/index/', stocks.index),
    url('^admin/max_stock/$', stocks.index),
    url('^admin/max_stock/stock_checked/', stocks.stock_checked),
    url('^admin/max_stock/checked_edit/', stocks.checked_edit),
    url('^admin/max_stock/checked_batch_edit/', stocks.checked_batch_edit),
    url('^admin/max_stock/export_stocks/', stocks.export_stocks),
    url('^admin/max_stock/threshold/', stocks.threshold),
    url('^admin/max_stock/threshold_add/', stocks.threshold_add),
    url('^admin/max_stock/get_threshold/', stocks.get_threshold),
    url('^admin/max_stock/threshold_del/', stocks.threshold_del),
    url('^admin/max_stock/threshold_import/', stocks.threshold_import),
    url('^admin/max_stock/check_new/', stocks.check_new),
    url('^admin/max_stock/check_all_new/', stocks.check_all_new),
    url('^admin/max_stock/covered_new/', stocks.covered_new),
    url('^admin/max_stock/covered_new_all/', stocks.covered_new_all),
    url('^admin/max_stock/covered_give_up/', stocks.covered_give_up),
    url('^admin/max_stock/users_sku/', skus.sku_list),
    url('^admin/max_stock/save_sku/', skus.save_sku),
    url('^admin/max_stock/import_sku/', skus.import_sku),
    url('^admin/max_stock/del_sku/', skus.del_sku),
    url('^admin/max_stock/logs/', skus.logs),
]

