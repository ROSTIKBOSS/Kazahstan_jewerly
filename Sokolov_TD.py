import pandas as pd
import json
import xlsxwriter
import xlrd
from bs4 import BeautifulSoup
import re
import math
from test import dictTDPhotos


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


satu = pd.read_excel('Data.xls')
sokolovIds = satu['Код_товара'].tolist()
satuIds = satu['Уникальный_идентификатор'].tolist()

mainData = pd.read_excel('Sokolov+TD.xlsx')
mainId = mainData['Код_товара'].tolist()

dictionary = dict(zip(sokolovIds, satuIds))
finalDict = {}

for i in mainId:
    if i not in dictionary.keys():
        finalDict[i] = 0
    else:
        finalDict[i] = dictionary[i]

# print(finalDict)

childrenLinks = pd.read_excel('TD_children_links.xls')
childrenLinks = list(set(childrenLinks[0].tolist()))

insertsLinks = pd.read_excel('TD_with_inserts_links.xls')
insertsLinks = list(set(insertsLinks[0].tolist()))

coloredLinks = pd.read_excel('TD_colored_stones_links.xls')
coloredLinks = list(set(coloredLinks[0].tolist()))

withoutInsertsLinks = pd.read_excel('TD_without_inserts_links.xls')
withoutInsertsLinks = list(set(withoutInsertsLinks[0].tolist()))

emalLinks = pd.read_excel('TD_emal_links.xls')
emalLinks = list(set(emalLinks[0].tolist()))

keramikaLinks = pd.read_excel('TD_keramika_links.xls')
keramikaLinks = list(set(keramikaLinks[0].tolist()))

with open('TD.json') as in1:
    TD = json.load(in1)

