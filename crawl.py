import requests
import re
from bs4 import BeautifulSoup
from PIL import Image
from urllib.request import Request,urlopen
import numpy as np
import cv2

import os

class Webcrawler:

    def __init__(self, i):
        self.discovered_web=[]
        self.i=i

    def crawl(self, start_url):
        queue=[start_url]
        self.discovered_web.append(start_url)

        while queue:

            actual_url = queue.pop(0)
            self.image_scraper(actual_url)
            print(actual_url)

            actual_url_html = self.read_raw_html(actual_url)

            for url in self.get_links_from_html(actual_url_html):
                if url not in self.discovered_web:
                    self.discovered_web.append(url)
                    queue.append(url)

    def image_scraper(self, actual_url):
        URL = actual_url # Replace this with the website's URL
        getURL = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"})
        # print(getURL.status_code)

        soup = BeautifulSoup(getURL.text, 'html.parser')

        images = soup.find_all('img')
        # print(images)

        imageSources = []

        for image in images:
            imageSources.append(image.get('src'))
        for image in imageSources:
            self.i+=1
            # n=str(image).split('/')[-1]
            # print(image)
            name=str(self.i)+'.jpeg'
            print(name)
            my_path='C:/Users/vibhu/Desktop/projects/webcrawler/images/'+name

            try:
                t = self.url_to_image(image)
                t = Image.fromarray(t, "RGB")
                t.save(my_path)    
            except KeyboardInterrupt:
                exit(0)
            except:
                pass

    def get_links_from_html(self, raw_html):

        return re.findall("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", raw_html)
    
    def read_raw_html(self, url):
        raw_html=''

        try:
            raw_html = requests.get(url).text
        except Exception as e:
            pass
        return raw_html
    
    def url_to_image(self, url, readFlag=cv2.IMREAD_COLOR):
        # download the image, convert it to a NumPy array, and then read
        # it into OpenCV format
        req=Request(url,headers={"User-Agent":"Mozilla/5.0"})
        resp = urlopen(req)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, readFlag)

        # return the image
        return image

link1='https://towardsdatascience.com/understanding-1d-and-3d-convolution-neural-network-keras-9d8f76e29610'
link2='https://www.rottentomatoes.com/top/bestofrt/'

crawler= Webcrawler(0)
crawler.crawl(link2)