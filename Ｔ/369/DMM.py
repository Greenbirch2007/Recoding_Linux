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
    driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr/td[1]/div[4]/dl/dd/ul/li[1]/a').click()
    driver.close()








# 遍历选择点击

def locate_page():
    while True:
        for item in queue_num():
            N_page= '//*[@id="wrapper"]/table/tbody/tr/td/div[' + str(item) + ']/table/tbody/tr[2]/td/a'
            driver.find_element_by_xpath(N_page).click()
            print(N_page)
            driver.close()




# 转换为一个测试的问题，就是要遍历点击所有的可点击元素
# 需要使用数据容器，队列取值？
# for num in range(1, 526):
    # get_first_page()
    # locate_page(num)
    # print(num)

# 队列只解决了一部分，所以全网还很难拔下来，就把单个先处理完！

# if __name__ == '__main__':
#     while True:
#         # queue_num()
#         get_first_page()
#         # locate_page()









# 等于测试一个大型网站  (单个网站翻页处理完成)

def next_page():
    html = driver.page_source
    selector = etree.HTML(html)
    pages = selector.xpath('//*[@id="wrapper"]/table[1]/tbody/tr[2]/td[2]/b[2]/text()')
    for i in pages:
        num = int(i) + 1
        for i in range(2,num):
            driver.find_element_by_xpath('//*[@id="wrapper"]/table[1]/tbody/tr[3]/td[2]/a[last()-1]').click()






# 用遍历打开网页59次来处理

    # print(html)  #正则还是有问题，选择了一个动态变动的颜色标记是不好的 最近浏览不是每次都有的！所以用数字的颜色取判断吧

def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    selector = etree.HTML(html)
    link = selector.xpath('//*[@id="wrapper"]/table/tbody/tr/td/div/table/tbody/tr[2]/td/a/@href')
    title = selector.xpath('//*[@id="wrapper"]/table/tbody/tr/td/div/table/tbody/tr[2]/td/a/text()')
    for i1,i2 in zip(title,link):
        yield (i1,i2)






#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='FUNS',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into DMM1 (title,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass






#
# if __name__ == '__main__':
#         html = get_first_page()
#         content = parse_html(html)
#         insertDB(content)



#         while True:
#             html = next_page()
#             time.sleep(2)
#             content = parse_html(html)
#             time.sleep(1)
#             insertDB(content)
#             print(datetime.datetime.now())


# p950


# 字段设置了唯一性 unique

# create table DMM1(
# id int not null primary key auto_increment,
# link varchar(100),
# title varchar(28)
# ) engine=InnoDB  charset=utf8;

# 传入url太快了，考虑分成两部分完成：1.先存到数据库中或其他容器中（数据结构不行）
#  2. 再从数据库中逐个调取进行爬取   3. 中间过渡的数据库是用内存型（redis) 还是一般存储型的？
# 4.数据量小，爬取，传入，再解析影响不大，但是分布式爬取大量数据，就必须要切割开来，才能各司其职，有效处理各自的工作！
# 5.容器是必备，分布式必备，代理池也是必备