final = []
TDIds = []
mainCol = []
for item in TD:
    TDFinal = {
        'id': '',

    }
    cur_child = item['url'].replace('product', 'product_modal')
    cur_child = cur_child.replace('http', 'https')
    categories = []
    if str(cur_child) in childrenLinks:
        categories.append('Детская')
    if str(cur_child) in insertsLinks:
        categories.append('Со вставкой')
    if str(cur_child) in coloredLinks:
        categories.append('Цветные камни')
    if str(cur_child) in withoutInsertsLinks:
        categories.append('Без вставки')
    if str(cur_child) in emalLinks:
        categories.append('Эмаль')
    if str(cur_child) in keramikaLinks:
        categories.append('Керамика')
    cat = '|'.join(categories)
    TDFinal['childrenFlag'] = cat
    ind1 = str(item['name']).find('(')
    ind2 = str(item['name']).find(')')
    idTD = item['name'][ind1 + 1:ind2]
    ind3 = item['url'].find('product/')
    TDFinal['id'] = idTD
    TDFinal['idTd'] = item['url'][ind3 + 8:]
    if len(idTD) == 0:
        TDFinal['id'] = TDFinal['idTd']
        TDFinal['name'] = item['name'][:ind1]
    else:
        TDFinal['name'] = item['name'][:ind1]
    sizesALM = []
    colALM = []
    prices = []
    weight = ''
    for i in item['dataALM']:
        stt = cleanhtml(str(i)).strip()
        w1 = stt.find('Вес:')
        w2 = stt.find('гр.')
        weight = stt[w1 + 5:w2].strip()
        soup = BeautifulSoup(i, features="lxml")
        size = soup.select('div.col-xs-7')
        size = size[0].text.strip()
        if size != '' and size not in sizesALM:
            sizesALM.append(size.split()[0])
        col = soup.select('div.col-xs-5')
        col = col[0].text.strip()
        colALM.append(col.split()[0])
        price = soup.select('span.price_sku_from')
        price = price[0].text.strip()
        indKZT = price.find('KZT')
        indOt = price.find('от')
        if indOt != -1:
            price = price[indOt + 3:indKZT]
        else:
            price = price[:indKZT]
        price = price.replace(' ', '')
        prices.append(price)
    TDFinal['weight'] = weight
    TDFinal['priceALM'] = prices
    TDFinal['sizesALM'] = sizesALM
    TDFinal['colALM'] = colALM
    theme = ''
    if item['themeALM'] is not None:
        theme = item['themeALM'].split(':')[1].strip()
    if item['themeAST'] is not None:
        theme = item['themeAST'].split(':')[1].strip()
    TDFinal['theme'] = theme

    color = ''
    if item['colorALM'] is not None:
        color = item['colorALM'].split(':')[1].strip()
    if item['colorAST'] is not None:
        color = item['colorAST'].split(':')[1].strip()
    TDFinal['color'] = color

    typeLock = ''
    if item['typeLockALM'] is not None:
        typeLock = item['typeLockALM'].split(':')[1].strip()
    if item['typeLockAST'] is not None:
        typeLock = item['typeLockAST'].split(':')[1].strip()
    TDFinal['typeLock'] = typeLock

    sizesAST = []
    colAST = []
    prices = []
    for i in item['dataAST']:
        try:
            soup = BeautifulSoup(i, features="lxml")
            size = soup.select('div.col-xs-7')
            size = size[0].text.strip()
            if size != '' and size not in sizesAST:
                sizesAST.append(size.split()[0])
            col = soup.select('div.col-xs-5')
            col = col[0].text.strip()
            colAST.append(col.split()[0])
            price = soup.select('span.price_sku_from')
            price = price[0].text.strip()
            indKZT = price.find('KZT')
            indOt = price.find('от')
            if indOt != -1:
                price = price[indOt + 3:indKZT]
            else:
                price = price[:indKZT]
            price = price.replace(' ', '')
            prices.append(price)
        except:
            pass
    ph = []
    if len(item['photos']) > 1:
        ph.append(item['photos'][0])
        for i in item['photos'][1:]:
            ph.append('https://tdserebro.ru' + i)
    else:
        ph = item['photos']
    TDFinal['priceAST'] = prices
    TDFinal['sizesAST'] = sizesAST
    TDFinal['colAST'] = colAST
    ph = ','.join(ph)
    TDFinal['photos'] = ph
    TDFinal['brand'] = item['brand']
    if item['probeALM'] is not None:
        TDFinal['proba'] = item['probeALM'].split(':')[1]
    elif item['probeAST'] is not None:
        TDFinal['proba'] = item['probeAST'].split(':')[1]
    else:
        TDFinal['proba'] = ''

    if item['insertALM'] is not None:
        TDFinal['insert'] = item['insertALM'].split(':')[1]
    elif item['insertAST'] is not None:
        TDFinal['insert'] = item['insertAST'].split(':')[1]
    else:
        TDFinal['insert'] = ''

    if item['outsideALM'] is not None:
        TDFinal['outside'] = item['outsideALM'].split(':')[1]
    elif item['outsideAST'] is not None:
        TDFinal['outside'] = item['outsideAST'].split(':')[1]
    else:
        TDFinal['outside'] = ''

    if item['zodiakAST'] is not None:
        TDFinal['zodiak'] = item['zodiakAST'].split(':')[1]
    elif item['zodiakALM'] is not None:
        TDFinal['zodiak'] = item['zodiakALM'].split(':')[1]
    else:
        TDFinal['zodiak'] = ''

    if item['posadkaAST'] is not None:
        TDFinal['posadka'] = item['posadkaAST'].split(':')[1]
    elif item['posadkaALM'] is not None:
        TDFinal['posadka'] = item['posadkaALM'].split(':')[1]
    else:
        TDFinal['posadka'] = ''

    if item['shinkaAST'] is not None:
        TDFinal['shinka'] = item['shinkaAST'].split(':')[1]
    elif item['shinkaALM'] is not None:
        TDFinal['shinka'] = item['shinkaALM'].split(':')[1]
    else:
        TDFinal['shinka'] = ''

    if item['typePletAST'] is not None:
        TDFinal['typePlet'] = item['typePletAST'].split(':')[1]
    elif item['typePletALM'] is not None:
        TDFinal['typePlet'] = item['typePletALM'].split(':')[1]
    else:
        TDFinal['typePlet'] = ''
    TDFinal['complect_item'] = []
    TDFinal['complect'] = ''
    if len(item['collect']) > 0:
        for b in item['collect']:
            b = b.replace('/almaty/product/', '')
            ind1 = b.index('?prev_product=')
            TDFinal['complect_item'].append(b[:ind1])
        TDFinal['complect'] = 'есть комплект'

    TDFinal['badge'] = ''
    if item['badges'] is not None:
        soup = BeautifulSoup(item['badges'], features="lxml")
        badge = soup.select('div.marker_hit')
        if len(badge) != 0:
            TDFinal['badge'] = badge[0].text.strip()

    if item['name'] != '502 Bad Gateway':
        TDIds.append(TDFinal['id'])
        TDFinal['groupName'] = item['groupName'][2]
        final.append(TDFinal)
    else:
        print('yes')

