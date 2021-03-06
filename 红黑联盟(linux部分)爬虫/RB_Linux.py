# -*- coding:utf8 -*-

# 写个小脚本就搞定了！
import re

import pymysql
from requests.exceptions import RequestException
import time

import requests
from selenium import webdriver
from lxml import etree
import datetime


#请求



def call_page(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre'
    }
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None





def parse_html(html):
    selector = etree.HTML(html)
    big_list = []
    names = selector.xpath('//*[@id="fontzoom"]/ul/li/a[2]/text()')
    links = selector.xpath('//*[@id="fontzoom"]/ul/li/a[2]/@href')
    for i1,i2 in zip(names,links):
        big_list.append((i1,i2))
    return big_list



#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Record_Linux',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into RB_Linux (name,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass




if __name__ == '__main__':

    for item in range(1,71):

        url = "https://www.2cto.com/ebook/xitong/Linux/" + str(item) + ".html"
        html = call_page(url)
        content = parse_html(html)
        insertDB(content)
        print(datetime.datetime.now())



# #
# create table RB_Linux(
# id int not null primary key auto_increment,
# name varchar(200),
# link varchar(200)
# ) engine=InnoDB  charset=utf8;

# drop table Record_Linux;