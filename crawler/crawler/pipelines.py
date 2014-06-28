# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sh
import sys
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from jinja2 import (
    Environment as JinjaEnvironment,
    PackageLoader as JinjaPackageLoader,
)
from scrapy.exceptions import DropItem
from urlparse import urlparse

from crawler import settings
from crawler.utils import escape


INDEX_ITEMS = 30

WEB_PROJECT_DIR = os.path.join(os.path.dirname(settings.ROOT_DIR), 'web')
WEB_SETTINGS_MODULE = 'web.settings'


def setup_django__web():
    sys.path.append(WEB_PROJECT_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = WEB_SETTINGS_MODULE

class ExistPipeline(object):
    def process_item(self, item, spider):
        setup_django__web()
        from postindex.models import PostIndex

        try:
            PostIndex.objects.get(guid=item['guid'])
            raise DropItem('Already existed.')
        except ObjectDoesNotExist:
            pass
        return item


class ImagePipeline(object):
    def process_item(self, item, spider):
        year = item['published'].year
        month = item['published'].month
        for img in item['images']:
            # moves files from temp dir to uploads dir
            img_src = os.path.join(settings.IMAGES_STORE, img['path'])
            uploads_dir = os.path.join(
                os.path.dirname(settings.ROOT_DIR),
                'uploads',
            )
            relative_img_dest = os.path.join(str(year), str(month), img['path'])
            img_dest = os.path.join(uploads_dir, relative_img_dest)
            img_dest_dir = os.path.dirname(img_dest)
            if not os.path.exists(img_dest_dir):
                os.makedirs(img_dest_dir)
            sh.cp(img_src, img_dest)

            url_img_dest = os.path.join(settings.IMAGES_HOST, relative_img_dest)
            # update contents to reflect local image paths
            item['content'] = item['content'].replace(
                img['url'], url_img_dest,
            )
            item['description'] = item['description'].replace(
                img['url'], url_img_dest,
            )

            escaped_img_url = escape(img['url'])
            item['content'] = item['content'].replace(
                escaped_img_url, url_img_dest,
            )
            item['description'] = item['description'].replace(
                escaped_img_url, url_img_dest,
            )
        return item


class ValidatePipeline(object):
    def process_item(self, item, spider):
        if not item.is_valid():
            raise DropItem('Failed validation.')
        return item


class SavePipeline(object):
    def __init__(self):
        self.jinja = JinjaEnvironment(
            loader=JinjaPackageLoader('crawler', 'templates'),
        )

    def process_item(self, item, spider):
        year = item['published'].year
        month = item['published'].month
        # normalize filename so it ended with .html
        filename = urlparse(item['url'], allow_fragments=False)
        filename = filename.path.rstrip('/')
        filename = os.path.basename(filename)
        filename = os.path.splitext(filename)[0] + '.html'

        ## save blog page content
        webroot_dir = os.path.join(os.path.dirname(settings.ROOT_DIR), 'htdocs')
        base_dir = os.path.join(webroot_dir, str(year), str(month))
        if not os.path.exists(base_dir):  os.makedirs(base_dir)
        item_template = self.jinja.get_template('blog_item.html')
        html = item_template.render(object=item).encode('utf-8')
        with open(os.path.join(base_dir, filename), 'w') as f:
            f.write(html)

        teaser_dir = os.path.join(
            webroot_dir, 'includes', 'teasers', str(year), str(month),
        )
        if not os.path.exists(teaser_dir):  os.makedirs(teaser_dir)
        with open(os.path.join(teaser_dir, filename), 'w') as f:
            f.write(item['description'].encode('utf-8'))

        ## save to scraper index
        setup_django__web()
        from postindex.models import PostIndex

        post = PostIndex()
        post.author_name = item['author_name']
        post.author_url = item['author_url']
        post.guid = item['guid']
        post.local_url = os.path.join('/', str(year), str(month), filename)
        post.local_desc_url = os.path.join(
            '/', 'includes', 'teasers',
            str(year), str(month), filename,
        )
        post.month = month
        post.published = item['published'].isoformat()
        post.title = item['title']
        post.url = item['url']
        post.year = year
        post.save()

        ## save to html index
        data = PostIndex.objects.order_by('-published').filter(
            year=year, month=month,
        )[:INDEX_ITEMS]
        item_template = self.jinja.get_template('blog_index.html')
        html = item_template.render(
            count=INDEX_ITEMS, object=data,
        ).encode('utf-8')
        with open(os.path.join(base_dir, 'index.html'), 'w') as f:
            f.write(html)

        ## update homepage
        now = datetime.now()
        if now.year == year and now.month == month:
            with open(os.path.join(webroot_dir, 'index.html'), 'w') as f:
                f.write(html)

        return item
