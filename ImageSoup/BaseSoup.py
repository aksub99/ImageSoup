import abc
import urllib.request
from pymongo import MongoClient


class BaseSoup(object):
    def setup_db(self):
        self.client = MongoClient()
        self.db = self.client.AuNP
        self.collection = self.db.Paper_Raw_HTML
    
    @property
    def base_url(self):
        raise NotImplementedError

    def create_full_url(self, partial: str) -> str:
        if not partial.startswith("http"):
            return self.base_url + partial
        else:
            return partial

    def parse(self, html_str):
        self.setup_db()
        results = self._parse(html_str)
        return results

    @staticmethod
    @abc.abstractmethod
    def _parse(html_str):
        raise NotImplementedError
