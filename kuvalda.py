import csv

import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4

# pip install lxml


url = 'https://samara.kuvalda.ru/catalog/7309-shurupoverty/page-2/?view=alt'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
data = requests.get(url, headers=headers).text
block = BeautifulSoup(data, 'lxml')
heads = block.find_all('div', class_='alt-snippet__content')
print(len(heads))
for i in heads:
    w = i.find_next('a', class_='alt-snippet__title link').get('href')
    # print('https://samara.kuvalda.ru'+w)
    get_url = ('https://samara.kuvalda.ru' + w)
    stock = requests.get(get_url, headers=headers).text
    loom = BeautifulSoup(stock, 'lxml')
    name = loom.find('h1', class_='page-header__title')
    print(name.text.strip())
    head = (name.text.strip())
    codd = loom.find('div', class_='product-buy__code')
    print(codd.text.strip())
    article = (codd.text.strip())
    cena = loom.find('span', class_='product-buy__price-value')
    print(cena.text.strip())
    price = (cena.text.strip())
    params = loom.find('div', class_='product-specs__characteristics spoiler__content').find_all('div',
                                                                                                 class_='product-specs__characteristics-item')
    get_param = []
    for le in params:
        param = le.find_all_next('span')
        # print(param[0].text.strip())
        param_1 = (param[0].text.strip())
        # print(param[1].text.strip())
        param_2 = (param[1].text.strip())
        all_param = param_1 + ': ' + param_2
        print(all_param)
        get_param.append(all_param)
    pixx = loom.find('div', class_='swiper-wrapper').find_all('img', src=True)
    pixes = []
    for pix in pixx:
        print(pix['src'])
        photo = (pix['src'])
        pixes.append(photo)
    print('\n')

    storage = {'name': head, 'code': article, 'price': price, 'params': ';'.join(get_param), 'photos': ';'.join(pixes),
               'url': get_url}

    fields = ['Name', 'Article', 'Price', 'Params', 'Photo', 'URL']
    with open('example.csv', 'a+', encoding='utf-16') as file:
        pisar = csv.writer(file, delimiter='$', lineterminator='\r')
        # Проверяем, находится ли файл в начале и пуст ли
        file.seek(0)
        if len(file.read()) == 0:
            pisar.writerow(fields)  # Записываем заголовки, только если файл пуст
        pisar.writerow(
            [storage['name'], storage['code'], storage['price'], storage['params'], storage['photos'], storage['url']])
