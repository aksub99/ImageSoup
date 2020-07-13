import json
import urllib.request
from pymongo import MongoClient
from bs4 import BeautifulSoup

from ImageSoup.BaseSoup import BaseSoup

class RSCSoup(BaseSoup):

    base_url = "https://pubs.rsc.org"

    def _extract_images(self, image_tables):
        image_meta = {}
        for image_table in image_tables:
            img_meta = {}
            # URL
            partial = image_table.find('img').get('src')
            img_url = self.create_full_url(partial)
            
            # Caption
            caption = image_table.find('span', attrs={'class': 'graphic_title'}).get_text()
            
            # Title
            title = image_table.find('td', attrs={'class': 'image_title'}).find('b').get_text().strip()

            img_meta["Image_URL"] = img_url
            img_meta["Caption"] = caption

            image_meta[title] = img_meta
        return image_meta

    def _parse(self, html_string) -> dict:
        paper = BeautifulSoup(html_string, 'html.parser')
        image_tables = paper.find_all('div', attrs={'class': 'image_table'})
        return self._extract_images(image_tables)

RSCImageSoup = RSCSoup()
print(RSCImageSoup)
