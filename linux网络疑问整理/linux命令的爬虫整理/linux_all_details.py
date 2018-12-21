# ! -*- coding:utf-8 -*-



#  用大主题＋大链接＋小主题＋小链接 来弥补不规则的表述～
# 想办法写一个类，中间使用静态方法来处理！
# ，没那么复杂，做一个小容器收集翻页数据，有的话就继续请求，没有就过，
# 如何让循环在合适的时候终止?取出容器之后再删除容器,解决重复调用的问题，还是数据容器或逻辑上进行优化
import time
import re
import pymysql
import requests
from selenium import webdriver
# 还是要用PhantomJS
import datetime
import string
from lxml import etree

N_n = '' #必须每次都要重新 必须用到新的数据结构了! 用栈,后进先出的特性
# 大链接都有重复的!


# 1.栈(stacks)是一种只能通过访问其一端来实现数据存储与检索的线性数据结构，具有后进先出(last in first out，LIFO)的特征
#
# 2.队列(queue)是一种具有先进先出特征的线性数据结构，元素的增加只能在一端进行，元素的删除只能在另一端进行。能够增加元素的队列一端称为队尾，可以删除元素的队列一端则称为队首。

def call_pages(url):
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    return html


def parse_pages(html):

    selector = etree.HTML(html)
    title = selector.xpath('//*[@id="arcs-list"]//a/text()')
    links = selector.xpath('//*[@id="arcs-list"]//a/@href')
    next_page = selector.xpath('//*[@id="main-archive"]/div/a/text()')
    for item in next_page:
        stack.append(item)
    for i1, i2 in zip(title, links):
        big_list.append([i1, i2])
    return big_list








def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='LINUX',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # 这里是判断big_list的长度，不是content字符的长度
    try:
        cursor.executemany('insert into linux_learning_details (s_title,s_link,b_link) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except Exception :
        print('出列啦')



def Python_sel_Mysql():
    # 使用cursor()方法获取操作游标
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='LINUX',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    for i in range(1,48):
        sql = 'select * from linux_learning where id = %s ' % i
        # #执行sql语句
        cursor.execute(sql)
        # #获取所有记录列表
        data = cursor.fetchall()
        for item in data:
            d_link = item['link']
            yield d_link


if __name__ == '__main__':

    big_list = []
    stack = []
    for url_item in Python_sel_Mysql():

        html = call_pages(url_item)
        content = parse_pages(html)  # 用一个平行赋值，拆包
        cn_insert1 = []
        for item in content:
            i1,i2 = item
            cn_insert1.append((i1,i2,url_item))
        insertDB(cn_insert1)


            #　１．是否有翻页　２．逻辑判断并处理，３．　果断逻辑终止符
        if len(stack) is  not None:
            try:


                n = stack.pop()  # 使用一个栈的特性,后进先出,取出自动清零的特性
                next_url = url_item + '/page/' + n
                html = call_pages(next_url)
                content = parse_pages(html)  # 用一个平行赋值，拆包
                cn_insert2 = []
                for item in content:
                    i1, i2 = item
                    cn_insert2.append((i1, i2, url_item))
                insertDB(cn_insert2)
                print(url_item)
            except IndexError as e:
                pass







#
#
# #
# #
# create table linux_learning_details (
# id int not null primary key auto_increment,
# s_title varchar(50),
# s_link varchar(150),
# b_link varchar(150)
# ) engine =InnoDB charset=utf8;

# drop table linux_learning_details;