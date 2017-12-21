# -*- coding: utf-8 -*-

import scrapy
from maxlead_site.models import UserAsins
from django.db.models import Count
from bots.maxlead_scrapy.maxlead_scrapy.items import AnswersItem
from maxlead_site.models import Questions

class QaSpider(scrapy.Spider):

    name = "qa_spider"
    start_urls = []
    url = "https://www.amazon.com/ask/questions/asin/%s/"
    res = list(UserAsins.objects.filter(is_use=True).values('aid','review_watcher','listing_watcher','sku').annotate(count=Count('aid')))

    if res:
        for re in res:
            asin = url % (re['aid'])
            start_urls.append(asin)

    def parse(self, response):
        res_asin = response.url.split('/')
        for qa_a in response.css('div.askInlineWidget div.askTeaserQuestions>.a-spacing-base'):
            qa_url = qa_a.css('.a-spacing-base .a-link-normal::attr("href")').extract_first()
            question = qa_a.css('.a-spacing-base .a-link-normal::text').extract_first().replace('\n','').strip()
            votes = int(qa_a.css('ul.voteAjax span.count::text').extract_first())
            asin_id = res_asin[6]
            qa_data = Questions(question=question, asin=asin_id, votes=votes)
            qa_data.id
            qa_data.save()
            qa_url = qa_url + '?qa_id=%s' % qa_data.id
            qa_page = response.urljoin(qa_url)
            yield scrapy.Request(qa_page, callback=self.get_answer)


        next_page = response.css('div#askPaginationBar li.a-last a::attr("href")').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def get_answer(self,response):
        qa_sp = response.url.split('?')[-1]
        qa_id = qa_sp.split('=')[-1]
        asked = response.css('div.a-spacing-base div.a-text-left::text').extract_first().replace('\n','').strip()
        qa_obj = Questions.objects.filter(id=qa_id)
        qa_obj.update(asked=asked)
        for asw in response.css('div.askAnswersAndComments>.a-section'):
            item = AnswersItem()
            item['person'] = asw.css('span.a-color-tertiary::text').extract_first()
            if item['person']:
                item['person'] = item['person'].replace('\n','').strip()
            item['answer'] = asw.css('span::text').extract_first()
            item['question'] = list(qa_obj)[0]
            yield item