import json
import requests
import re
import scrapy
from fake_useragent import UserAgent

ua = UserAgent()


class Spider(scrapy.Spider):
    name = 'aqumarine'

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'IWusrsesckgd=jojhbQMjYWEdV9ohRKijJKalgxKEvPEPzVqoH/F2376n50ziaNRcMA==; '
                      'ICusrcartgd=be6d8ad2-c52e-49b8-83b2-f384a9feaa60; ASP.NET_SessionId=fml4b0tqtwa11fu3rmnfi24n',
            'Host': 'catalog.aquamarine.kz',
            'Pragma': 'no-cache',
            'Referer': 'http://catalog.aquamarine.kz/catalog/index.aspx',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': ua.random
        }
        self.domain = 'http://catalog.aquamarine.kz/catalog/item.ashx?id='
        self.final = []
        self.count = 0

    def start_requests(self):
        urls = [
            'http://catalog.aquamarine.kz/catalog/products.ashx?rnd=469708377&q=&spec=&mip=167&map=230088&mippg=960'
            '&mappg=14270&miw=0.15&maw=137.74&miq=1&maq=412&miprcs=999999.999&maprcs=0&page=1&sort=art-down&view=1'
            '&spc=1,&brid=7,&_=1595148439274'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page1, headers=self.headers)

    def parse_page1(self, response):
        if self.count != 0:
            req = requests.get(response.url, headers=self.headers)
            con = req.text
            js = json.loads(con)
            ids = re.findall(r'data-pid=\"(.*)\"\ssrc', js['productsHtml'])
            for i in ids:
                self.final.append(self.domain + i)
            ind1 = response.url.find('page=')
            ind2 = response.url.find('&sort=')
            curPage = int(response.url[ind1 + 5:ind2])
            nextLink = response.url.replace('page=' + str(curPage), 'page=' + str(curPage + 1))
            if curPage != js['totalPages']:
                yield scrapy.Request(url=nextLink, callback=self.parse_page1, headers=self.headers)
            else:
                with open('Aqumarine_links.json', 'w') as out:
                    json.dump(self.final, out)
        else:
            self.count += 1
            url = 'http://catalog.aquamarine.kz/catalog/products.ashx?rnd=469708377&q=&spec=&mip=167&map=230088&mippg' \
                  '=960&mappg=14270&miw=0.15&maw=137.74&miq=1&maq=412&miprcs=999999.999&maprcs=0&page=1&sort=art-down' \
                  '&view=1&spc=1,&brid=7,&_=1594327185645'
            yield scrapy.Request(url=url, callback=self.parse_page1, headers=self.headers)
