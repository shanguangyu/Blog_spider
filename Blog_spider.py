#!usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Guangyu Shan <shanguangyu6@gmail.com>


import urllib2
from bs4 import BeautifulSoup, Tag
import re
import datetime


def GetId(url):
    content = urllib2.urlopen(url).read()
    list1 = []
    soup = BeautifulSoup(content)
    # global siteUrls
    for link in soup.findAll('dd',attrs = {'class':'cl'}):
        id_number = re.findall(r'\d+',link.get('id'))
        list1.extend(id_number)
    return list1


def YieldUrlList():
    url = "http://blog.sciencenet.cn/home.php?mod=space&uid=40692&do=blog&view=me&from=space&page=%d"
    for j in range(1, 65):
        soup =  BeautifulSoup(urllib2.urlopen(url % j).read())
        for blog in soup.find_all('dl'):
            date =  blog.find('span', attrs = {'class': 'xg1'}).text
            blog_id = blog.find('dd', attrs = {'class': 'cl'}).get('id').split('_')[-1]
            blog_url = "http://blog.sciencenet.cn/blog-40692-%s.html" % blog_id
            print blog_url
            try:
                GetContent(blog_url, date.encode('utf-8'))
            except:
                continue

  
def GetContent(url, date):
    standard_date = date.split(' ')[0]
    standard_time = date.split(' ')[1]

    standard_time_former = standard_time.split(':')[0]
    standard_time_latter = standard_time.split(':')[1]


    soup = BeautifulSoup(urllib2.urlopen(url).read())
    blog_content = soup.find('div', attrs = {'id':'blog_article', 'class':'d cl'})
    weekday = datetime.datetime.strptime(standard_date,"%Y-%M-%d").strftime("%a")
    content = []
    for text in blog_content.stripped_strings:
        if len(text) == 0:
            continue

        if len(text.replace('.', '')) == 0:
            continue

        if '本文引用地址' in text.encode('utf-8'):
            break

        content.append(text)

    content = "\n\n".join(content).encode('utf-8')

    title = "-".join([t.strip() for t in soup.find('h1', attrs = {'class': 'ph'}).text.encode('utf-8').splitlines() if len(t.strip()) > 0])
    with open("%s[%s-%s,%s_%s].txt" % (title, weekday, standard_date, standard_time_former, standard_time_latter), 'w') as fh:
        fh.write(content)


def main():
    YieldUrlList()


if __name__ =='__main__':
    main()