sokolov = pd.read_excel('SokolovData.xls')
sokolovData = sokolov.values.tolist()
sokolovIds = sokolov['Код_товара'].tolist()

headers = ['Код_товара', 'Название_позиции', 'Поисковые_запросы', 'Описание', 'Тип_товара', 'Цена', 'Валюта',
           'Единица_измерения', 'Количество', 'Товарная категория', 'Ссылка_изображения', 'Наличие', 'Скидка',
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
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # ШиринаШинки ТД
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Посадка ТД4
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Зодиак ТД
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',  # Ширина овсинки
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           'Название_Характеристики', 'Измерение_Характеристики', 'Значение_Характеристики',
           'Видео',
           ]

workbook = xlsxwriter.Workbook('Sokolov+TD.xlsx', {'strings_to_urls': False})
worksheet = workbook.add_worksheet()

worksheet.write_row(0, 0, headers)
count = 0
controlId = []

for i in range(len(sokolovIds)):
    if sokolovIds[i] not in TDIds:  # чистый соколов
        count += 1
        for j in range(len(sokolovData[i])):
            try:
                if j == 17 and sokolovData[i][0] in finalDict.keys():
                    worksheet.write(count, j, finalDict[sokolovData[i][0]])
                elif j == 17:
                    worksheet.write(count, j, 0)
                elif j == 9:
                    worksheet.write(count, j, '')
                elif j == 1:
                    allSizes = []
                    size1 = sokolovData[i][j + 21]
                    size2 = sokolovData[i][j + 24]
                    size3 = sokolovData[i][j + 27]
                    size4 = sokolovData[i][j + 30]
                    if 'Нет' not in size1 and 'Да' not in size1:
                        temp = size1.split('|')
                        for t in temp:
                            allSizes.append(t)
                    if 'Нет' not in size2 and 'Да' not in size2:
                        temp = size2.split('|')
                        for t in temp:
                            allSizes.append(t)
                    if 'Нет' not in size3 and 'Да' not in size3:
                        temp = size3.split('|')
                        for t in temp:
                            allSizes.append(t)
                    if 'Нет' not in size4 and 'Да' not in size4:
                        temp = size4.split('|')
                        for t in temp:
                            allSizes.append(t)
                    if len(allSizes) != 0:
                        allSizes = list(dict.fromkeys(allSizes))
                        sss = ' '.join(allSizes)
                        if '- есть комплект' in sokolovData[i][j]:
                            name = re.sub('- есть комплект', '', sokolovData[i][j])
                            worksheet.write(count, j,
                                            name + ' ' + sokolovData[i][j + 12] + ' ' + sss + ' - есть комплект')
                        else:
                            worksheet.write(count, j,
                                            sokolovData[i][j] + ' ' + sokolovData[i][j + 12] + ' ' + sss)
                    else:
                        if '- есть комплект' in sokolovData[i][j]:
                            name = re.sub('- есть комплект', '', sokolovData[i][j])
                            worksheet.write(count, j,
                                            name + ' ' + sokolovData[i][j + 12] + ' - есть комплект')
                        else:
                            worksheet.write(count, j,
                                            sokolovData[i][j] + ' ' + sokolovData[i][j + 12])
                else:
                    worksheet.write(count, j, sokolovData[i][j])
            except:
                if j == 17 and sokolovData[i][0] in finalDict.keys():
                    worksheet.write(count, j, 0)
                elif j == 9:
                    worksheet.write(count, j, '')
                elif j == 17:
                    worksheet.write(count, j, 0)
                else:
                    worksheet.write(count, j, '')
        worksheet.write(count, 107, 'Количество в России')
        worksheet.write(count, 108, '')
        worksheet.write(count, 109, sokolovData[i][9])
        # worksheet.write(count, 110, 'Для детей')
        # worksheet.write(count, 111, '')
        worksheet.write(count, 9, '')
        mainCol.append(sokolovData[i][8])
        controlId.append(sokolovIds[i])
    else:  # пересечение соколова с тд
        count += 1
        ind1 = TDIds.index(sokolovIds[i])
        worksheet.write(count, 0, sokolovIds[i])
        allSizes = []
        if len(final[ind1]['sizesAST']) != 0:
            for size in final[ind1]['sizesAST']:
                allSizes.append(size)
            sizesAST = '|'.join(final[ind1]['sizesAST'])
            worksheet.write(count, 22, sizesAST)
        elif len(final[ind1]['colAST']) != 0:
            worksheet.write(count, 22, 'Да')
        else:
            worksheet.write(count, 22, sokolovData[i][22])

        worksheet.write(count, 23, sokolovData[i][23])
        worksheet.write(count, 24, '')
        if len(final[ind1]['sizesALM']) != 0:
            for size in final[ind1]['sizesALM']:
                if size not in allSizes:
                    allSizes.append(size)
            sizesALM = '|'.join(final[ind1]['sizesALM'])
            worksheet.write(count, 25, sizesALM)
        elif len(final[ind1]['colALM']) != 0:
            worksheet.write(count, 25, 'Да')
        else:
            worksheet.write(count, 25, sokolovData[i][22])
        if final[i]['complect'] != '':
            name = re.sub('- есть комплект', '',
                          sokolovData[i][1] + ' ' + sokolovData[i][13] + ' ' + ' '.join(allSizes))
            worksheet.write(count, 1, name + ' - есть комплект')
        else:
            worksheet.write(count, 1, sokolovData[i][1] + ' ' + sokolovData[i][13] + ' ' + ' '.join(allSizes))
        worksheet.write(count, 2, '')
        worksheet.write(count, 3, sokolovData[i][3])
        worksheet.write(count, 4, 'r')
        maxAST = 0
        maxALM = 0
        if len(final[ind1]['priceAST']) != 0:
            maxAST = max(final[ind1]['priceAST'])
        if len(final[ind1]['priceALM']) != 0:
            maxALM = max(final[ind1]['priceALM'])
        price = max(float(maxALM), float(maxAST))
        price *= 3
        price = math.ceil(price)
        worksheet.write(count, 5, price)  # Цена
        worksheet.write(count, 6, 'KZT')
        worksheet.write(count, 7, 'шт.')
        worksheet.write(count, 8, '')
        worksheet.write(count, 9, '')
        worksheet.write(count, 10, str(sokolovData[i][10]))
        worksheet.write(count, 11, '+')  # Наличие
        # worksheet.write(count, 12, str(sokolovData[i][12]))
        worksheet.write(count, 12, '50%')
        worksheet.write(count, 13, sokolovData[i][13])
        worksheet.write(count, 14, sokolovData[i][14])
        worksheet.write(count, 15, sokolovData[i][15])

        worksheet.write(count, 16, '')  # Идентификатор_группы (добавить)
        if sokolovIds[i] in finalDict.keys():
            worksheet.write(count, 17, finalDict[sokolovIds[i]])  # Уникальный_идентификатор
        # else:
        #    worksheet.write(count, 17, '')
        worksheet.write(count, 18, final[ind1]['idTd'])  # Идентификатор_товара
        try:
            worksheet.write(count, 19, sokolovData[i][19])  # Ярлык
        except:
            worksheet.write(count, 19, '')  # добавить с ТД

        worksheet.write(count, 20, sokolovData[i][20])
        worksheet.write(count, 21, '')
        colAST = [int(i) for i in final[ind1]['colAST']]
        colALM = [int(i) for i in final[ind1]['colALM']]
        s = sum(colAST) + sum(colALM) + sokolovData[i][8]
        worksheet.write(count, 8, s)
        mainCol.append(s)

        worksheet.write(count, 26, sokolovData[i][26])
        worksheet.write(count, 27, '')
        worksheet.write(count, 28, sokolovData[i][28])

        worksheet.write(count, 29, sokolovData[i][29])
        worksheet.write(count, 30, '')
        worksheet.write(count, 31, sokolovData[i][31])

        counter = 32
        for j in sokolovData[i][32:]:
            try:
                worksheet.write(count, counter, j)
            except:
                worksheet.write(count, counter, '')
            counter += 1
        if final[ind1]['theme'] != '':
            worksheet.write(count, 44, 'Тематика')
            worksheet.write(count, 45, '')
            worksheet.write(count, 46, final[ind1]['theme'])
        if final[ind1]['color'] != '':
            worksheet.write(count, 47, 'Цвет')
            worksheet.write(count, 48, '')
            worksheet.write(count, 49, final[ind1]['color'])
        if final[ind1]['typeLock'] != '':
            worksheet.write(count, 50, 'Виды замков')
            worksheet.write(count, 51, '')
            worksheet.write(count, 52, final[ind1]['typeLock'])

        if final[ind1]['shinka'] != '':
            worksheet.write(count, 98, 'ШиринаШинки')
            worksheet.write(count, 99, '')
            worksheet.write(count, 100, final[ind1]['shinka'])

        if final[ind1]['posadka'] != '':
            worksheet.write(count, 101, 'Посадка')
            worksheet.write(count, 102, '')
            worksheet.write(count, 103, final[ind1]['posadka'])

        if final[ind1]['zodiak'] != '':
            worksheet.write(count, 104, 'Зодиак')
            worksheet.write(count, 105, '')
            worksheet.write(count, 106, final[ind1]['zodiak'])
        worksheet.write(count, 107, 'Количество в России')
        worksheet.write(count, 108, '')
        worksheet.write(count, 109, sokolovData[i][9])
        # worksheet.write(count, 110, 'Для детей')
        # worksheet.write(count, 111, '')
        worksheet.write(count, 9, final[ind1]['childrenFlag'])
        if final[ind1]['typePlet'] != '':
            worksheet.write(count, 110, 'Вид плетения')
            worksheet.write(count, 111, '')
            worksheet.write(count, 112, final[ind1]['typePlet'])
        controlId.append(sokolovIds[i])
        # добавить больше характеристик с тд

