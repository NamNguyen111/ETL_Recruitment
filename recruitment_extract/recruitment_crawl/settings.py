# Scrapy settings for recruitment_crawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "bidetu"

SPIDER_MODULES = ["recruitment_crawl.spiders"]
NEWSPIDER_MODULE = "recruitment_crawl.spiders"

# Scrapy keep an eye on response time from server to see if the server is overloaded or not
DOWNLOAD_DELAY = 17
RANDOMIZE_DOWNLOAD_DELAY = True

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 15
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

CONCURRENT_REQUESTS = 3
COOKIES_ENABLED = True

PLAYWRIGHT_BROWSER_TYPE = 'chromium'
PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': False  # Keep the browser visible for debugging
}


DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # Vô hiệu hóa mặc định
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,   # Fake User-Agent Middleware
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,   # Proxy Middleware
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,         # Rotating Proxy Middleware
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,          # Ban Detection Middleware
}

FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # Sử dụng fake-useragent
    'scrapy_fake_useragent.providers.FakerProvider',          # Sử dụng faker
    'scrapy_fake_useragent.providers.FixedUserAgentProvider', # User-Agent cố định (nếu cần)
]

# Thêm vào headers chuẩn trong start_requests hoặc settings.py
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",  # Do Not Track
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "User-Agent": "your-user-agent-here",
}


ROTATING_PROXY_LIST = [
    'http://rdQjur:HqnuDj@185.126.85.244:9611',
    'http://rdQjur:HqnuDj@147.45.53.183:9841',
    'http://rdQjur:HqnuDj@188.119.125.173:9431',
    'http://rdQjur:HqnuDj@188.119.127.80:9891',
    'http://rdQjur:HqnuDj@31.129.21.233:9235',
    'http://pdkw3n2t:pDkW3n2T@14.225.48.107:6666',
    'http://jaoi1c4z:jAoI1c4Z@103.74.104.109:36781',
    'http://xBQwtq:kFWVOA@160.30.190.186:31324',
    'http://bvih8609:COHbzq8501@203.145.44.242:17111',
    'http://proxy000015:Http9999@103.129.127.214:3181',
]

ROTATING_PROXY_PAGE_RETRY_TIMES = 5  # Số lần retry khi gặp lỗi proxy
ROTATING_PROXY_BACKOFF_BASE = 300    # Thời gian chờ trước khi thử lại proxy, tính bằng giây

# Các cấu hình khác trong dự án
ROBOTSTXT_OBEY = True
# Nếu cần đặt User-Agent cố định (không phải ngẫu nhiên)

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "recruitment_crawl (+http://www.yourdomain.com)"

# Obey robots.txt rules

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "recruitment_crawl.middlewares.RecruitmentCrawlSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "recruitment_crawl.middlewares.RecruitmentCrawlDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "recruitment_crawl.pipelines.RecruitmentCrawlPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
