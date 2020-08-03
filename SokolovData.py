import json
import pandas as pd
import scrapy
import requests
from test import dictPhotos
import re

with open('SokolovOpt.json') as in1:
    opt = json.load(in1)

with open('SokolovRozn.json') as in2:
    rozn = json.load(in2)

headers = ['Код_товара', 'Название_позиции', 'Поисковые_запросы', 'Описание', 'Тип_товара', 'Цена', 'Валюта',
           'Единица_измерения', 'Количество', 'Количество в России', 'Ссылка_изображения', 'Наличие', 'Скидка',
           'Производитель', 'Страна_производитель', 'Название_группы', 'Идентификатор_группы',
           'Уникальный_идентификатор', 'Идентификатор_товара', 'Ярлык',
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Нурсултан
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Алматы(1)
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Алматы(2)
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Россия
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Товарная категория
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Проба
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Вставка/камень
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Покрытие
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Тематика
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Цвет
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Виды замков
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Вес
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Коллекция
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Высота
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Длина
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Ширина
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Длина швензы
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Для кого
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Вид изделия
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Диаметр
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Макс. длина цепи
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Длина овсинки
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           # Высота подвесного элемента
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           # Длина подвесного элемента
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           # Ширина подвесного элемента
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Мин. ширина шинки
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Ширинашинки ТД
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Посадка ТД
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Зодиак ТД
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Ширина овсинки
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Высота овсинки
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Вид плетения ТД
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Толщина проволоки ТД
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           # Длина декоративного элемента
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           # Ширина декоративного элемента
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           # Длина декоративной части
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           # Ширина декоративной части
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           # Длина булавки
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           # Высота чаши
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           # Объём чаши
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           # Длина ручки
           'Видео'
           ]


def koef():
    req = requests.get('https://kazfin.info/exchange/rur/#buy')
    sel = scrapy.Selector(req)
    num = sel.css('div.col-xs-4 a small + span::text').get()
    num = float(num)
    return num