for i in range(len(TDIds)):  # Чистый ТД
    if final[i]['id'] not in controlId:
        count += 1
        worksheet.write(count, 0, final[i]['id'])
        description11 = '''<div class="b-user-content" data-qaid="product_description"> 
                                <div> 
                                 </div> <p> </p> 

                                 '''
        descriptionTD = description11.replace('name_id', final[i]['id'])
        allSizes = []
        if len(final[i]['sizesAST']) > 0:
            for size in final[i]['sizesAST']:
                allSizes.append(size)
            sizesAST = '|'.join(final[i]['sizesAST'])
            worksheet.write(count, 22, sizesAST)
        elif len(final[i]['colAST']) > 0:
            worksheet.write(count, 22, 'Да')
        else:
            worksheet.write(count, 22, 'Нет')

        worksheet.write(count, 23, 'Наличие, размеры в Алматы (склад 1)')
        worksheet.write(count, 24, '')
        if len(final[i]['sizesALM']) > 0:
            for size in final[i]['sizesALM']:
                if size not in allSizes:
                    allSizes.append(size)
            sizesALM = '|'.join(final[i]['sizesALM'])
            worksheet.write(count, 25, sizesALM)
        elif len(final[i]['colALM']) > 0:
            worksheet.write(count, 25, 'Да')
        else:
            worksheet.write(count, 25, 'Нет')
        if final[i]['complect'] != '':
            for nn in final[i]['complect_item']:
                if nn in dictTDPhotos.keys():
                    descriptionTD += '\n' + dictTDPhotos[nn]
            worksheet.write(count, 1,
                            final[i]['name'] + ' ' + final[i]['brand'] + ' ' + ' '.join(allSizes) + ' - есть комплект')
        else:
            worksheet.write(count, 1, final[i]['name'] + ' ' + final[i]['brand'] + ' ' + ' '.join(allSizes))
        worksheet.write(count, 2, '')
        worksheet.write(count, 3, descriptionTD)
        worksheet.write(count, 4, 'r')
        maxAST = 0
        maxALM = 0
        if len(final[i]['priceAST']) != 0:
            maxAST = max(final[i]['priceAST'])
        if len(final[i]['priceALM']) != 0:
            maxALM = max(final[i]['priceALM'])
        price = max(float(maxALM), float(maxAST))
        price *= 3
        price = math.ceil(price)
        worksheet.write(count, 5, price)
        worksheet.write(count, 6, 'KZT')
        worksheet.write(count, 7, 'шт.')
        colAST = [int(i) for i in final[i]['colAST']]
        colALM = [int(i) for i in final[i]['colALM']]
        s = sum(colAST) + sum(colALM)
        worksheet.write(count, 8, s)
        mainCol.append(s)
        worksheet.write(count, 9, '')
        worksheet.write(count, 10, final[i]['photos'])
        worksheet.write(count, 11, '+')
        worksheet.write(count, 12, '50%')
        worksheet.write(count, 13, final[i]['brand'])
        worksheet.write(count, 14, 'Россия')
        worksheet.write(count, 15, final[i]['groupName'])
        worksheet.write(count, 16, '')  # идентификатор группы
        worksheet.write(count, 17, '')  # уникальный
        if final[i]['id'] in finalDict.keys():
            worksheet.write(count, 17, finalDict[final[i]['id']])  # Уникальный_идентификатор
        # else:
        #    worksheet.write(count, 17, '')
        worksheet.write(count, 18, final[i]['idTd'])
        worksheet.write(count, 19, final[i]['badge'])
        worksheet.write(count, 20, 'Наличие, размеры в Нурсултане')
        worksheet.write(count, 21, '')

        worksheet.write(count, 26, 'Наличие, размеры в Алматы (склад 2)')
        worksheet.write(count, 27, '')
        worksheet.write(count, 28, 'Нет')

        worksheet.write(count, 29, 'Наличие, размеры в России')
        worksheet.write(count, 30, '')
        worksheet.write(count, 31, 'Нет')

        worksheet.write(count, 32, '')
        worksheet.write(count, 33, '')
        worksheet.write(count, 34, '')

        if final[i]['proba'] != '':
            worksheet.write(count, 35, 'Проба')
            worksheet.write(count, 36, '')
            worksheet.write(count, 37, final[i]['proba'])

        if final[i]['insert'] != '':
            worksheet.write(count, 38, 'Вставка/камень')
            worksheet.write(count, 39, '')
            worksheet.write(count, 40, final[i]['insert'].replace(', ', '|')[1:])

        if final[i]['outside'] != '':
            worksheet.write(count, 41, 'Покрытие')
            worksheet.write(count, 42, '')
            worksheet.write(count, 43, final[i]['outside'].replace(', ', '|'))

        if final[i]['theme'] != '':
            worksheet.write(count, 44, 'Тематика')
            worksheet.write(count, 45, '')
            worksheet.write(count, 46, final[i]['theme'])
        if final[i]['color'] != '':
            worksheet.write(count, 47, 'Цвет')
            worksheet.write(count, 48, '')
            worksheet.write(count, 49, final[i]['color'])
        if final[i]['typeLock'] != '':
            worksheet.write(count, 50, 'Виды замков')
            worksheet.write(count, 51, '')
            worksheet.write(count, 52, final[i]['typeLock'])
        if final[i]['weight'] != '':
            worksheet.write(count, 53, 'Вес')
            worksheet.write(count, 54, '')
            worksheet.write(count, 55, final[i]['weight'])
        if final[i]['shinka'] != '':
            worksheet.write(count, 98, 'ШиринаШинки')
            worksheet.write(count, 99, '')
            worksheet.write(count, 100, final[i]['shinka'])

        if final[i]['posadka'] != '':
            worksheet.write(count, 101, 'Посадка')
            worksheet.write(count, 102, '')
            worksheet.write(count, 103, final[i]['posadka'])

        if final[i]['zodiak'] != '':
            worksheet.write(count, 104, 'Зодиак')
            worksheet.write(count, 105, '')
            worksheet.write(count, 106, final[i]['zodiak'])
        worksheet.write(count, 107, 'Количество в России')
        worksheet.write(count, 108, '')
        worksheet.write(count, 109, 'Нет на сайте')
        # worksheet.write(count, 110, 'Для детей')
        # worksheet.write(count, 111, '')
        worksheet.write(count, 9, final[i]['childrenFlag'])
        if final[i]['typePlet'] != '':
            worksheet.write(count, 110, 'Вид плетения')
            worksheet.write(count, 111, '')
            worksheet.write(count, 112, final[i]['typePlet'])
        controlId.append(final[i]['id'])

