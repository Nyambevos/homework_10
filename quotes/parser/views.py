import json
from django.shortcuts import redirect, render

import scrapy
from scrapy.crawler import CrawlerProcess

from quoteapp.models import Quote, Author, Tag

# Create your views here.

def main(request):
    return render(request, 'parser/index.html')

class AuthorItem(scrapy.Item):
    fullname = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field()

class QuoteItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class Django_DB_Pipeline:
    def open_spider(self, spider):
        self.authors = []
        self.quotes = []

    def close_spider(self, spider):
        for item in self.authors:
            author_obj, _ = Author.objects.get_or_create(**item)

        for item in self.quotes:
            try:
                author_obj = Author.objects.get(fullname=item['author'])
                quote_obj = Quote.objects.create(quote=item['quote'], author=author_obj)
            except Exception as err:
                print(err, item['author'], '==========================')

            for tag in item['tags']:
                tag_obj, _ = Tag.objects.get_or_create(name=tag)
                quote_obj.tags.add(tag_obj)
        

    def process_item(self, item, spider):
        if isinstance(item, AuthorItem):
            self.authors.append(dict(item))
        elif isinstance(item, QuoteItem):
            self.quotes.append(dict(item))
        return item

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {
        "ITEM_PIPELINES": {
            Django_DB_Pipeline: 100,
        }
    }
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            item = QuoteItem()
            item['quote'] = quote.xpath('span[@class="text"]/text()').get()
            item['author'] = quote.xpath('span/small[@class="author"]/text()').get()
            item['tags'] = quote.xpath('div[@class="tags"]/a/text()').getall()
            yield item

            author_link = quote.xpath("span/a/@href").get()
            yield response.follow(self.start_urls[0] + author_link, callback=self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        item = AuthorItem()
        item['fullname'] = response.xpath("//h3[@class='author-title']/text()").get()
        item['born_date'] = response.xpath("//span[@class='author-born-date']/text()").get()
        item['born_location'] = response.xpath("//span[@class='author-born-location']/text()").get()
        item['description'] = response.xpath("//div[@class='author-description']/text()").get()
        yield item

            
def run_spider(request):
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
    return redirect(to='quoteapp:main')
