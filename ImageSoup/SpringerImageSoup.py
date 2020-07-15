import re
import json
import urllib.request
from pymongo import MongoClient
from bs4 import BeautifulSoup

from ImageSoup.BaseSoup import BaseSoup
from ImageSoup.utils.database import get_year

class SpringerSoup(BaseSoup):

    def _extract_images(self, images):
        image_meta = {'figures':[]}
        for image in images:
            # Title
            title = image.find('span', attrs={'class': 'CaptionNumber'}).get_text()

            # Caption
            caption = image.find('p', attrs={'class': 'SimplePara'}).get_text()

            # URL
            img_url = image.find('a').get('href')

            image_meta['figures'].append({'Image_URL': img_url, 'Caption': caption, 'Title': title})
        return image_meta

    def _parse(self, html_string) -> dict:
        paper = BeautifulSoup(html_string, 'html.parser')
        images = paper.find_all('figure')
        return self._extract_images(images)

SpringerImageSoup = SpringerSoup()
