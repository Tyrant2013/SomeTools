# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import json
import os
import re

class XiaoShuoCatch:

    def __init__(self):
        self.urls = []
        self.titles = []
        self.infoFileName = 'xiao_shuo_update_info.txt'
        self.loadInfo()

    def loadInfo(self):
        if (os.path.exists(self.infoFileName)):
            lastUpdateInfoFile = open(self.infoFileName, 'r')
            self.updateInfo = json.load(lastUpdateInfoFile)
            lastUpdateInfoFile.close()
        else:
            self.updateInfo = {}

    def updateInfoWithNew(self, novelInfo):
        self.updateInfo[novelInfo['novelKey']] = novelInfo
        file_handler = open(self.infoFileName, 'w')
        json.dump(self.updateInfo, file_handler)
        file_handler.close()

    def checkAndDownload(self):
        for (key, val) in self.updateInfo.items():
            fileName = val['name']
            baseUrl = val['baseUrl']
            lastUrl = val['lastUrl']
            chapterUrls = self.getChapterUrls(baseUrl)
            updateUrls = self.getValidUrls(chapterUrls, lastUrl)
            print '只找到%s章, 最新章节有%s章' %(len(chapterUrls), len(updateUrls))
            if (len(updateUrls)):
                self.getAllContentWithUrls(baseUrl, updateUrls)
                val['lastUrl'] = updateUrls[-1]
                self.updateInfoWithNew(val)

    #获取全部章节链接
    def getChapterUrls(self, baseUrl):
        req = urllib2.Request(baseUrl)
        response = urllib2.urlopen(req)
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        datas = soup.find_all('dt')[1].next_siblings
        allUrls = []
        regex = re.compile(r'href=\"(.+?)\"')
        for dd in datas:
            m = regex.findall(str(dd))
            if (len(m) == 1):
                allUrls.append(m[0])
        return allUrls

    #找出最新的章节内容连接
    def getValidUrls(self, urls, lastUrl):
        if (len(lastUrl) == 0):
            return urls
        validUrls = []
        isNew = False
        for urlIndex in urls:
            if (urlIndex == lastUrl):
                isNew = True
                continue
            if (isNew):
                validUrls.append(urlIndex)
                
        return validUrls
        
    #获取指定章节连接的内容
    def getAllContentWithUrls(self, baseUrl, urls):
        for urlIndex in urls:
            url = '%s%s' % (baseUrl, urlIndex)
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
spider.checkAndDownload()
#spider.getLastUpdateUrls()
#spider.printLastUpdateInfo()
#spider.makeADicisionForDownload()

#spider.getChapterUrls()
#spider.getAllDatas()

