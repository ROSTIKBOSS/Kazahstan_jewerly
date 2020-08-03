import scrapy
import json
import time

from fake_useragent import UserAgent

ua = UserAgent()


class Spider(scrapy.Spider):
    name = 'test'

    def start_requests(self):
        self.final = []
        self.total = 0
        self.count = 0
        urls = [
            'https://sokolov.ru/jewelry-catalog/silver/?page=1'
        ]
        self.domain = 'https://sokolov.ru'
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page1, headers={'user-agent': ua.random})

    def parse_page1(self, response):
        sel = scrapy.Selector(response)
        links = sel.css('div.product-list a.product-description::attr(href)').extract()
        if len(links) != 0:
            self.total += len(links)
            for item in links:
                d1 = {
                    'url': self.domain + str(item)
                }
                self.final.append(d1)
                time.sleep(0.3)
                yield scrapy.Request(url=d1['url'], callback=self.parse_page2, headers={'user-agent': ua.random},
                                     meta={"dict": d1})
            ind = response.url.find('=')
            page = int(response.url[ind + 1:]) + 1
            next_page = response.url[:ind + 1] + str(page)
            yield scrapy.Request(url=next_page, callback=self.parse_page1, headers={'user-agent': ua.random})

    def parse_page2(self, response):
        self.count += 1
        cur_d = response.meta.get('dict')
        sel = scrapy.Selector(response)
        uid = sel.css('div.product-article::text').get()
        cur_d['id'] = uid.split(':')[1].strip()
        name = sel.css('h1.product-title::text').get()
        cur_d['name'] = name
        brand = sel.css('div.name:contains(\'Бренд\') + div span::text').get()
        cur_d['brand'] = brand
        forWho = sel.css('div.name:contains(\'Для кого\') + div span::text').get()
        cur_d['forWho'] = forWho
        typeOfInput = sel.css('div.name:contains(\'Тип вставки\') + div span::text').extract()
        cur_d['typeOfInput'] = typeOfInput
        typeOfMaterial = sel.css('div.name:contains(\'Тип металла\') + div span::text').get()
        cur_d['typeOfMaterial'] = typeOfMaterial
        proba = sel.css('div.name:contains(\'Проба\') + div span::text').get()
        cur_d['proba'] = proba
        outside = sel.css('div.name:contains(\'Покрытие\') + div span::text').extract()
        cur_d['outside'] = outside
        width = sel.css('div.name:contains(\'Ширина\') + div span::text').get()
        cur_d['width'] = width
        height = sel.css('div.name:contains(\'Высота\') + div span::text').get()
        cur_d['height'] = height
        length = sel.css('div.name:contains(\'Длина\') + div span::text').get()
        cur_d['length'] = length
        badges = sel.css('div.product div.badge::text').extract()
        cur_d['badges'] = badges
        photos = sel.css('div.slider-for div.swiper-wrapper source::attr(srcset)').extract()
        cur_d['photos'] = photos
        video = sel.css('video source[type=\'video/mp4\']::attr(src)').get()
        cur_d['video'] = video
        checkForComplet = sel.css('h2:contains(\'Дополните свой образ\')::text').get()
        if checkForComplet:
            cur_d['complet'] = 'есть комплект'
        else:
            cur_d['complet'] = checkForComplet
        collection = sel.css('div.name:contains(\'Коллекция\') + div span::text').get()
        cur_d['collection'] = collection
        sizes = sel.css('div.sizes-header:contains(\'Размер\') + div button::text').extract()
        cur_d['sizes'] = sizes
        group = sel.css('div.breadcrumbs a span::text').extract()
        cur_d['group'] = group
        price = sel.css('span.price::text').get()
        cur_d['price'] = price
        if self.count == self.total:
            with open('SokolovRozn.json', 'w') as out:
                json.dump(self.final, out)
