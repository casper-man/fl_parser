import requests
import json
from bs4 import BeautifulSoup as BS
from local_settings import FILENAME

def get_rss(url):
    add = []
    try:
        with open(f'{FILENAME}.json') as filehandle:
            items = json.load(filehandle)
            # print(items)
    except Exception as ex:
        print(ex)
        items = {}
    r = requests.get(url)
    html = BS(r.content, 'lxml')
    items_list = html.find_all('item')
    for i in items_list:
        category = i.find('category').text
        if category.find('Парсинг данных') != -1:
            title = i.find('title').text.replace('<![CDATA[', '').replace(']]>', '').strip()
            description = i.find('description').text.replace('<![CDATA[', '').replace(']]>', '').strip()
            link = i.find('guid').text.replace('<![CDATA[', '').replace(']]>', '').strip()
            category = category.replace('<![CDATA[', '').replace(']]>', '').strip()
            id = link.split('/')[-2]
            item = {
                'title': title,
                'link': link,
                'category': category
            }
            if not id in items:
                add.append(id)
                items[id] = []
                items[id].append(item)
    with open(f'{FILENAME}.json', 'w+') as filehandle:
        json.dump(items, filehandle, ensure_ascii=False, sort_keys=False, indent=4)
    # print(items)
    return add


def get_ditails(ids):
    with open(f'{FILENAME}.json') as filehandle:
        items = json.load(filehandle)

    for i in ids:
        for k in items[i]:
            print(k['link'])
            r = requests.get(k['link'])
            html = BS(r.content, 'lxml')



def main():
    upd = get_rss(url='https://www.fl.ru/rss/all.xml?category=5')
    if bool(upd):
        get_ditails(ids=upd)


if __name__ == '__main__':
    main()
