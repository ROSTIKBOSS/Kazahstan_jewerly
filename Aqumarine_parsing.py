import scrapy
import pandas as pd
from fake_useragent import UserAgent
import json
import requests


ua = UserAgent()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'IWusrsesckgd=jojhbQMjYWEdV9ohRKijJKalgxKEvPEPzVqoH/F2376n50ziaNRcMA==; ICusrcartgd=be6d8ad2-c52e-49b8-83b2-f384a9feaa60; ASP.NET_SessionId=fml4b0tqtwa11fu3rmnfi24n',
    'Host': 'catalog.aquamarine.kz',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': ua.random
}
with open('Aqumarine_links.json', 'r') as out:
    js = json.load(out)
with open('Aqumarine_types.json', 'r') as out:
    js1 = json.load(out)

links = js
final = []
headers_1 = ['Код_товара', 'Название_позиции', 'Поисковые_запросы', 'Описание', 'Тип_товара', 'Цена', 'Валюта',
             'Единица_измерения', 'Количество', 'Товарная категория', 'Ссылка_изображения', 'Наличие', 'Скидка',
             'Производитель', 'Страна_производитель', 'Вес', 'Тип вставки', 'Вставка', 'Цвет вставки', 'Коллекция',
             'Размер', 'Покрытие', 'Вид изделия', ]
