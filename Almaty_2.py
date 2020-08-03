import os


print('Get TD links...')
try:
    os.system('python TDLiknks.py')
except:
    print('TD smth')

# print('Get children links from TD...')
# os.system('python TD_children.py')

print('SokolovOpt is processing...')
os.system('python SokolovOpt.py')

print('SokolovRozn is processing...')
os.system('scrapy runspider SokolovRozn.py')

print('Fetching SokolovData...')
os.system('python SokolovData.py')
print('Parse TD...')
os.system('python TDserebro.py')
print('Get data from Satu')
os.system('python test.py')

print('Fetching data with TD and Almaty2')
os.system('python Sokolov_TD.py')


