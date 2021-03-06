import os,sched,calendar
from datetime import *
import queue
import threading
import time
from django.http import HttpResponseRedirect
from django.shortcuts import render
from maxlead_site.views.app import App
from maxlead import settings
from max_stock.models import SkuUsers,StockLogs,WarehouseStocks
from django.http import HttpResponse

# 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数
# 第二个参数以某种人为的方式衡量时间
schedule = sched.scheduler(time.time, time.sleep)
week_day = {
    'monday':'MONDAY',
    'tuesday':'TUESDAY',
    'wednesday':'WEDNESDAY',
    'thursday':'THURSDAY',
    'saturday':'SATURDAY',
    'sunday':'SUNDAY',
}
def getNextSaturday():
    today = date.today()
    oneday = timedelta(days = 1)
    m1 = calendar.SATURDAY
    while today.weekday() != m1:
        today += oneday
    re = today.strftime('%Y-%m-%d')
    return re

def _set_user_sku(request=None):
    sku_list = []
    file_name = 'userSkus_txt.txt'
    if request:
        user = App.get_user_info(request)
    user_skus = SkuUsers.objects.filter().all()
    if request and not user.user.is_superuser:
        user_skus = user_skus.filter(user=user.user)
        file_name = 'userSkus_txt_%s.txt' % user.user.username
    if user_skus:
        for val in user_skus:
            sku_list.append(val.sku)
        file_path = os.path.join(settings.BASE_DIR, settings.THRESHOLD_TXT, file_name)
        with open(file_path, "w+") as f:
            sku_list = str(sku_list)
            f.write(sku_list)
            f.close()
    return True

class perform_command_que(threading.Thread):
    def __init__(self, t_name, queue, request=None):
        threading.Thread.__init__(self,name=t_name)
        self.data = queue
        self.t_name = t_name
        self.username = ''
        if request:
            user = App.get_user_info(request)
            if not user.user.is_superuser:
                self.username = user.user.username

    def run(self):
        work_path = settings.STOCHS_SPIDER_URL
        os.chdir(work_path)
        os.popen('scrapyd-deploy')

        cmd_str2 = 'curl http://www.goldgg.cn:6800/schedule.json -d project=stockbot -d spider=twu_spider'
        cmd_str1 = 'curl http://www.goldgg.cn:6800/schedule.json -d project=stockbot -d spider=hanover_spider'
        cmd_str3 = 'curl http://www.goldgg.cn:6800/schedule.json -d project=stockbot -d spider=exl_spider'
        # cmd_str4 = 'curl http://localhost:6800/schedule.json -d project=stockbot -d spider=exl1_spider'
        os.popen(cmd_str2)
        os.popen(cmd_str1)
        os.popen(cmd_str3)
        # os.popen(cmd_str4)
        print('%s:%s finished!' % (time.time(), self.getName()))
        os.chdir(settings.ROOT_PATH)

def run_command_queue():
    time_now = datetime.now()
    time_re = datetime.now() + timedelta(days=1)
    time_saturday = '%s 05:00:00' % time_re.strftime('%Y-%m-%d')
    time_saturday = datetime.strptime(time_saturday, '%Y-%m-%d %H:%M:%S')
    t_re = (time_saturday - time_now).total_seconds()
    spiders_time = "%.1f" % t_re
    t = threading.Timer(float(spiders_time), run_command_queue)
    _set_user_sku()
    q = queue.Queue()

    tname = 'stocks_done'
    reviews = perform_command_que(tname, q)
    reviews.start()
    reviews.join()
    t.start()

def stock_spiders(request):
    user = App.get_user_info(request)
    if not user:
        return HttpResponseRedirect("/admin/max_stock/login/")
    type = request.GET.get('type','')
    if type == 'now':
        _set_user_sku(request)
        q = queue.Queue()

        tname = 'stocks_done'
        reviews = perform_command_que(tname, q, request)
        reviews.start()
        reviews.join()
        msg_str = 'Spiders is runing!'
    else:
        time_now = datetime.now()
        time_re = datetime.now() + timedelta(days = 1)
        time_saturday = '%s 05:00:00' % time_re.strftime('%Y-%m-%d')
        time_saturday = datetime.strptime(time_saturday, '%Y-%m-%d %H:%M:%S')
        t_re = (time_saturday - time_now).total_seconds()
        t = threading.Timer(float('%.1f' % int(t_re)), run_command_queue)
        # 持续运行，直到计划时间队列变成空为止
        t.start()
        time_str = datetime.now() +  timedelta(seconds = int(t_re))
        msg_str = 'Spiders will be runing!The time:%s' % time_str
    return render(request, "Stocks/spider/home.html", {'msg_str':msg_str})

def save_logs(data):
    logs = StockLogs()
    logs.id
    logs.user = data['user']
    logs.fun = data['fun']
    logs.description = data['description']
    res = logs.save()
    return True

def empty_data(request):
    WarehouseStocks.objects.filter().all().delete()
    StockLogs.objects.filter().all().delete()
    return HttpResponse(request, 'Spiders is runing!Time:%s' % datetime.now())

def test(request):
    work_path = settings.STOCHS_SPIDER_URL
    os.chdir(work_path)
    os.popen('scrapyd-deploy')

    cmd_str2_test = 'curl http://localhost:6800/schedule.json -d project=stockbot -d spider=email_spider'
    os.popen(cmd_str2_test)
    return render(request, "Stocks/spider/home.html", {'msg_str': 'Done!'})