Almaty = []
satu = pd.read_excel('Остаток склада полный.xlsx')
art = satu['Артикул'].tolist()
size = satu['Размеры и кол-во в наличии'].tolist()
weight = satu['вес'].tolist()
number = satu['Количество'].tolist()

Almaty = []
Al2ID = []
sizes = []
weights = []
numbers = []

for i in art:
    if type(i) != float:
        try:
            Al2ID.append(int(i))
        except:
            Al2ID.append(i)

for i in range(len(Al2ID)):
    weights.append(weight[i])
    try:
        numbers.append(int(number[i]))
    except:
        numbers.append(0)
    # try:
    # print(size[i])
    if type(size[i]) != float:
        arr = size[i].split('; ')
        # print(arr)
        arr1 = []
        for j in arr:
            arr1.append(j.split('-')[0])
            # print(arr1)
        sizes.append(arr1)
    else:
        sizes.append([])
    # except:
    #    sizes.append([])

for i in range(len(Al2ID)):
    inf = {
        'id': Al2ID[i],
        'count': numbers[i],
        'sizes': sizes[i],
        'weight': weights[i],
    }
    Almaty.append(inf)

count += 1
for i in Almaty:
    if str(i['id']) in controlId:
        ind = controlId.index(str(i['id']))
        s = mainCol[ind]
        ind += 1
        s += int(i['count'])
        worksheet.write(ind, 8, s)
        if len(i['sizes']) > 0:
            s = '|'.join(i['sizes'])
            worksheet.write(ind, 28, s)
            worksheet.write(ind, 12, '50%')
        else:
            worksheet.write(ind, 28, 'Да')
            worksheet.write(ind, 12, '50%')
    # else:
    #    worksheet.write(count, 0, i['id'])
    #    count += 1
    # print(i)

workbook.close()
