# -*- coding: utf-8 -*-
import scrapy


class OsuSpiderSpider(scrapy.Spider):
    name = 'osu_spider'
    allowed_domains = ['osu.ppy.sh']
    start_urls = ['https://osu.ppy.sh/rankings/osu/performance']

    def parse(self, response):
        for href in response.css('.ranking-page-table__row h1 a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url,callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'rank':response.css('.ranking-page-table_column ranking-page-table__column--rank a::text').extract(),
            'name':response.css('.ranking-page-table__user-link-text js-usercard a::text').extract(),
            'country':response.css('.flag-country .data-orig-title::text').extract(),
            'performance':response.css(".ranking-page-table__column ranking-page-table__column--focused"
                                       "a::text").extract(),
            'link':response.url,
        }