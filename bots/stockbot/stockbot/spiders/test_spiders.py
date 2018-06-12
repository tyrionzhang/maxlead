# -*- coding: utf-8 -*-
import scrapy,os,time
from selenium import webdriver
from bots.stockbot.stockbot import settings
from maxlead import settings as max_settings
from bots.stockbot.stockbot.items import WarehouseStocksItem
from max_stock.models import WarehouseStocks,Thresholds,SkuUsers
from django.core.mail import send_mail

class TestSpider(scrapy.Spider):
    name = "test_spider"

    # start_urls = ['https://docs.google.com/spreadsheets/d/1cIW9ksnTu-k0G2_bMYno56j7lep2IDdz7jsH_wQZMvw/edit#gid=0']
    start_urls = ['https://accounts.google.com/ServiceLogin?service=wise&passive=1209600']

    def parse(self, response):
        driver = webdriver.PhantomJS(executable_path=settings.PHANTOMJS_PATH)
        driver.get(response.url)
        elem_pass = driver.find_elements_by_css_selector("input[type='password']")
        btn_login = driver.find_elements_by_id('signIn')
        if elem_pass:
            elem_pass[0].send_keys('075686zwd717.')
        btn_login[0].click()
        page = response.url.split('/')[-2]
        filename = os.path.join(max_settings.BASE_DIR, max_settings.THRESHOLD_TXT, '%s.html' % page)
        with open(filename, 'wb') as f:
            f.write(driver)
            pass
        self.log('Saved file %s' % filename)
