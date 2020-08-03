import pandas as pd
import json
import xlsxwriter
import xlrd
from bs4 import BeautifulSoup
import re

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
    #try:
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
    #except:
    #    sizes.append([])

for i in range(len(Al2ID)):
    inf = {
        'id': Al2ID[i],
        'count': numbers[i],
        'sizes': sizes[i],
        'weight': weights[i],
    }
    Almaty.append(inf)


print(Almaty)

