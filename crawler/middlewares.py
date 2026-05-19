import random
from fake_useragent import UserAgent


class RandomUserAgentMiddleware:
    def __init__(self):
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.ua.random


class CookieMiddleware:
    COOKIES = [
        'bid=AbCdEf123456; ll="118282"; __yadk_uid=abcdefghijk;',
        'bid=GhIjKl789012; ll="118282"; __yadk_uid=lmnopqrstuv;',
        'bid=MnOpQr345678; ll="108288"; __yadk_uid=wxyzabcdefg;',
    ]

    def process_request(self, request, spider):
        request.headers['Cookie'] = random.choice(self.COOKIES)