count = 1
for item in links:
    print(item)
    print(count)
    product = []
    req = requests.get(item, headers=headers)
    sel = scrapy.Selector(req)
    article = sel.css('td:contains(\'Артикул\') + td::text').get()
    name = sel.css('td > div::text').get()
    price = sel.css('td:contains(\'Цена\') + td::text').get()
    image = sel.css('div.imageview img::attr(src)').get()
    product.append(article)
    product.append(name)
    product.append('')
    product.append('')
    product.append('r')
    product.append(price)
    product.append('KZT')
    product.append('шт.')
    product.append('Кол-во')
    product.append('')
    product.append('http://catalog.aquamarine.kz/' + str(image))
    product.append('+')
    product.append('50%')
    product.append('AQUAMARINE')
    product.append('Россия')
    weight = sel.css('td:contains(\'вес\') + td::text').get()
    product.append(weight)
    if item in js1['SW']:
        product.append('SW')
    elif item in js1['Без вставок']:
        product.append('Без вставки')
    elif item in js1['Искусственные']:
        product.append('Искусственные')
    elif item in js1['Полудрагоценные']:
        product.append('Полудрагоценные')
    else:
        product.append('')

    if item in js1['Агат аметистовый']:
        product.append('Агат аметистовый')
    elif item in js1['Агат голубой']:
        product.append('Агат голубой')
    elif item in js1['Агат зеленый']:
        product.append('Агат зеленый')
    elif item in js1['Агат розовый']:
        product.append('Агат розовый')
    elif item in js1['Агат рубиновый']:
        product.append('Агат рубиновый')
    elif item in js1['Александрит иск.']:
        product.append('Александрит иск.')
    elif item in js1['Алексит лаванд. иск.']:
        product.append('Алексит лаванд. иск.')
    elif item in js1['Аметист']:
        product.append('Аметист')
    elif item in js1['Аметист иск.']:
        product.append('Аметист иск.')
    elif item in js1['Бирюза иск.']:
        product.append('Бирюза иск.')
    elif item in js1['Бирюза иск.голуб.сет.']:
        product.append('Бирюза иск.голуб.сет.')
    elif item in js1['Бриллиант']:
        product.append('Бриллиант')
    elif item in js1['Винил алмазная крошка']:
        product.append('Винил алмазная крошка')
    elif item in js1['Гранат']:
        product.append('Гранат')
    elif item in js1['Грин Аметист']:
        product.append('Грин Аметист')
    elif item in js1['Дублет фианит/стекло']:
        product.append('Дублет фианит/стекло')
    elif item in js1['Дуплет фианит/стекло']:
        product.append('Дуплет фианит/стекло')
    elif item in js1['Имитация жемчуга']:
        product.append('Имитация жемчуга')
    elif item in js1['Каучук']:
        product.append('Каучук')
    elif item in js1['Кварц дымчатый']:
        product.append('Кварц дымчатый')
    elif item in js1['Кварц Коньячный']:
        product.append('Кварц Коньячный')
    elif item in js1['Кварц Медовый']:
        product.append('Кварц Медовый')
    elif item in js1['Кварц Олива']:
        product.append('Кварц Олива')
    elif item in js1['Кварц Розовый']:
        product.append('Кварц Розовый')
    elif item in js1['Керамика']:
        product.append('Керамика')
    elif item in js1['Керамическое покрытие']:
        product.append('Керамическое покрытие')
    elif item in js1['Кожа']:
        product.append('Кожа')
    elif item in js1['Корунд']:
        product.append('Корунд')
    elif item in js1['Корунд рубиновый']:
        product.append('Корунд рубиновый')
    elif item in js1['Культ. Жемчуг  АА']:
        product.append('Культ. Жемчуг  АА')
    elif item in js1['Культ. Жемчуг  ААА']:
        product.append('Культ. Жемчуг  ААА')
    elif item in js1['Леска']:
        product.append('Леска')
    elif item in js1['Лимонный Кварц']:
        product.append('Лимонный Кварц')
    elif item in js1['Морион']:
        product.append('Морион')
    elif item in js1['Наноаметист']:
        product.append('Наноаметист')
    elif item in js1['Наноаметист иск.']:
        product.append('Наноаметист иск.')
    elif item in js1['Наногранат иск.']:
        product.append('Наногранат иск.')
    elif item in js1['Наноизумруд']:
        product.append('Наноизумруд')
    elif item in js1['Нанокристалл']:
        product.append('Нанокристалл')
    elif item in js1['Нанокристалл Грей']:
        product.append('Нанокристалл Грей')
    elif item in js1['Нанокристалл Грей  иск.']:
        product.append('Нанокристалл Грей  иск.')
    elif item in js1['Наноморганит иск.']:
        product.append('Наноморганит иск.')
    elif item in js1['Нанорубеллит иск.']:
        product.append('Нанорубеллит иск.')
    elif item in js1['Наносапфир']:
        product.append('Наносапфир')
    elif item in js1['Нанотанзанит иск.']:
        product.append('Нанотанзанит иск.')
    elif item in js1['Нанотопаз']:
        product.append('Нанотопаз')
    elif item in js1['Нанотопаз лондон иск.']:
        product.append('Нанотопаз лондон иск.')
    elif item in js1['Нанотопаз свисс иск.']:
        product.append('Нанотопаз свисс иск.')
    elif item in js1['Нанотурмалин']:
        product.append('Нанотурмалин')
    elif item in js1['Нанотурмалин иск.']:
        product.append('Нанотурмалин иск.')
    elif item in js1['Нанохризолит']:
        product.append('Нанохризолит')
    elif item in js1['Нанохризолит иск.']:
        product.append('Нанохризолит иск.')
    elif item in js1['Наноцитрин']:
        product.append('Наноцитрин')
    elif item in js1['Наноцитрин иск.']:
        product.append('Наноцитрин иск.')
    elif item in js1['Оникс черный']:
        product.append('Оникс черный')
    elif item in js1['Опал белый иск.']:
        product.append('Опал белый иск.')
    elif item in js1['Опал блед-голуб иск.']:
        product.append('Опал блед-голуб иск.')
    elif item in js1['Опал изумрудный иск.']:
        product.append('Опал изумрудный иск.')
    elif item in js1['Опал сапфировый иск.']:
        product.append('Опал сапфировый иск.')
    elif item in js1['Опал черный иск.']:
        product.append('Опал черный иск.')
    elif item in js1['Перламутр']:
        product.append('Перламутр')
    elif item in js1['Пластик']:
        product.append('Пластик')
    elif item in js1['поделочный камень']:
        product.append('поделочный камень')
    elif item in js1['Празиолит']:
        product.append('Празиолит')
    elif item in js1['Раухтопаз']:
        product.append('Раухтопаз')
    elif item in js1['Стекло']:
        product.append('Стекло')
    elif item in js1['Султанит иск.']:
        product.append('Султанит иск.')
    elif item in js1['Топаз Swarovski Gems']:
        product.append('Топаз Swarovski Gems')
    elif item in js1['Топаз Лондон Блю']:
        product.append('Топаз Лондон Блю')
    elif item in js1['Топаз Свисс Блю']:
        product.append('Топаз Свисс Блю')
    elif item in js1['Топаз Скай Блю']:
        product.append('Топаз Скай Блю')
    elif item in js1['Турмалин зеленый иск.']:
        product.append('Турмалин зеленый иск.')
    elif item in js1['Фианит']:
        product.append('Фианит')
    elif item in js1['ФИАНИТ SWAROVSKI']:
        product.append('ФИАНИТ SWAROVSKI')
    elif item in js1['Фианит иск.']:
        product.append('Фианит иск.')
    elif item in js1['Фианит черный']:
        product.append('Фианит черный')
    elif item in js1['Хризолит']:
        product.append('Хризолит')
    elif item in js1['Цитрин']:
        product.append('Цитрин')
    elif item in js1['Шнур нейлон']:
        product.append('Шнур нейлон')
    elif item in js1['Шнур текстильный']:
        product.append('Шнур текстильный')
    elif item in js1['Шнур хлопчатобумажный']:
        product.append('Шнур хлопчатобумажный')
    elif item in js1['Шпинель']:
        product.append('Шпинель')
    elif item in js1['ы Аметист']:
        product.append('Аметист')
    elif item in js1['Эмаль']:
        product.append('Эмаль')
    else:
        product.append('')

    if item in js1['белый']:
        product.append('белый')
    elif item in js1['Бесцветный']:
        product.append('Бесцветный')
    elif item in js1['Голубой']:
        product.append('Голубой')
    elif item in js1['Голубой хамелеон']:
        product.append('Голубой хамелеон')
    elif item in js1['Желтый']:
        product.append('Желтый')
    elif item in js1['Зеленый']:
        product.append('Зеленый')
    elif item in js1['зелёный агат']:
        product.append('зелёный агат')
    elif item in js1['Золотисто синий']:
        product.append('Золотисто синий')
    elif item in js1['Золотистый']:
        product.append('Золотистый')
    elif item in js1['Изумруд']:
        product.append('Изумруд')
    elif item in js1['Коричневый']:
        product.append('Коричневый')
    elif item in js1['Красный']:
        product.append('Красный')
    elif item in js1['Лаванда']:
        product.append('Лаванда')
    elif item in js1['Лондон']:
        product.append('Лондон')
    elif item in js1['молочный']:
        product.append('молочный')
    elif item in js1['Оранжевый']:
        product.append('Оранжевый')
    elif item in js1['Параиба']:
        product.append('Параиба')
    elif item in js1['Розовый']:
        product.append('Розовый')
    elif item in js1['Рубин']:
        product.append('Рубин')
    elif item in js1['Сапфир']:
        product.append('Сапфир')
    elif item in js1['Серебристо лавандовый']:
        product.append('Серебристо лавандовый')
    elif item in js1['серебристый']:
        product.append('серебристый')
    elif item in js1['Серый']:
        product.append('Серый')
    elif item in js1['Синий']:
        product.append('Синий')
    elif item in js1['фиолетовый']:
        product.append('фиолетовый')
    elif item in js1['Хризолитовый']:
        product.append('Хризолитовый')
    elif item in js1['Цветной']:
        product.append('Цветной')
    elif item in js1['Цитрин M']:
        product.append('Цитрин M')
    elif item in js1['черный']:
        product.append('черный')
    elif item in js1['Шампань']:
        product.append('Шампань')
    else:
        product.append('')

    if item in js1['Baguette']:
        product.append('Baguette')
    elif item in js1['Belle']:
        product.append('Belle')
    elif item in js1['Book']:
        product.append('Book')
    elif item in js1['Brave']:
        product.append('Brave')
    elif item in js1['Bubbles']:
        product.append('Bubbles')
    elif item in js1['Christmas Story']:
        product.append('Christmas Story')
    elif item in js1['Color block']:
        product.append('Color block')
    elif item in js1['Color boom']:
        product.append('Color boom')
    elif item in js1['Double Dream']:
        product.append('Double Dream')
    elif item in js1['Dynamic']:
        product.append('Dynamic')
    elif item in js1['Energy']:
        product.append('Energy')
    elif item in js1['Fancy']:
        product.append('Fancy')
    elif item in js1['Fashion Spice']:
        product.append('Fashion Spice')
    elif item in js1['Fly']:
        product.append('Fly')
    elif item in js1['Foxy']:
        product.append('Foxy')
    elif item in js1['French ball']:
        product.append('French ball')
    elif item in js1['Fresh']:
        product.append('Fresh')
    elif item in js1['Funny']:
        product.append('Funny')
    elif item in js1['Geometry']:
        product.append('Geometry')
    elif item in js1['Gothic']:
        product.append('Gothic')
    elif item in js1['Happy']:
        product.append('Happy')
    elif item in js1['Hello Kitty']:
        product.append('Hello Kitty')
    elif item in js1['In City']:
        product.append('In City')
    elif item in js1['Inari']:
        product.append('Inari')
    elif item in js1['Jazz']:
        product.append('Jazz')
    elif item in js1['Juicy']:
        product.append('Juicy')
    elif item in js1['Lady Style']:
        product.append('Lady Style')
    elif item in js1['Little Tropic']:
        product.append('Little Tropic')
    elif item in js1['Love story']:
        product.append('Love story')
    elif item in js1['Maxima']:
        product.append('Maxima')
    elif item in js1['Mehendi']:
        product.append('Mehendi')
    elif item in js1['Mon Amour']:
        product.append('Mon Amour')
    elif item in js1['Monaco']:
        product.append('Monaco')
    elif item in js1['Moon']:
        product.append('Moon')
    elif item in js1['Must Have']:
        product.append('Must Have')
    elif item in js1['Neo']:
        product.append('Neo')
    elif item in js1['Nimfa']:
        product.append('Nimfa')
    elif item in js1['Paloma']:
        product.append('Paloma')
    elif item in js1['Polaris']:
        product.append('Polaris')
    elif item in js1['Regina']:
        product.append('Regina')
    elif item in js1['Rio']:
        product.append('Rio')
    elif item in js1['Route']:
        product.append('Route')
    elif item in js1['Safary']:
        product.append('Safary')
    elif item in js1['Sci-Fi']:
        product.append('Sci-Fi')
    elif item in js1['Spark']:
        product.append('Spark')
    elif item in js1['Spring']:
        product.append('Spring')
    elif item in js1['Stones']:
        product.append('Stones')
    elif item in js1['Summer']:
        product.append('Summer')
    elif item in js1['Sunshine']:
        product.append('Sunshine')
    elif item in js1['Supreme']:
        product.append('Supreme')
    elif item in js1['Toys']:
        product.append('Toys')
    elif item in js1['Twin']:
        product.append('Twin')
    elif item in js1['TWO in ONE']:
        product.append('TWO in ONE')
    elif item in js1['Undina']:
        product.append('Undina')
    elif item in js1['Volum']:
        product.append('Volum')
    elif item in js1['Авангард']:
        product.append('Авангард')
    elif item in js1['Аккорд']:
        product.append('Аккорд')
    elif item in js1['Алиса']:
        product.append('Алиса')
    elif item in js1['Андромеда']:
        product.append('Андромеда')
    elif item in js1['Ар-Деко']:
        product.append('Ар-Деко')
    elif item in js1['Аура']:
        product.append('Аура')
    elif item in js1['Афины']:
        product.append('Афины')
    elif item in js1['Благовест']:
        product.append('Благовест')
    elif item in js1['Валенсия']:
        product.append('Валенсия')
    elif item in js1['Вервица']:
        product.append('Вервица')
    elif item in js1['Версаль']:
        product.append('Версаль')
    elif item in js1['Восточная сказка']:
        product.append('Восточная сказка')
    elif item in js1['Гипноз']:
        product.append('Гипноз')
    elif item in js1['Гороскоп']:
        product.append('Гороскоп')
    elif item in js1['Гравитация']:
        product.append('Гравитация')
    elif item in js1['Джулия']:
        product.append('Джулия')
    elif item in js1['Джуна']:
        product.append('Джуна')
    elif item in js1['Жозефина']:
        product.append('Жозефина')
    elif item in js1['Забава']:
        product.append('Забава')
    elif item in js1['Иман Нуры']:
        product.append('Иман Нуры')
    elif item in js1['Камелия']:
        product.append('Камелия')
    elif item in js1['Каприз']:
        product.append('Каприз')
    elif item in js1['Кармен']:
        product.append('Кармен')
    elif item in js1['Клеопатра']:
        product.append('Клеопатра')
    elif item in js1['Лагуна']:
        product.append('Лагуна')
    elif item in js1['Лолита']:
        product.append('Лолита')
    elif item in js1['Мой ангел']:
        product.append('Мой ангел')
    elif item in js1['Монпансье']:
        product.append('Монпансье')
    elif item in js1['Океан']:
        product.append('Океан')
    elif item in js1['Отражение']:
        product.append('Отражение')
    elif item in js1['Помпеи']:
        product.append('Помпеи')
    elif item in js1['Рандеву']:
        product.append('Рандеву')
    elif item in js1['Сакура']:
        product.append('Сакура')
    elif item in js1['Тея']:
        product.append('Тея')
    elif item in js1['Флёр']:
        product.append('Флёр')
    elif item in js1['Флоренция']:
        product.append('Флоренция')
    elif item in js1['Фруктовый лёд']:
        product.append('Фруктовый лёд')
    else:
        product.append('')

    if item in js1['11.0']:
        product.append('11.0')
    elif item in js1['12.0']:
        product.append('12.0')
    elif item in js1['12.5']:
        product.append('12.5')
    elif item in js1['13.0']:
        product.append('13.0')
    elif item in js1['13.5']:
        product.append('13.5')
    elif item in js1['14.0']:
        product.append('14.0')
    elif item in js1['14.5']:
        product.append('14.5')
    elif item in js1['15.0']:
        product.append('15.0')
    elif item in js1['15.5']:
        product.append('15.5')
    elif item in js1['16.0']:
        product.append('16.0')
    elif item in js1['16.5']:
        product.append('16.5')
    elif item in js1['17.0']:
        product.append('17.0')
    elif item in js1['17.5']:
        product.append('17.5')
    elif item in js1['18.0']:
        product.append('18.0')
    elif item in js1['18.5']:
        product.append('18.5')
    elif item in js1['19.0']:
        product.append('19.0')
    elif item in js1['20.0']:
        product.append('20.0')
    elif item in js1['20.5']:
        product.append('20.5')
    elif item in js1['21.0']:
        product.append('21.0')
    elif item in js1['21.5']:
        product.append('21.5')
    elif item in js1['22.0']:
        product.append('22.0')
    elif item in js1['22.5']:
        product.append('22.5')
    elif item in js1['23.0']:
        product.append('23.0')
    elif item in js1['23.5']:
        product.append('23.5')
    elif item in js1['24.0']:
        product.append('24.0')
    elif item in js1['25.0']:
        product.append('25.0')
    elif item in js1['26.0']:
        product.append('26.0')
    elif item in js1['26.5']:
        product.append('26.5')
    elif item in js1['30.0']:
        product.append('30.0')
    elif item in js1['35.0']:
        product.append('35.0')
    elif item in js1['38.0']:
        product.append('38.0')
    elif item in js1['39.0']:
        product.append('39.0')
    elif item in js1['38.0']:
        product.append('38.0')
    elif item in js1['40.0']:
        product.append('40.0')
    elif item in js1['45.0']:
        product.append('45.0')
    elif item in js1['50.0']:
        product.append('50.0')
    elif item in js1['55.0']:
        product.append('55.0')
    elif item in js1['60.0']:
        product.append('60.0')
    elif item in js1['65.0']:
        product.append('65.0')
    elif item in js1['70.0']:
        product.append('70.0')
    elif item in js1['75.0']:
        product.append('75.0')
    elif item in js1['80.0']:
        product.append('80.0')
    elif item in js1['85.0']:
        product.append('85.0')
    elif item in js1['90.0']:
        product.append('90.0')
    elif item in js1['95.0']:
        product.append('95.0')
    elif item in js1['100.0']:
        product.append('100.0')
    elif item in js1['105.0']:
        product.append('105.0')
    elif item in js1['110.0']:
        product.append('110.0')
    elif item in js1['115.0']:
        product.append('115.0')
    elif item in js1['120.0']:
        product.append('120.0')
    elif item in js1['125.0']:
        product.append('125.0')
    else:
        product.append('')

    if item in js1['Без покрытия']:
        product.append('Без покрытия')
    elif item in js1['Позолота']:
        product.append('Позолота')
    elif item in js1['Родаж']:
        product.append('Родаж')
    else:
        product.append('')

    if item in js1['Жёсткие браслеты']:
        product.append('Жёсткие браслеты')
    elif item in js1['Браслеты на шнурке']:
        product.append('Браслеты на шнурке')
    elif item in js1['Браслеты классические']:
        product.append('Браслеты классические')
    elif item in js1['браслеты детские']:
        product.append('браслеты детские')
    elif item in js1['Браслет православный']:
        product.append('Браслет православный')
    elif item in js1['Браслеты тематические']:
        product.append('Браслеты тематические')
    elif item in js1['Броши']:
        product.append('Броши')
    elif item in js1['Буквы']:
        product.append('Буквы')
    elif item in js1['Булавки']:
        product.append('Булавки')
    elif item in js1['Зажимы для галстука']:
        product.append('Зажимы для галстука')
    elif item in js1['Заколки и гребни']:
        product.append('Заколки и гребни')
    elif item in js1['Запонки']:
        product.append('Запонки')
    elif item in js1['Значки']:
        product.append('Значки')
    elif item in js1['Иконы настольные']:
        product.append('Иконы настольные')
    elif item in js1['Колье текстильное']:
        product.append('Колье текстильное')
    elif item in js1['Колье классические']:
        product.append('Колье классические')
    elif item in js1['Колье из каучука']:
        product.append('Колье из каучука')
    elif item in js1['Колье на леске']:
        product.append('Колье на леске')
    elif item in js1['Обручальные кольца']:
        product.append('Обручальные кольца')
    elif item in js1['Накладки на кольца']:
        product.append('Накладки на кольца')
    elif item in js1['Мусульманские кольца']:
        product.append('Мусульманские кольца')
    elif item in js1['Мужские печатки']:
        product.append('Мужские печатки')
    elif item in js1['Кольца православные']:
        product.append('Кольца православные')
    elif item in js1['Кольца венчальные']:
        product.append('Кольца венчальные')
    elif item in js1['Кольца помолвочные']:
        product.append('Кольца помолвочные')
    elif item in js1['Кольца на 2-ю фалангу']:
        product.append('Кольца на 2-ю фалангу')
    elif item in js1['Кольца на две фаланги']:
        product.append('Кольца на две фаланги')
    elif item in js1['Кольца на пальцы ног']:
        product.append('Кольца на пальцы ног')
    elif item in js1['Кольца детские']:
        product.append('Кольца детские')
    elif item in js1['Кольца на 2 пальца']:
        product.append('Кольца на 2 пальца')
    elif item in js1['Кольца классические']:
        product.append('Кольца классические')
    elif item in js1['Кольца тематические']:
        product.append('Кольца тематические')
    elif item in js1['Кресты православные']:
        product.append('Кресты православные')
    elif item in js1['Ложки']:
        product.append('Ложки')
    elif item in js1['Ложки-загребушки']:
        product.append('Ложки-загребушки')
    elif item in js1['Монеты']:
        product.append('Монеты')
    elif item in js1['Пирсинг в бровь']:
        product.append('Пирсинг в бровь')
    elif item in js1['Пирсинг в пупок']:
        product.append('Пирсинг в пупок')
    elif item in js1['Знаки зодиака']:
        product.append('Знаки зодиака')
    elif item in js1['Мусульманские подвески']:
        product.append('Мусульманские подвески')
    elif item in js1['Еврейские подвески']:
        product.append('Еврейские подвески')
    elif item in js1['Кресты декоративные']:
        product.append('Кресты декоративные')
    elif item in js1['Иконы нательные']:
        product.append('Иконы нательные')
    elif item in js1['Подвески тематические']:
        product.append('Подвески тематические')
    elif item in js1['Кресты католические']:
        product.append('Кресты католические')
    elif item in js1['Подвески детские']:
        product.append('Подвески детские')
    elif item in js1['Бегунки']:
        product.append('Бегунки')
    elif item in js1['Ладанки']:
        product.append('Ладанки')
    elif item in js1['Подвески на карабине']:
        product.append('Подвески на карабине')
    elif item in js1['Подвески классические']:
        product.append('Подвески классические')
    elif item in js1['Шарм']:
        product.append('Шарм')
    elif item in js1['Подвески на цепи']:
        product.append('Подвески на цепи')
    elif item in js1['Серьги-эльфы']:
        product.append('Серьги-эльфы')
    elif item in js1['Серьги-продевки']:
        product.append('Серьги-продевки')
    elif item in js1['Конго']:
        product.append('Конго')
    elif item in js1['Пуссеты']:
        product.append('Пуссеты')
    elif item in js1['Одиночные пуссеты']:
        product.append('Одиночные пуссеты')
    elif item in js1['Серьги длинные']:
        product.append('Серьги длинные')
    elif item in js1['Кафы']:
        product.append('Кафы')
    elif item in js1['Детские серьги']:
        product.append('Детские серьги')
    elif item in js1['Пуссеты-трансформеры']:
        product.append('Пуссеты-трансформеры')
    elif item in js1['Серьги-скобы']:
        product.append('Серьги-скобы')
    elif item in js1['Подкова-сувенир']:
        product.append('Подкова-сувенир')
    elif item in js1['Сувенир']:
        product.append('Сувенир')
    elif item in js1['Цепь']:
        product.append('Цепь')
    else:
        product.append('')

    try:
        s = 'http://catalog.aquamarine.kz/' + image
        final.append(product)
    except:
        pass
    count += 1

df = pd.DataFrame(final, columns=headers_1)
df.to_excel('AqumarineData.xls', index=False)
