# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup

class XiaoShuoCatch:

    def __init__(self):
        self.urls = []
        self.titles = []
        self.baseUrl = 'http://www.4xiaoshuo.com/55/55533/'

    def test(self):
        req = urllib2.Request(self.baseUrl)
        response = urllib2.urlopen(req)
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        print len(soup.find_all('a'))

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

    def getLastUpdateUrls(self):
        req = urllib2.Request(self.baseUrl)
        response = urllib2.urlopen(req)
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        datas = soup.find_all('dd', limit = 12)
        for i in range(0, len(datas)):
            self.urls.append(datas[i].a['href'])
            self.titles.append(datas[i].string)

    def printLastUpdateInfo(self):
        if (len(self.titles) > 0):
            print '找到如下的章节更新：\n' 
            for i in range(0, len(self.titles)):
                title = self.titles[i]
                print '%s %s' %(i + 1, title)

    def makeADicisionForDownload(self):
        tip = '输入要下载的章节序号（0开始下载):'
        index = int(raw_input(tip))
        indexs = []
        while (index != 0):
            indexs.append(index - 1)
            index = int(raw_input(tip))
        needDownloadUrls = []
        needDownloadTitles = []
        for ind in indexs:
            needDownloadUrls.append(self.urls[ind])
            needDownloadTitles.append(self.titles[ind])
        self.urls = needDownloadUrls
        for url in reversed(self.urls):
            print url
        for title in reversed(needDownloadTitles):
            print title
        
    def getLastUpdateData(self):
        for index in reversed(self.urls):
            url = '%s%s' %(self.baseUrl, index)
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
            f.write('=========================== 我是分隔线 =============================== \n')
        print ' =========== 完成章节 %s 的下载 =============== ' %title.encode('utf-8')
        
    def find_title(self, soup):
        title = soup.find('h1').contents[0]
        return title

    def find_content(self, soup):
        content = soup.find(id='content')
        return content

spider = XiaoShuoCatch()
spider.getLastUpdateUrls()
spider.printLastUpdateInfo()
spider.makeADicisionForDownload()
#spider.getLastUpdateData()
#spider.test()
#spider.getChapterUrls()
#spider.getAllDatas()

