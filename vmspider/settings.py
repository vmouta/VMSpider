# Scrapy settings for vmspider project

BOT_NAME = 'vmscrapy'
BOT_VERSION = '0.1'

SPIDER_MODULES = ['vmspider.vmscrapy.spiders']
NEWSPIDER_MODULE = 'vmspider.vmscrapy.spiders'
DEFAULT_ITEM_CLASS = 'vmspider.vmscrapy.items.Website'

USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = {'vmspider.vmscrapy.pipelines.FilterWordsPipeline': 1}


