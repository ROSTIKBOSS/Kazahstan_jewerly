import scrapy
import json
import requests
import pandas as pd
import re


from fake_useragent import UserAgent

ua = UserAgent()


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


links = pd.read_excel('Links.xls')
urls = list(set(links[0].tolist()))
urls = [item.replace('product_modal', 'product') for item in urls]
final = []
count = 1
# urls = ['http://tdserebro.ru/astana/product/719876', 'https://tdserebro.ru/astana/product/718439',
# 'https://tdserebro.ru/astana/product/711939']
with open('Cookie.txt', 'r') as in1:
    cookie = in1.readline()

flag_spec = 0
try:
    for item in urls:
        flag_spec += 1
        print(item)
        print(count)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': ''+cookie,
            'Host': 'tdserebro.ru',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua.random
        }
        req = requests.get(item, headers=headers)
        # print(req.request.headers)
        sel = scrapy.Selector(req)
        d1 = {
            'url': item,
            'name': sel.css('title::text').get().strip(),
            'brand': sel.css('div.description h4 > a::text').get(),
            'groupName': sel.css('ol.breadcrumbs li span::text').extract(),
            'groupLinks': sel.css('ol.breadcrumbs li a::attr(href)').extract(),
            'photos': sel.css('div#img-gallery a img::attr(src)').extract(),
            'collect': sel.css('div.products.kit.col-xs-12 h4 > a.product_link::attr(href)').extract(),
            'attached': sel.css('div.products.recommended.col-xs-12 h4 > a.product_link::attr(href)').extract(),
            'badges': sel.css('div.markers_product').get(),

            'probeALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Проба\')::text').get(),
            'insertALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Вставка\')::text').get(),
            'outsideALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Покрытие\')::text').get(),
            'themeALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Тематика\')::text').get(),
            'typeLockALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Виды замков\')::text').get(),
            'collectionALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Коллекция\')').get(),
            'typePletALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Вид плетения\')::text').get(),
            'colorALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Цвет\')::text').get(),
            'posadkaALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Посадка\')::text').get(),
            'shinkaALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'ШиринаШинки\')::text').get(),
            'zodiakALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Зодиак\')::text').get(),
            'dataALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') div.col-xs-6').extract(),

            'probeAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Проба\')::text').get(),
            'insertAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Вставка\')::text').get(),
            'outsideAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Покрытие\')::text').get(),
            'themeAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Тематика\')::text').get(),
            'typeLockAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Виды замков\')::text').get(),
            'collectionAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Коллекция\')').get(),
            'typePletAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Вид плетения\')::text').get(),
            'colorAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Цвет\')::text').get(),
            'posadkaAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Посадка\')::text').get(),
            'shinkaAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'ШиринаШинки\')::text').get(),
            'zodiakAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Зодиак\')::text').get(),
            'dataAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') div.col-xs-6').extract(),
        }
        count += 1
        final.append(d1)
except:
    print('Error')
    for item in urls[flag_spec:]:
        print(item)
        print(count)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': ''+str(cookie),
            'Host': 'tdserebro.ru',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua.random
        }
        req = requests.get(item, headers=headers)
        # print(req.request.headers)
        sel = scrapy.Selector(req)
        d1 = {
            'url': item,
            'name': sel.css('title::text').get().strip(),
            'brand': sel.css('div.description h4 > a::text').get(),
            'groupName': sel.css('ol.breadcrumbs li span::text').extract(),
            'groupLinks': sel.css('ol.breadcrumbs li a::attr(href)').extract(),
            'photos': sel.css('div#img-gallery a img::attr(src)').extract(),
            'collect': sel.css('div.products.kit.col-xs-12 h4 > a.product_link::attr(href)').extract(),
            'attached': sel.css('div.products.recommended.col-xs-12 h4 > a.product_link::attr(href)').extract(),
            'badges': sel.css('div.markers_product').get(),

            'probeALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Проба\')::text').get(),
            'insertALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Вставка\')::text').get(),
            'outsideALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Покрытие\')::text').get(),
            'themeALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Тематика\')::text').get(),
            'typeLockALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Виды замков\')::text').get(),
            'collectionALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Коллекция\')').get(),
            'typePletALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Вид плетения\')::text').get(),
            'colorALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Цвет\')::text').get(),
            'posadkaALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Посадка\')::text').get(),
            'shinkaALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'ШиринаШинки\')::text').get(),
            'zodiakALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') li:contains(\'Зодиак\')::text').get(),
            'dataALM': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АЛМ Основной\') div.col-xs-6').extract(),

            'probeAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Проба\')::text').get(),
            'insertAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Вставка\')::text').get(),
            'outsideAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Покрытие\')::text').get(),
            'themeAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Тематика\')::text').get(),
            'typeLockAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Виды замков\')::text').get(),
            'collectionAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Коллекция\')').get(),
            'typePletAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Вид плетения\')::text').get(),
            'colorAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Цвет\')::text').get(),
            'posadkaAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Посадка\')::text').get(),
            'shinkaAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'ШиринаШинки\')::text').get(),
            'zodiakAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') li:contains(\'Зодиак\')::text').get(),
            'dataAST': sel.css(
                'div.show-skus div.col-xs-12:contains(\'Склад - АСТ Основной\') div.col-xs-6').extract(),
        }
        count += 1
        final.append(d1)
    # with open('TD.json', 'w') as out:
    #     json.dump(final, out)

with open('TD.json', 'w') as out:
    json.dump(final, out)