# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.contrib.loader.processor import Compose, TakeFirst
from scrapy.item import Item, Field

from .processors import filter_html


class BlogItem(Item):
    guid = Field(output_processor=TakeFirst())
    title = Field(output_processor=TakeFirst())
    published = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    description = Field(output_processor=Compose(TakeFirst(), filter_html))
    content = Field(output_processor=Compose(TakeFirst(), filter_html))
    categories = Field()
    author_name = Field(output_processor=TakeFirst())
    author_url = Field(output_processor=TakeFirst())

    image_urls = Field()
    images = Field()
    local_url = Field()
    
    def is_valid(self):
        for c in self['categories']:
            if c.lower() in ('planet-idjs', 'javascript-id'):
                return True
        return False
