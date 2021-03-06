import scrapy

from myproject.items import Page
from myproject.utils import get_content
from myproject.utils import bs4_test
#from myproject.utils import mecab_test


class BroadSpider(scrapy.Spider):
    name = 'broad'
    # はてなブックマークの新着エントリーページ。
    start_urls = ['https://b.hatena.ne.jp/entrylist/all']

    def parse(self, response):
        """
        はてなブックマークの新着エントリーページをパースする。
        """
        # 個別のWebページへのリンクをたどる。
        for url in response.css('.entrylist-contents-title > a::attr("href")').getall():
            # parse_page() メソッドをコールバック関数として指定する。
            yield scrapy.Request(url, callback=self.parse_page)

        # page=の値が1桁である間のみ「次の20件」のリンクをたどる（最大9ページ目まで）。
        url_more = response.css('.entrylist-readmore > a::attr("href")').re_first(r'.*\?page=\d{1,2}$')
        if url_more:
            yield response.follow(url_more)

    def parse_page(self, response):
        """
        個別のWebページをパースする。
        """
        # utils.pyに定義したget_content()関数でタイトルと本文を抽出する。
        title, content, kimoti = get_content(response.text)
        count_image =   bs4_test(response.text)
        #hinshi, word = mecab_test(response.text)
        # Pageオブジェクトを作成してyieldする。
        yield Page(url=response.url, title=title, content=content,kimoti=kimoti)
