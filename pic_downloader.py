# -*- coding: utf-8 -*-
# HTML pic_downloader for windows
import requests
from bs4 import BeautifulSoup
import os

doc_dir = os.path.abspath(input("Doc dir:"))
doc_list = [os.path.join(doc_dir, doc) for doc in next(os.walk(doc_dir))[2]]


def resolve(doc):
    doc_soup = BeautifulSoup(open(doc, encoding='utf-8'), "html5lib")
    img_list = [img.get('src') for img in doc_soup.find_all('img') if img.src is not None]
    return img_list


def download(img_item):
    trys = 0
    while True:
        try:
            r = requests.get(img_item, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36 Vivaldi/1.2.490.43'})
        except requests.exceptions.ConnectionError:
            trys += 1
            if trys >= 5:
                print("Too many error. Skipping...")
                return None
            print("Connection Error. Retrying... %s" % trys)
        except requests.exceptions.InvalidSchema:
            print("Invalid Schema, Skip.")
            return None
        except BaseException as e:
            print("Error: %s. Skipping..." % e)
            return None
        else:
            break
    return r


for doc in doc_list:
    try:
        print("Resolving %s." % doc.encode(encoding='utf-8').decode(encoding='utf-8'))
    except BaseException:
        print("Resolving %s." % doc.encode())
    img_list = resolve(doc)
    print("Resolved.")
    if img_list is None:
        print("No image file, skip.")
        continue
    imgs = list(map(download, img_list))
    print("Downloaded.")
    for img in imgs:
        if img is None:
            continue
        if not img.status_code == 200:
            print("Status Code is not 200. Skipping...")
            continue
        path = os.path.join(doc_dir, '\\'.join(img.url[7:].split('/'))).replace('?', '.')
        (basename, filename) = os.path.split(path)
        if not os.path.exists(basename):
            os.makedirs(basename)
        with open(path, 'w+b') as img_file:
            img_file.write(img.content)
    print("Saved.")
