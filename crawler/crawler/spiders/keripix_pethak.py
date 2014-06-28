from BeautifulSoup import BeautifulSoup
from dateutil.parser import parse as date_parse
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.spiders import XMLFeedSpider

from crawler.utils import unescape
from ..items import KeripixPethakItem

ALLOWED_TAGS = ['a', 'b', 'i', 'img', 'div', 'span']
ALLOWED_ATTRIBUTES = {
    '*': ['class'],
    'a':  ['href', 'title'],
    'img': ['alt', 'src', 'title'],
}

class KeripixPethakSpider(XMLFeedSpider):
    name = 'keripix_pethak'
    allowed_domains = ['keripix.pethak.com']
    start_urls = ['http://keripix.pethak.com/feed/']
    iterator = 'iternodes' # you can change this; see the docs
    itertag = 'item' # change it accordingly
    item_class = KeripixPethakItem

    class Meta:
        author_name = 'Akbar Hidayat'
        author_url = 'https://plus.google.com/u/0/+AkbarHidayat-keripix/about'

    def parse_node(self, response, selector):
        l = ItemLoader(item=self.item_class(), selector=selector, response=response)
        l.add_xpath('guid', 'guid/text()')
        l.add_xpath('title', 'title/text()')
        l.add_value('published', [date_parse(d) for d in \
                                  selector.xpath('pubDate/text()').extract()])
        l.add_xpath('url', 'link/text()')
        l.add_xpath('description', 'description/text()')
        l.add_xpath('content', '*[name()="content:encoded"]/text()')
        l.add_xpath('categories', 'category/text()')
        l.add_value('author_name', self.Meta.author_name)
        l.add_value('author_url', self.Meta.author_url)
        i = l.load_item()
        if not 'image_urls' in i:  i['image_urls'] = []

        sel = BeautifulSoup(markup=i['description'], isHTML=True)
        imgs = sel.findAll('img')
        if len(imgs):
            i['image_urls'] += (unescape(img['src']) for img in imgs)
        sel = BeautifulSoup(markup=i['content'], isHTML=True)
        imgs = sel.findAll('img')
        if len(imgs):
            i['image_urls'] += (unescape(img['src']) for img in imgs)
        return i
