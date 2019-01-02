# 写个小脚本就搞定了！
import re

import pymysql

import time
from requests.exceptions import ConnectionError
from selenium import webdriver
from lxml import etree
import datetime
driver = webdriver.Chrome()


#请求

def get_first_page():
    url = 'http://www.wowhezi.com/video/?page=120'
    # driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
    driver.set_window_size(1200, 1200)  # 设置窗口大小
    driver.get(url)
    # time.sleep(3)
    html = driver.page_source
    # time.sleep(3)
    return html


# 把首页和翻页处理？

def next_page():
    for i in range(1,3566):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a[last()]').click()
        time.sleep(3)
        html = driver.page_source
        return html




# 用遍历打开网页59次来处理

    # print(html)  #正则还是有问题，选择了一个动态变动的颜色标记是不好的 最近浏览不是每次都有的！所以用数字的颜色取判断吧

def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    selector = etree.HTML(html)
    link = selector.xpath('//*[@id="waterfall"]/div/a[1]/@href')
    for link_single in link:
        yield ('http://www.wowhezi.com'+link_single)






#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='FUNS',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into viedos (link) values (%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass







if __name__ == '__main__':
        html = get_first_page()
        content = parse_html(html)
        time.sleep(3)
        insertDB(content)
        while True:
            html = next_page()
            content = parse_html(html)
            insertDB(content)
            print(datetime.datetime.now())





# 字段设置了唯一性 unique

# create table viedos(
# id int not null primary key auto_increment,
# link varchar(88)
# ) engine=InnoDB  charset=utf8;

# 传入url太快了，考虑分成两部分完成：1.先存到数据库中或其他容器中（数据结构不行）
#  2. 再从数据库中逐个调取进行爬取   3. 中间过渡的数据库是用内存型（redis) 还是一般存储型的？
# 4.数据量小，爬取，传入，再解析影响不大，但是分布式爬取大量数据，就必须要切割开来，才能各司其职，有效处理各自的工作！
# 5.容器是必备，分布式必备，代理池也是必备