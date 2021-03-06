# -*- coding: utf-8 -*-
import scrapy,os,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bots.stockbot.stockbot import settings
from maxlead import settings as max_settings
from bots.stockbot.stockbot.items import WarehouseStocksItem
from max_stock.models import WarehouseStocks,Thresholds,SkuUsers
from django.core.mail import send_mail

class HanoverSpider(scrapy.Spider):
    name = "hanover_spider"

    msg_str1 = "complete\n"
    start_urls = [
        'http://www.telescoassoc.com/prod/hnv/transform.aspx?_h=go&_md=vwInventory&_tpl=vwInventoryList.xsl&_gt=-1&_gs=20&rhash=5adab926c2b523c494&_ha=gmv'
    ]
    sku_list = []

    def __init__(self, username=None, *args, **kwargs):
        super(HanoverSpider, self).__init__(*args, **kwargs)
        file_name = 'userSkus_txt.txt'
        if username:
            file_name = 'userSkus_txt_%s.txt' % username
        file_path = os.path.join(max_settings.BASE_DIR, max_settings.THRESHOLD_TXT, file_name)
        with open(file_path, "r") as f:
            sku_list = f.read()
            f.close()
        if sku_list:
            self.sku_list = eval(sku_list)

    def parse(self, response):
        file_path = os.path.join(max_settings.BASE_DIR, max_settings.THRESHOLD_TXT, 'threshold_txt.txt')
        msg_str2 = ''
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(800, 800))
        display.start()
        chrome_options = Options()
        chrome_options.add_argument('-headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=settings.CHROME_PATH, service_log_path=settings.LOG_PATH)
        driver.get(response.url)
        elem_code = driver.find_elements_by_id('WarehouseCode')
        elem_acode = driver.find_elements_by_id('AccountCode')
        elem_name = driver.find_elements_by_id('UserName')
        elem_pass = driver.find_elements_by_id('Password')
        btn_login = driver.find_elements_by_css_selector('input[name="Login"]')

        if elem_code:
            elem_code[0].send_keys('03')
        if elem_acode:
            elem_acode[0].send_keys('001862')
        if elem_name:
            elem_name[0].send_keys('MAXLEAD')
        if elem_pass:
            elem_pass[0].send_keys('1202HXML')
        btn_login[0].click()
        driver.implicitly_wait(100)
        total_page = driver.find_elements_by_css_selector('#navigationTR nobr')[0].text
        total_page = int(total_page.split(' ')[-1])
        for i in range(total_page):
            res = driver.find_elements_by_css_selector('#ViewManyListTable tr')
            elem = driver.find_element_by_id('MetaData')
            elem.click()
            res.pop(0)
            for val in res:
                item = WarehouseStocksItem()
                td_re = val.find_elements_by_tag_name('td')
                if td_re:
                    item['sku'] = td_re[0].text
                    if item['sku'] in self.sku_list:
                        item['warehouse'] = 'Hanover'
                        item['is_new'] = 1
                        if td_re[2].text and not td_re[2].text == ' ':
                            item['qty'] = td_re[2].text
                            item['qty'] = item['qty'].replace(',','')
                        else:
                            item['qty'] = 0
                        yield item

                        threshold = Thresholds.objects.filter(sku=item['sku'], warehouse=item['warehouse'])
                        user = SkuUsers.objects.filter(sku=item['sku'])
                        if threshold and threshold[0].threshold >= int(item['qty']):
                            if user:
                                msg_str2 += '%s=>SKU:%s,Warehouse:%s,QTY:%s,Early warning value:%s \n|' % ( user[0].user.email,
                                                        item['sku'], item['warehouse'], item['qty'], threshold[0].threshold)
            if i < total_page:
                elem_next_page = driver.find_elements_by_id('Next')
                if elem_next_page:
                    elem_next_page[0].click()
                    driver.implicitly_wait(100)
        display.stop()
        driver.quit()

        if not os.path.isfile(file_path):
            with open(file_path, "w+") as f:
                f.close()
        with open(file_path, "r+") as f:
            old = f.read()
            f.seek(0)
            f.write(self.msg_str1)
            f.write(old)
            f.write(msg_str2)
            f.close()

        with open(file_path, "r") as f:
            msg1 = f.readline()
            msg2 = f.readline()
            msg3 = f.readline()
            if msg1 == 'complete\n' and msg2 == 'complete\n' and msg3 == 'complete\n':
                msg_line = f.read()
                if msg_line:
                    msg_line = msg_line.split('|')
                    msg_line.pop()
                    all_msg = ''
                    subject = 'Maxlead库存预警'
                    from_email = max_settings.EMAIL_HOST_USER

                    msg = {}
                    for i, val in enumerate(msg_line, 1):
                        val = val.split('=>')
                        msg_res_str = val[1]
                        for n, v in enumerate(msg_line, 1):
                            v = v.split('=>')
                            if not n == i and val[0] == v[0]:
                                msg_res_str += v[1]
                        msg.update({val[0]: msg_res_str})
                    for key in msg:
                        all_msg += msg[key]
                        send_mail(subject, msg[key], from_email, [key], fail_silently=False)
                    send_mail(subject, all_msg, from_email, ['shipping.gmi@gmail.com'], fail_silently=False)
                f.close()
                os.remove(file_path)


