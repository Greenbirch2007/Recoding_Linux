


# /detail.html?cid=jufd00562  爬取第一层连接

# http://ip1.dmm.co.jp/detail.html?cid=jufd00562
# http://pics.dmm.co.jp/digital/video/jufd00562/jufd00562pl.jpg   #封面
#http://pics.dmm.co.jp/digital/video/jufd00562/jufd00562jp-1.jpg
#http://pics.dmm.co.jp/digital/video/jufd00891/jufd00891jp-1.jpg
# http://pics.dmm.co.jp/digital/video/jux00891/jux00891jp-1.jpg

# 写个小脚本就搞定了！
import re

import pymysql

import time
from requests.exceptions import ConnectionError
from selenium import webdriver
from lxml import etree
import datetime
driver = webdriver.Chrome()


#请求  关键在于遍历点击 (操作动作细分！)
# 1. 登录页面可以复用
#2. 点击个人页面，寻求遍历
#3. 点击个人页面，然后翻页，在这个页面最终关闭浏览器！
# 问题，遍历之后如果从最开始又回到之前的下一个！除非使用减去一个容器里面的数字，下一次绝对是最新的！

def queue_num():

    from queue import Queue
    q = Queue()
    for num in range(1, 526):
        q.put(num)
        yield q.get()



def get_first_page():

    url = 'http://ip1.dmm.co.jp/list.html?page=1&view='
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/a').click()
    driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr/td[1]/div[4]/dl/dd/ul/li[6]/a').click()
    driver.find_element_by_xpath('//*[@id="wrapper"]/table/tbody/tr/td/div[36]/table/tbody/tr[2]/td/a').click()
    html = driver.page_source
    # time.sleep(3)
    return html

# 遍历选择点击

# def locate_page():
#     while True:
#         for item in queue_num():
#             N_page= '//*[@id="wrapper"]/table/tbody/tr/td/div[' + str(item) + ']/table/tbody/tr[2]/td/a'
#             driver.find_element_by_xpath(N_page).click()
#             print(N_page)
#             driver.close()




# 转换为一个测试的问题，就是要遍历点击所有的可点击元素
# 需要使用数据容器，队列取值？
# for num in range(1, 526):
    # get_first_page()
    # locate_page(num)
    # print(num)

# 队列只解决了一部分，所以全网还很难拔下来，就把单个先处理完！






# 等于测试一个大型网站  (单个网站翻页处理完成)

def next_page():
    html = driver.page_source
    selector = etree.HTML(html)
    pages = selector.xpath('//*[@id="wrapper"]/table[1]/tbody/tr[2]/td[2]/b[2]/text()')
    for i in pages:
        num = int(i) + 1
        for i in range(2,num):
            time.sleep(3)
            driver.find_element_by_xpath('//*[@id="wrapper"]/table[1]/tbody/tr[3]/td[2]/a[last()-1]').click()
            html = driver.page_source
            # time.sleep(3)
            return html






# 用遍历打开网页59次来处理

    # print(html)  #正则还是有问题，选择了一个动态变动的颜色标记是不好的 最近浏览不是每次都有的！所以用数字的颜色取判断吧

def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    selector = etree.HTML(html)
    link = selector.xpath('//tbody/tr/td/div/dl/dt/a/@href')
    return link
    # Big_list =  []
    # for sel in link:
    #     str_tup = tuple(sel)
    #     Big_list.append(str_tup)
    #     return Big_list
    # for sel in link:
    #     details =  sel[17:0]
    #     print(details)



def new_screan():
    for item in parse_html():
        return 'http://pics.dmm.co.jp/digital/video/'+str(item)+'/'+str(item)+'pl.jpg'

def big_pic():
    for item in parse_html():
        for i in range(1,15):
            return 'http://pics.dmm.co.jp/digital/video/' + str(item) + '/' + str(item) + '-'+ str(i)+'.jpg'



#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='FUNS',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into DMM1 (link) values (%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass






# 需要将列表中的字符串，转换为元祖然后放回远处！
# 刷新的思维！ 列表中的字符串也可以放入到mysql
if __name__ == '__main__':
    html = get_first_page()
    content = parse_html(html)
    insertDB(content)
    while True:
        html = next_page()
        content = parse_html(html)
        insertDB(content)



# 字段设置了唯一性 unique

# create table DMM1(
# id int not null primary key auto_increment,
# link varchar(100)
# ) engine=InnoDB  charset=utf8;

