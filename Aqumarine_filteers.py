import json
import requests
import re
import scrapy
from fake_useragent import UserAgent

ua = UserAgent()

js_final = []
headers = {
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
cur = {
    'typeInsert': [],
    'Insert': [],
    'colorOfInsert': [],
    'Collection': [],
    'Sizes': [],
}
cur1 = {}

req = requests.get('http://catalog.aquamarine.kz/catalog/index.aspx', headers=headers)
sel = scrapy.Selector(req)
types = sel.css('table.selector td:contains(\'Тип вставки\') div div label')
for i in types:
    name = i.css('::text').get()
    cur1[name] = []
    flag = 1
    curPage = '1'
    while flag != 0:
        print(name)
        curPage = str(curPage)
        url = 'http://catalog.aquamarine.kz/catalog/products.ashx?rnd=186262780&q=&spec=&mip=210&map=232010&mippg=960' \
              '&mappg=14270&miw=0.2&maw=137.74&miq=1&maq=411&miprcs=999999.999&maprcs=0&page=[INDEX]&sort=art-down&view=1&spc' \
              '=1,&[TYPE],&brid=7,&_=1595153244242 '
        type = i.css('::attr(for)').get()
        type = type.replace('-', '=')
        url = url.replace('[TYPE]', type)
        url = url.replace('[INDEX]', curPage)
        req = requests.get(url, headers=headers)
        con = req.text
        js = json.loads(con)
        ids = re.findall(r'data-pid=\"(.*)\"\ssrc', js['productsHtml'])
        ind1 = url.find('page=')
        ind2 = url.find('&sort=')
        curPage = int(url[ind1 + 5:ind2])
        print(curPage)
        print(js['totalPages'])
        if curPage != js['totalPages']:
            curPage += 1
            for j in ids:
                cur1[name].append('http://catalog.aquamarine.kz/catalog/item.ashx?id=' + j)
        else:
            flag = 0

with open('Aqumarine_types.json', 'w') as out:
    json.dump(cur1, out)


types = sel.css('table.selector td:contains(\'Вставка\') div div label')
for i in types:
    name = i.css('::text').get()
    cur1[name] = []
    flag = 1
    curPage = '1'
    while flag != 0:
        print(name)
        curPage = str(curPage)
        url = 'http://catalog.aquamarine.kz/catalog/products.ashx?rnd=186262780&q=&spec=&mip=210&map=232010&mippg=960' \
              '&mappg=14270&miw=0.2&maw=137.74&miq=1&maq=411&miprcs=999999.999&maprcs=0&page=[INDEX]&sort=art-down&view=1&spc' \
              '=1,&[TYPE],&brid=7,&_=1595153244242 '
        type = i.css('::attr(for)').get()
        type = type.replace('-', '=')
        url = url.replace('[TYPE]', type)
        url = url.replace('[INDEX]', curPage)
        req = requests.get(url, headers=headers)
        con = req.text
        js = json.loads(con)
        ids = re.findall(r'data-pid=\"(.*)\"\ssrc', js['productsHtml'])
        ind1 = url.find('page=')
        ind2 = url.find('&sort=')
        curPage = int(url[ind1 + 5:ind2])
        print(curPage)
        print(js['totalPages'])
        if js['totalPages'] == 0:
            flag = 0
        if curPage != js['totalPages']:
            curPage += 1
            for j in ids:
                cur1[name].append('http://catalog.aquamarine.kz/catalog/item.ashx?id=' + j)
        else:
            flag = 0

with open('Aqumarine_types.json', 'w') as out:
    json.dump(cur1, out)

types = sel.css('table.selector td:contains(\'Цвет вставки\') div div label')
for i in types:
    name = i.css('::text').get()
    cur1[name] = []
    flag = 1
    curPage = '1'
    while flag != 0:
        print(name)
        curPage = str(curPage)
        url = 'http://catalog.aquamarine.kz/catalog/products.ashx?rnd=186262780&q=&spec=&mip=210&map=232010&mippg=960' \
              '&mappg=14270&miw=0.2&maw=137.74&miq=1&maq=411&miprcs=999999.999&maprcs=0&page=[INDEX]&sort=art-down&view=1&spc=1,&[TYPE],&brid=7,&_=1595153244242 '
        type = i.css('::attr(for)').get()
        type = type.replace('-', '=')
        url = url.replace('[TYPE]', type)
        url = url.replace('[INDEX]', curPage)
        req = requests.get(url, headers=headers)
        con = req.text
        js = json.loads(con)
        ids = re.findall(r'data-pid=\"(.*)\"\ssrc', js['productsHtml'])
        ind1 = url.find('page=')
        ind2 = url.find('&sort=')
        curPage = int(url[ind1 + 5:ind2])
        print(curPage)
        print(js['totalPages'])
        if js['totalPages'] == 0:
            flag = 0
        if curPage != js['totalPages']:
            curPage += 1
            for j in ids:
                cur1[name].append('http://catalog.aquamarine.kz/catalog/item.ashx?id=' + j)
        else:
            flag = 0

with open('Aqumarine_types.json', 'w') as out:
    json.dump(cur1, out)

types = sel.css('table.selector td:contains(\'Коллекция\') div div label')
for i in types:
    name = i.css('::text').get()
    cur1[name] = []
    flag = 1
    curPage = '1'
    while flag != 0:
        print(name)
        curPage = str(curPage)
        url = 'http://catalog.aquamarine.kz/catalog/products.ashx?rnd=186262780&q=&spec=&mip=210&map=232010&mippg=960' \
              '&mappg=14270&miw=0.2&maw=137.74&miq=1&maq=411&miprcs=999999.999&maprcs=0&page=[INDEX]&sort=art-down&view=1&spc' \
              '=1,&[TYPE],&brid=7,&_=1595153244242 '
        type = i.css('::attr(for)').get()
        type = type.replace('-', '=')
        url = url.replace('[TYPE]', type)
        url = url.replace('[INDEX]', curPage)
        req = requests.get(url, headers=headers)
        con = req.text
        js = json.loads(con)
        ids = re.findall(r'data-pid=\"(.*)\"\ssrc', js['productsHtml'])
        ind1 = url.find('page=')
        ind2 = url.find('&sort=')
        curPage = int(url[ind1 + 5:ind2])
        print(curPage)
        print(js['totalPages'])
        if js['totalPages'] == 0:
            flag = 0
        if curPage != js['totalPages']:
            curPage += 1
            for j in ids:
                cur1[name].append('http://catalog.aquamarine.kz/catalog/item.ashx?id=' + j)
        else:
            flag = 0

with open('Aqumarine_types.json', 'w') as out:
    json.dump(cur1, out)

types = sel.css('table.selector td:contains(\'Размер\') div div label')
for i in types:
    name = i.css('::text').get()
    cur1[name] = []
    flag = 1
    curPage = '1'
    while flag != 0:
        print(name)
        curPage = str(curPage)
        url = 'http://catalog.aquamarine.kz/catalog/products.ashx?rnd=186262780&q=&spec=&mip=210&map=232010&mippg=960' \
              '&mappg=14270&miw=0.2&maw=137.74&miq=1&maq=411&miprcs=999999.999&maprcs=0&page=[INDEX]&sort=art-down&view=1&spc' \
              '=1,&[TYPE],&brid=7,&_=1595153244242 '
        type = i.css('::attr(for)').get()
        type = type.replace('-', '=')
        url = url.replace('[TYPE]', type)
        url = url.replace('[INDEX]', curPage)
        req = requests.get(url, headers=headers)
        con = req.text
        js = json.loads(con)
        ids = re.findall(r'data-pid=\"(.*)\"\ssrc', js['productsHtml'])
        ind1 = url.find('page=')
        ind2 = url.find('&sort=')
        curPage = int(url[ind1 + 5:ind2])
        print(curPage)
        print(js['totalPages'])
        if js['totalPages'] == 0:
            flag = 0
        if curPage != js['totalPages']:
            curPage += 1
            for j in ids:
                cur1[name].append('http://catalog.aquamarine.kz/catalog/item.ashx?id=' + j)
        else:
            flag = 0

name = 'Без покрытия'
cur1[name] = []
flag = 1
curPage = '1'
while flag != 0:
    print(name)
    curPage = str(curPage)
    url = 'http://catalog.aquamarine.kz/catalog/products.ashx?rnd=489759904&q=&spec=&mip=210&map=232010&mippg=960' \
          '&mappg=14270&miw=0.2&maw=137.74&miq=1&maq=411&miprcs=999999.999&maprcs=0&page=[INDEX]&sort=art-down&view=1&spc' \
          '=1,&mfid=0,&brid=7,&_=1595269042446 '
    url = url.replace('[INDEX]', curPage)
    req = requests.get(url, headers=headers)
    con = req.text
    js = json.loads(con)
    ids = re.findall(r'data-pid=\"(.*)\"\ssrc', js['productsHtml'])
    ind1 = url.find('page=')
    ind2 = url.find('&sort=')
    curPage = int(url[ind1 + 5:ind2])
    print(curPage)
    print(js['totalPages'])
    if js['totalPages'] == 0:
        flag = 0
    if curPage != js['totalPages']:
        curPage += 1
        for j in ids:
            cur1[name].append('http://catalog.aquamarine.kz/catalog/item.ashx?id=' + j)
    else:
        flag = 0

name = 'Позолота'
cur1[name] = []
flag = 1
curPage = '1'
while flag != 0:
    print(name)
    curPage = str(curPage)
    url = 'http://catalog.aquamarine.kz/catalog/products.ashx?rnd=833710831&q=&spec=&mip=210&map=232010&mippg=960' \
          '&mappg=14270&miw=0.2&maw=137.74&miq=1&maq=411&miprcs=999999.999&maprcs=0&page=[INDEX]&sort=art-down&view=1&spc' \
          '=1,&mfid=1,&brid=7,&_=1595269042447 '
    url = url.replace('[INDEX]', curPage)
    req = requests.get(url, headers=headers)
    con = req.text
    js = json.loads(con)
    ids = re.findall(r'data-pid=\"(.*)\"\ssrc', js['productsHtml'])
    ind1 = url.find('page=')
    ind2 = url.find('&sort=')
    curPage = int(url[ind1 + 5:ind2])
    print(curPage)
    print(js['totalPages'])
    if js['totalPages'] == 0:
        flag = 0
    if curPage != js['totalPages']:
        curPage += 1
        for j in ids:
            cur1[name].append('http://catalog.aquamarine.kz/catalog/item.ashx?id=' + j)
    else:
        flag = 0

name = 'Родаж'
cur1[name] = []
flag = 1
curPage = '1'
while flag != 0:
    print(name)
    curPage = str(curPage)
    url = 'http://catalog.aquamarine.kz/catalog/products.ashx?rnd=25888674&q=&spec=&mip=210&map=232010&mippg=960' \
          '&mappg=14270&miw=0.2&maw=137.74&miq=1&maq=411&miprcs=999999.999&maprcs=0&page=[INDEX]&sort=art-down&view=1&spc' \
          '=1,&mfid=2,&brid=7,&_=1595269042448 '
    url = url.replace('[INDEX]', curPage)
    req = requests.get(url, headers=headers)
    con = req.text
    js = json.loads(con)
    ids = re.findall(r'data-pid=\"(.*)\"\ssrc', js['productsHtml'])
    ind1 = url.find('page=')
    ind2 = url.find('&sort=')
    curPage = int(url[ind1 + 5:ind2])
    print(curPage)
    print(js['totalPages'])
    if js['totalPages'] == 0:
        flag = 0
    if curPage != js['totalPages']:
        curPage += 1
        for j in ids:
            cur1[name].append('http://catalog.aquamarine.kz/catalog/item.ashx?id=' + j)
    else:
        flag = 0

types = sel.css('table.selector td:contains(\'Вид изделия\') div div label[for*=\'cid\']')
d = {}
for i in types:
    curName = i.css('::text').get()
    curInd = i.css('::attr(for)').get().split('-')[1]
    d[curName] = curInd
types = sel.css('table.selector td:contains(\'Вид изделия\') div div label[for*=\'cgrs\']')
d1 = {}
for i in types:
    curName = i.css('::text').get()
    curInd = i.css('::attr(for)').get().split('cgrs-')[1]
    ind = curInd.split('-')[0]
    for k, v in d.items():
        if v == ind:
            d1[d[k] + ',' + curInd] = curName
d1['27'] = 'Подкова-сувенир'
d1['39'] = 'Сувенир'
d1['6'] = 'Цепь'
print(d1)
for k, v in d1.items():
    cur1[v] = []
    flag = 1
    curPage = '1'
    while flag != 0:
        print(v)
        curPage = str(curPage)
        url = 'http://catalog.aquamarine.kz/catalog/products.ashx?rnd=186262780&q=&spec=&mip=210&map=232010&mippg=960' \
              '&mappg=14270&miw=0.2&maw=137.74&miq=1&maq=411&miprcs=999999.999&maprcs=0&page=[INDEX]&sort=art-down&view=1&spc' \
              '=1,&cid=[TYPE],&brid=7,&_=1595153244242 '
        url = url.replace('[TYPE]', k)
        url = url.replace('[INDEX]', curPage)
        req = requests.get(url, headers=headers)
        con = req.text
        js = json.loads(con)
        ids = re.findall(r'data-pid=\"(.*)\"\ssrc', js['productsHtml'])
        ind1 = url.find('page=')
        ind2 = url.find('&sort=')
        curPage = int(url[ind1 + 5:ind2])
        print(curPage)
        print(js['totalPages'])
        if js['totalPages'] == 0:
            flag = 0
        if curPage != js['totalPages']:
            curPage += 1
            for j in ids:
                cur1[v].append('http://catalog.aquamarine.kz/catalog/item.ashx?id=' + j)
        else:
            flag = 0

with open('Aqumarine_types.json', 'w') as out:
    json.dump(cur1, out)
