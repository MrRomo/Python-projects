import requests
import bs4
from common import config


class NewsPage:

    def __init__(self, news_sites_uid, url):
        self._config = config()['web'][news_sites_uid]
        self._queries = self._config['queries']
        self._html = None

        self._visit(url)

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):

        response = requests.get(url)
        response.raise_for_status()

        self._html = bs4.BeautifulSoup(response.text, 'html.parser')


class HomePage(NewsPage):

    def __init__(self, news_sites_uid, url):
        super().__init__(news_sites_uid, url)

    @property
    def article_links(self):
        link_list = []

        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)

        return set(link['href'] for link in link_list)


class ArticlPage(NewsPage):

    def __init__(self, news_sites_uid, url):
        self.link =  url
        super().__init__(news_sites_uid, url)

    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''
  
    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''