final = []
# num = koef()
num = 6
for item in opt:
    l = []
    type = ''
    l.append(item['id'])
    description_cur = ''
    videos = []
    for i in rozn:
        video = ''
        if item['id'] == i['id'] and len(i['outside']) != 0:
            material = i['outside']
        if item['id'] == i['id'] and 'Новинка                                                                    ' in i[
            'badges']:
            type = 'Новинка'  # [19] = 'Новинка'
        if item['id'] == i['id']:
            forWho = i['forWho']
            if i['video'] != None:
                video = i['video']
                videos.append(video)
                '''description_cur = <div class="b-user-content">
                <div>
                <div class="ck-image-text-right ck-image-text-right_type_lite ck-theme-grey">
                <div class="ck-image-text-right__image-wrapper"><a href="video_link"><img alt="" class="ck-image-text-right__image" src="image_link" style="width: 58px; height: 57px;" /></a></div>

                <div class="ck-image-text-right__text">
                <div class="ck-image-text-right__title" style="margin-left: 40px;"><span style="font-size:14px;"><a href="video_link" target="_blank">Смотреть видео товара</a></span><span style="font-size:14px;"></span></div>
                </div>
                </div>
                            
                description_cur = description_cur.replace('video_link', i['video'])
                description_cur = description_cur.replace('image_link', item['attributes']['photo'])'''
                description_cur = ''
            else:
                videos.append(video)
            try:
                typeOfProduct = i['group'][2]
            except:
                pass

    if description_cur == '':
        description11 = '''<div class="b-user-content" data-qaid="product_description"> 
                            <div> 
                             </div> <p> </p> 
    
                             '''
        description = description11.replace('name_id', item['id'])
    else:
        description = description_cur
    if len(item['attributes']['complect-products']) != 0:
        for n in item['attributes']['complect-products']:
            if n in dictPhotos.keys():
                description += '\n' + dictPhotos[n]

        l.append(item['attributes']['title'] + ' - есть комплект')
    else:
        l.append(item['attributes']['title'])

    for n in item['attributes']['model-products']:
        if n in dictPhotos.keys():
            description += '\n' + dictPhotos[n].replace('Комплект', 'Аналог')

    l.append('')  # Поисковые_запросы
    l.append(description)  # Описание
    l.append('r')  # Тип_товара
    price = item['attributes']['trade-price-without-sale']
    sale_price = item['attributes']['trade-price']
    sale = ''
    if price is not None:
        sale = ((sale_price / price) * 100 - 1) // 1
        l.append(round(float(price) * 3 * num * 1.04, 2))  # Цена
    elif sale_price is not None:
        l.append(round(float(sale_price) * 3 * num * 1.04, 2))
    else:
        l.append('')
    l.append('KZT')  # Валюта
    l.append('шт.')  # Единица_измерения
    sizes = []
    number = 0
    ifExist = '-'
    countInRussia = ''
    if item['attributes']['has-sizes']:
        for j in item['attributes']['sizes']:
            if j['balance']['hint'] == 'Небольшое количество':
                number += 1
                sizes.append(j['size'])
            elif j['balance']['hint'] == 'Достаточное количество':
                number += 3
                sizes.append(j['size'])
            elif j['balance']['hint'] == 'Много на складах':
                number += 10
                sizes.append(j['size'])
        ifExist = '+'

    if item['attributes']['balance']['hint'] == 'Небольшое количество':
        number += 1
        countInRussia = 'Небольшое количество'
        ifExist = '+'
    elif item['attributes']['balance']['hint'] == 'Достаточное количество':
        number += 3
        countInRussia = 'Достаточное количество'
        ifExist = '+'
    elif item['attributes']['balance']['hint'] == 'Много на складах':
        number += 10
        countInRussia = 'Много на складах'
        ifExist = '+'
    elif item['attributes']['balance']['hint'] == 'Нет на складах':
        countInRussia = 'Нет на складах'
        ifExist = '-'
    l.append(number)  # Количество
    l.append(countInRussia)  # Количество в России
    photos = []
    if len(item['attributes']['photos']) > 0:
        photos = item['attributes']['photos']
    if item['attributes']['photo'] is not None:
        photos.append(item['attributes']['photo'])
    ph = ','
    ph = ph.join(photos[::-1])
    l.append(ph)  # Фотографии
    l.append(ifExist)  # Наличие
    if sale != '':
        sale = 100 * (1 - sale_price / (price * 2))
        # print(sale)
        l.append(str(int(sale)) + '%')  # Скидка
        badge = 'Распродажа'
    else:
        badge = ''
        l.append('50%')
    l.append('SOKOLOV')  # Производитель
    l.append('Россия')  # Страна производитель
    l.append(item['attributes']['category'])  # Название группы
    l.append('')  # Идентификатор группы
    l.append('')  # Уникальный_идентификатор
    l.append('')  # Идентификатор_товара
    l.append(badge)  # Ярлык
    l.append('Наличие, размеры в Нурсултане')  # Наличие, размеры в Нурсултане
    l.append('')  # default
    l.append('Нет')  # yes/no
    l.append('Наличие, размеры в Алматы (склад 1)')  # Наличие, размеры в Алматы (склад 1)
    l.append('')  # default
    l.append('Нет')  # yes/no
    l.append('Наличие, размеры в Алматы (склад 2)')  # Наличие, размеры в Алматы (склад 2)
    l.append('')  # default
    l.append('Нет')  # yes/no
    l.append('Наличие, размеры в России')  # Наличие, размеры в России
    l.append('')  # default
    if len(sizes) != 0:
        size = '|'
        size = size.join(sizes)
        l.append(size)
    elif ifExist == '+':
        l.append('Да')  # yes/no
    else:
        l.append('Нет')
    l.append('')  # Товарная категория
    l.append('')
    if len(item['attributes']['inserts']) != 0:
        vstavka = []
        for j in item['attributes']['inserts']:
            if j['type'] not in vstavka:
                vstavka.append(j['type'])
        vstavka = '|'.join(vstavka)
        l.append(vstavka)
    else:
        l.append('Без вставок')

    l.append('Проба')  # Проба
    l.append('')
    l.append(item['attributes']['material'] + ' ' + item['attributes']['probe'])

    l.append('Вставка/камень')  # Вставка
    l.append('')
    l.append('Без вставок')
    stone = []
    for i in item['attributes']['inserts']:
        stone.append(i['name'])
    if len(stone) != 0:
        stone = '|'.join(set(stone))
        l[-1] = stone
    material = []
    forWho = ''
    typeOfProduct = ''
    if item['attributes']['material-plating'] is not None:
        if item['attributes']['material-plating'] == 'Родаж':
            material.append('Родирование')
        else:
            material.append(item['attributes']['material-plating'])
    if len(material) != 0:
        l.append('Покрытие')  # Покрытие
        l.append('')
        material = [j.replace(',', '') for j in material]
        materials = '|'.join(set(material))
        l.append(materials)
    else:
        l.append('')
        l.append('')
        l.append('')

    l.append('')  # Тематика
    l.append('')
    l.append('')

    l.append('')  # Цвет
    l.append('')
    l.append('')

    l.append('')  # Виды замков
    l.append('')
    l.append('')

    l.append('Вес')  # Вес
    l.append('')
    l.append(item['attributes']['total-weight'])

    collect = []
    if len(item['attributes']['collections']) != 0:
        l.append('Коллекция')
        l.append('')
        for i in item['attributes']['collections']:
            collect.append(i['collection']['title'])
        collect = '|'.join(collect)
        l.append(collect)
    else:
        l.append('')  # Коллекция
        l.append('')
        l.append('')

    l.append('')  # Высота
    l.append('')
    l.append('')

    l.append('')  # Длина
    l.append('')
    l.append('')

    l.append('')  # Ширина
    l.append('')
    l.append('')

    l.append('')  # Длина швензы
    l.append('')
    l.append('')

    diametr = ''
    maxLenght = ''
    lengthPodv = ''
    widthPodv = ''
    heightPodv = ''
    lengthOvs = ''
    widthOvs = ''
    shinka = ''
    heightOvs = ''
    lengthArm = ''
    Vcup = ''
    Hcup = ''
    lengthBul = ''
    lengthDecPart = ''
    widthDecPart = ''
    lengthDecEl = ''
    widthDecEl = ''
    if item['attributes']['props'] is not None:
        for i in item['attributes']['props']['proportions']:
            if i['name'] == 'Высота':
                l[-12] = i['name']
                l[-10] = i['value']
            elif i['name'] == 'Длина':
                l[-9] = i['name']
                l[-7] = i['value']
            elif i['name'] == 'Ширина':
                l[-6] = i['name']
                l[-4] = i['value']
            elif i['name'] == 'Длина швензы':
                l[-3] = i['name']
                l[-1] = i['value']
            elif i['name'] == 'Диаметр':
                diametr = i['value']
            elif i['name'] == 'Макс. длина цепи':
                maxLenght = i['value']
            elif i['name'] == 'Длина подвесного элемента':
                lengthPodv = i['value']
            elif i['name'] == 'Высота подвесного элемента':
                heightPodv = i['value']
            elif i['name'] == 'Ширина подвесного элемента':
                widthPodv = i['value']
            elif i['name'] == 'Длина овсинки':
                lengthOvs = i['value']
            elif i['name'] == 'Ширина овсинки':
                widthOvs = i['value']
            elif i['name'] == 'Мин. ширина шинки':
                shinka = i['value']
            elif i['name'] == 'Высота овсинки':
                heightOvs = i['value']
            elif i['name'] == 'Длина ручки':
                lengthArm = i['value']
            elif i['name'] == 'Объём чаши':
                Vcup = i['value']
            elif i['name'] == 'Высота чаши':
                Hcup = i['value']
            elif i['name'] == 'Длина булавки':
                lengthBul = i['value']
            elif i['name'] == 'Длина декоративной части':
                lengthDecPart = i['value']
            elif i['name'] == 'Ширина декоративной части':
                widthDecPart = i['value']
            elif i['name'] == 'Длина декоративного элемента':
                lengthDecEl = i['value']
            elif i['name'] == 'Ширина декоративного элемента':
                widthDecEl = i['value']

    if forWho:
        l.append('Для кого')  # Для кого
        l.append('')
        l.append(forWho.strip())
    else:
        l.append('')  # Для кого
        l.append('')
        l.append('')

    if typeOfProduct != '':
        l.append('Вид изделия')  # Вид изделия
        l.append('')
        l.append(typeOfProduct)
    else:
        l.append('')
        l.append('')
        l.append('')

    if diametr != '':
        l.append('Диаметр')  # Диаметр
        l.append('')
        l.append(diametr)
    else:
        l.append('')
        l.append('')
        l.append('')

    if maxLenght != '':
        l.append('Макс. длина цепи')  # Макс. длина цепи
        l.append('')
        l.append(maxLenght)
    else:
        l.append('')
        l.append('')
        l.append('')

    if lengthOvs != '':
        l.append('Длина овсинки')  # Длина овсинки
        l.append('')
        l.append(lengthOvs)
    else:
        l.append('')
        l.append('')
        l.append('')

    if heightPodv != '':
        l.append('Высота подвесного элемента')  # Высота подвесного элемента
        l.append('')
        l.append(heightPodv)
    else:
        l.append('')
        l.append('')
        l.append('')

    if lengthPodv != '':
        l.append('Длина подвесного элемента')  # Длина подвесного элемента
        l.append('')
        l.append(lengthPodv)
    else:
        l.append('')
        l.append('')
        l.append('')

    if widthPodv != '':
        l.append('Ширина подвесного элемента')  # Ширина подвесного элемента
        l.append('')
        l.append(widthPodv)
    else:
        l.append('')
        l.append('')
        l.append('')

    if shinka != '':
        l.append('Мин. ширина шинки')  # Мин. ширина шинки
        l.append('')
        l.append(shinka)
    else:
        l.append('')
        l.append('')
        l.append('')

    l.append('')  # Ширина Шинки ТД
    l.append('')
    l.append('')

    l.append('')  # Посадка ТД
    l.append('')
    l.append('')

    l.append('')  # Зодиак ТД
    l.append('')
    l.append('')

    if widthOvs != '':
        l.append('Ширина овсинки')  # Ширина овсинки
        l.append('')
        l.append(widthOvs)
    else:
        l.append('')
        l.append('')
        l.append('')

    if heightOvs != '':
        l.append('Высота овсинки')  # Высота овсинки
        l.append('')
        l.append(heightOvs)
    else:
        l.append('')
        l.append('')
        l.append('')

    l.append('')  # Вид плетения
    l.append('')
    l.append('')

    l.append('')  # Толщина проволоки
    l.append('')
    l.append('')

    if lengthDecEl != '':
        l.append('Длина декоративного элемента')  # Длина декоративного элемента
        l.append('')
        l.append(lengthDecEl)
    else:
        l.append('')
        l.append('')
        l.append('')

    if widthDecEl != '':
        l.append('Ширина декоративного элемента')  # Ширина декоративного элемента
        l.append('')
        l.append(widthDecEl)
    else:
        l.append('')
        l.append('')
        l.append('')

    if lengthDecPart != '':
        l.append('Длина декоративной части')  # Длина декоративной части
        l.append('')
        l.append(lengthDecPart)
    else:
        l.append('')
        l.append('')
        l.append('')

    if widthDecPart != '':
        l.append('Ширина декоративной части')  # Ширина декоративной части
        l.append('')
        l.append(widthDecPart)
    else:
        l.append('')
        l.append('')
        l.append('')

    if lengthBul != '':
        l.append('Длина булавки')  # Длина булавки
        l.append('')
        l.append(lengthBul)
    else:
        l.append('')
        l.append('')
        l.append('')

    if Hcup != '':
        l.append('Объём чаши')  # Высота чаши
        l.append('')
        l.append(Hcup)
    else:
        l.append('')
        l.append('')
        l.append('')

    if Vcup != '':
        l.append('Объём чаши')  # Объём чаши
        l.append('')
        l.append(Vcup)
    else:
        l.append('')
        l.append('')
        l.append('')

    if lengthArm != '':
        l.append('Длина ручки')  # Длина ручки
        l.append('')
        l.append(lengthArm)
    else:
        l.append('')
        l.append('')
        l.append('')
    l[19] = type
    print(videos)
    try:
        l.append(videos[0])
    except:
        l.append('')
    # print(len(l))
    final.append(l)

df = pd.DataFrame(final, columns=headers)
df.to_excel('SokolovData.xls', index=False)
