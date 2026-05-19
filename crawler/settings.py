BOT_NAME = 'douban_movie'
SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 4
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
}

DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.RandomUserAgentMiddleware': 400,
    'crawler.middlewares.CookieMiddleware': 700,
}

FEEDS = {
    '../data/movies.jsonl': {'format': 'jsonlines', 'encoding': 'utf-8', 'overwrite': True},
    '../data/persons.jsonl': {'format': 'jsonlines', 'encoding': 'utf-8', 'overwrite': True},
}

FEED_EXPORT_FIELDS = None
LOG_LEVEL = 'INFO'
