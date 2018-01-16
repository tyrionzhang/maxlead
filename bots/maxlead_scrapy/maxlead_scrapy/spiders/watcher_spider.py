# -*- coding: utf-8 -*-

import scrapy,time,os
from bots.maxlead_scrapy.maxlead_scrapy.items import ListingWacherItem
from maxlead_site.models import UserAsins
from django.db.models import Count
from selenium import webdriver
from bots.maxlead_scrapy.maxlead_scrapy import settings


class WatcherSpider(scrapy.Spider):

    name = "watcher_spider"
    start_urls = []
    res = list(UserAsins.objects.filter(is_use=True).values('aid').annotate(count=Count('aid')))

    def __init__(self, asin=None, *args, **kwargs):
        url1 = "https://www.amazon.com/gp/offer-listing/%s/ref=dp_olp_all_mbc?ie=UTF8&condition=new&th=1&psc=1"
        super(WatcherSpider, self).__init__(*args, **kwargs)
        if asin:
            urls = url1 % asin
            self.start_urls.append(urls)
        else:
            if self.res:
                for re in self.res:
                    asins = UserAsins.objects.values('aid','review_watcher','listing_watcher','sku','ownership').filter(aid=re['aid'])[0]
                    urls = url1 % asins['aid']
                    self.start_urls.append(urls)

    def parse(self, response):
        res_asin = response.url.split('/')
        driver = webdriver.PhantomJS(executable_path=settings.PHANTOMJS_PATH)
        driver.get(response.url)
        # img = Image.open(StringIO(base64.b64decode(driver.get_screenshot_as_base64())))
        dir_path = '%s/%s' % (settings.IMAGES_STORE, 'listing_watcher')
        dir_path1 = '%s/%s' % (settings.IMAGES, 'listing_watcher')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        now_time = time.time()
        image_file_name = '%s.png' % now_time
        file_path = '%s/%s' % (dir_path, image_file_name)
        path_str = '%s/%s' % (dir_path1, image_file_name)
        driver.get_screenshot_as_file(file_path)
        driver.quit()

        for k,wa in enumerate(response.css('div.a-spacing-double-large div.olpOffer'),1):

            asin_id = res_asin[5]
            item = ListingWacherItem()
            item['asin'] = asin_id
            item['images'] = path_str
            item['seller'] = wa.css('div.olpSellerColumn h3.olpSellerName a::text').extract_first()
            seller_link= wa.css('div.olpSellerColumn h3.olpSellerName a::attr(href)').extract_first()
            if seller_link:
                item['seller_link'] = 'https://www.amazon.com%s' % seller_link
            if not item['seller']:
                item['seller'] = wa.css('div.olpSellerColumn h3.olpSellerName img::attr(alt)').extract_first()
            item['price'] = wa.css('div.olpPriceColumn span.olpOfferPrice::text').extract_first()
            if item['price']:
                item['price'] = item['price'].replace('\n','').strip()
            item['shipping'] = wa.css('div.olpPriceColumn p.olpShippingInfo b::text').extract_first()
            if not item['shipping']:
                a = wa.css('div.olpPriceColumn p.olpShippingInfo span.olpShippingPrice').extract()
                if a:
                    item['shipping'] = wa.css('div.olpPriceColumn p.olpShippingInfo span.olpShippingPrice::text').extract_first()+ \
                                       wa.css('div.olpPriceColumn p.olpShippingInfo span.olpShippingPriceText::text').extract_first()
            prime = wa.css('div.olpPriceColumn span.supersaver').extract()
            is_fba = wa.css('div.olpDeliveryColumn div.olpBadgeContainer')
            if is_fba:
                is_fba = is_fba.css('a.olpFbaPopoverTrigger::text').extract_first().replace('\n','').strip()
                if is_fba == 'Fulfillment by Amazon':
                    item['fba'] = 1
            else:
                item['fba'] = 0
            if prime:
                item['prime'] = 1
            else:
                item['prime'] = 0
            if k == 1:
                item['winner'] = 1
            else:
                item['winner'] = 0
            yield item

        next_page = response.css('li.a-last a::attr("href")').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)