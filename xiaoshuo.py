# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup

class XiaoShuoCatch:

    def __init__(self):
        self.urls = []
        self.baseUrl = 'http://www.4xiaoshuo.com/55/55533/'

    def getChapterUrls(self):
        req = urllib2.Request(self.baseUrl)
        response = urllib2.urlopen(req)
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        datas = soup.find_all('dd')
        for i in range(12, len(datas)):
            self.urls.append(datas[i].a['href'])

    def getAllDatas(self):
        for index in self.urls:
            url = '%s%s'%(self.baseUrl, index)
            html = self.getDataFromUrl(url)
            soup = BeautifulSoup(html, 'lxml')
            self.saveData(soup)

    def getDataFromUrl(self, url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html = response.read().decode('utf-8')
        return html

    def saveData(self, soup):
        title = self.find_title(soup)
        content = self.find_content(soup)
        with open('异常生物见闻录.txt', 'a') as f:
            f.write(title.encode('utf-8'))
            for stri in content.contents:
                pos = stri.find('br')
                if pos == -1:
                    f.write(stri.encode('utf-8') + '\n')
            f.write('=========================== 我是分隔线 ===============================')
        print ' =========== 完成章节 %s 的下载 =============== ' %title
        
    def find_title(self, soup):
        title = soup.find('h1').contents[0]
        return title

    def find_content(self, soup):
        content = soup.find(id='content')
        return content

spider = XiaoShuoCatch()
spider.getChapterUrls()
spider.getAllDatas()
