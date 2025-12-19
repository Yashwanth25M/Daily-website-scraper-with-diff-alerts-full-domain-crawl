import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from storage.db import save_snapshot
from diff_engine.hasher import hash_text


class DomainSpider(scrapy.Spider):
    name = "domain"

    def __init__(self, domain=None, run_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_urls = [domain]
        self.allowed_domains = [urlparse(domain).hostname]
        self.run_id = run_id

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")

        main = soup.find("main")
        if main:
            text = main.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

        h = hash_text(text)
        save_snapshot(response.url, h, text, self.run_id)

        for href in response.css("a::attr(href)").getall():
            next_url = urljoin(response.url, href)
            if urlparse(next_url).hostname == self.allowed_domains[0]:
                yield response.follow(next_url, self.parse)
