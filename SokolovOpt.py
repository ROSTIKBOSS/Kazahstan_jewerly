import json
import requests
from auth_data import sokolov_login, sokolov_password
import base64


def get_token():
    base_url = 'https://api.b2b.sokolov.net/ru-ru/login'

    headers = {
        'Authorization': f"Basic {str(base64.b64encode(f'{sokolov_login}:{sokolov_password}'.encode('UTF-8')), 'UTF-8')}"
    }
    access_token = json.loads(requests.post(base_url, headers=headers).text)['access_token']
    return access_token


def get_and_filter_data(access_token):
    final = []
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': f'Bearer {access_token}'
    }

    url = f'https://api.b2b.sokolov.net/ru-ru/catalog/products?page=1&size=120&filter%5Bmaterial%5D=Серебро'
    lastUrl = ''
    while url != lastUrl:
        response_text = requests.get(url, headers=headers).text
        data = json.loads(response_text)
        url = data['links']['next']['href']
        print(url)
        lastUrl = data['links']['last']['href']
        for item in data['data']:
            final.append(item)
    response_text = requests.get(lastUrl, headers=headers).text
    data = json.loads(response_text)
    for item in data['data']:
        final.append(item)

    with open('SokolovOpt.json', 'w') as out:
        json.dump(final, out)


get_and_filter_data(get_token())
