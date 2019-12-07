#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibrarySystem.settings")
django.setup()

import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.test import TestCase
from xlrd import open_workbook

from locallibrary.models import Book

# 将选择器过滤的信息分离
col_list = ["书名", "作者", "出版社", "出版日期", "价格", "ISBN", "简介"]
title_list = []
info_list = []
author_list = []
image_list = []
press_list = []
publish_date_list = []
price_list = []
summary_list = []

link_list = []

# 链接数据库
book_set = Book.objects.all()
book_exist_list = []

# 获取数据库中现有的图书名
for item in book_set:
    book_exist_list.append(item.book_name)
print("数据库中已经存在的book：", book_exist_list)


# 抓取豆瓣读书某个分类下的全部书籍列表信息
def get_list_from_scraper(url):
    # 使用requests请求书籍页面列表
    # 加入header是为了增加浏览器请求代理，防止因请求被截断
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    response = requests.get(url, headers=header)
    text = response.content.decode('utf-8')

    # 使用bs4的select选择器选取列表中的title，info，summary
    soup = BeautifulSoup(text, 'html.parser')
    # print(text)
    # 截取20条链接
    for i in range(1, 21):
        # print("#subject_list > ul > li:nth-child(" + str(i) + ") > div.info")
        # author, press, publish time, price,
        try:
            temp2 = soup.select("#subject_list > ul > li:nth-child(" + str(i) + ") > div.info > div.pub")[0].string
        except:
            continue
        else:
            info = str(temp2).strip().split('/')

        if len(info) == 5:
            author_list.append(info[0])
            press_list.append(info[2])
            publish_date_list.append(info[3])
            price_list.append(info[4])
        elif len(info) == 4:
            author_list.append(info[0])
            press_list.append(info[1])
            publish_date_list.append(info[2])
            price_list.append(info[3])
        else:
            print(len(info), info)
            continue

        # title string
        title_string = soup.select("#subject_list > ul > li:nth-child(" + str(i) + ") > div.info > h2 > a")[0].string
        # print(str(title_string).strip())
        title_list.append(str(title_string).strip())

        # image src
        image_src = soup.select("#subject_list > ul > li:nth-child(" + str(i) + ") > div.pic > a > img")[0].get('src')
        # print(image_src)
        image_list.append(image_src)

        # subject href
        link_href = soup.select("#subject_list > ul > li:nth-child(" + str(i) + ") > div.info > h2 > a")[0].get('href')
        # print(subject_href)
        link_list.append(link_href)

    # print(image_list, title_list, link_list, info_list)
    # return link_list


def get_summary_from_list(link_list):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    # 需要从书目详情页中获得内容简介
    failed_list = []
    for link in link_list:
        time.sleep(1)
        # print(link)
        response = requests.get(link, headers=header)
        soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
        try:
            filter_set = soup.select('#link-report > div:nth-child(1) > div > p')[0].string
        except:
            # failed_list.append(link)
            summary_list.append("None")
        else:
            summary_list.append(filter_set)

    # print(failed_list)


def get_image_from_list(image_list):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    for i in range(len(image_list)):
        time.sleep(2)
        if title_list[i] != "None":
            res = requests.get(image_list[i], stream=True, headers=header)
            save_path = "locallibrary/static/image/" + title_list[i] + ".jpg"
            with open(save_path, 'wb') as file:
                file.write(res.content)


def load_data_from_list(url, tag):

    # 爬取书籍内容
    get_list_from_scraper(url)
    get_summary_from_list(link_list)
    get_image_from_list(image_list)
    load_data_from_list(tag)

    # 将数据记录保存到数据库中
    cnt = 0
    for i in range(len(title_list)):
        if title_list[i] != "None" and title_list[i] not in book_exist_list:
            # print(len(publish_date_list[i].strip()), publish_date_list[i])
            if len(publish_date_list[i].strip()) <= 7:
                date = datetime.strptime(publish_date_list[i].strip(), "%Y-%m")
            else:
                date = datetime.strptime(publish_date_list[i].strip(), "%Y-%m-%d")
            new_record = Book.objects.create(book_name=title_list[i],
                                             book_author=author_list[i],
                                             book_press=press_list[i],
                                             book_publish_date=date,
                                             book_price=price_list[i][:-1],
                                             book_summary=summary_list[i],
                                             book_category_choice=tag)
            new_record.save()
            cnt += 1
    print("Successfully execute: ", cnt)


def load_data_from_file(file_path):
    data = open_workbook(file_path)
    table = data.sheets()[0]
    row_number = table.nrows
    cnt = 0
    for i in range(1, row_number):
        row = table.row_values(i)
        if row[1] in book_exist_list:
            continue
        print(row)
        # print(row[8])
        if len(row[7].strip()) <= 7:
            date = datetime.strptime(row[7].strip(), "%Y-%m")
        else:
            date = datetime.strptime(row[7].strip(), "%Y-%m-%d")

        new_record = Book.objects.create(book_name=row[1],
                                         book_author=row[2],
                                         book_press=row[3],
                                         book_isbn=row[4],
                                         book_language=row[5],
                                         book_price=row[6],
                                         book_publish_date=date,
                                         book_number=row[8],
                                         book_category_choice=row[9],
                                         book_summary=row[10],
                                         )
        new_record.save()
        cnt += 1
    print("successfully execute: ", cnt)


class DatabaseTest(TestCase):
    # 书籍分类标签
    tag = "society"
    url = 'https://book.douban.com/tag/' + tag
    file_path = "C:/Users/imagi/Downloads/Book-2019-12-07.xls"

    # 从爬虫中获取书籍，并写入数据库
    # load_data_from_list(url, tag)

    # 从文件中读取书籍，并写入数据库
    load_data_from_file(file_path)






