# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os

BOT_NAME = os.environ['SCRAPY_HOST']

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
IMAGES_HOST = os.environ['SCRAPY_IMAGES_HOST']

TELNETCONSOLE_ENABLED = False
WEBSERVICE_ENABLED = False

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'crawler (+http://%s)' % os.environ['SCRAPY_HOST']

DOWNLOAD_DELAY = 2

ITEM_PIPELINES = {
    'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    'crawler.pipelines.ValidatePipeline': 800,
    'crawler.pipelines.ExistPipeline': 801,
    'crawler.pipelines.ImagePipeline': 802,
    'crawler.pipelines.SavePipeline': 803,
}

IMAGES_STORE = os.environ['SCRAPY_IMAGES_STORE']
