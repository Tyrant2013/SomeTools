# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import json
import os
import re
import sys
import StringIO
import gzip

class XiaoShuoCatch:

    def __init__(self):
        self.urls = []
        self.titles = []
        self.infoFileName = 'xiao_shuo_update_info.txt'
        self.loadInfo()

    #加载配置文件
    def loadInfo(self):
        if (os.path.exists(self.infoFileName)):
            lastUpdateInfoFile = open(self.infoFileName, 'r')
            self.updateInfo = json.load(lastUpdateInfoFile)
            lastUpdateInfoFile.close()
        else:
            self.updateInfo = {}
    
    #更新配置文件
    def updateInfoWithNew(self, novelInfo):
        self.updateInfo[novelInfo['novelKey']] = novelInfo
        file_handler = open(self.infoFileName, 'w')
        json.dump(self.updateInfo, file_handler)
        file_handler.close()

    #检查下载
    def checkAndDownload(self):
        for (key, val) in self.updateInfo.items():
            fileName = val['name'].encode('utf-8')
            baseUrl = val['baseUrl']
            lastUrl = val['lastUrl']
            chapterUrls = self.getChapterUrls(baseUrl)
            updateUrls = self.getValidUrls(chapterUrls, lastUrl)
            print u'[%s]共找到%s章, 最新章节有%s章'.encode('utf-8') %(fileName, len(chapterUrls), len(updateUrls))
            if (len(updateUrls)):
                res = self.getAllContentWithUrls(baseUrl, updateUrls, fileName)
                #val['lastUrl'] = updateUrls[-1]
                val['lastUrl'] = res[1]
                self.updateInfoWithNew(val)

    #获取全部章节链接
    def getChapterUrls(self, baseUrl):
        html = self.getDataFromUrl(baseUrl)
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
    def getAllContentWithUrls(self, baseUrl, urls, fileName):
        isError = False
        lastUrl = ""
        for urlIndex in urls:
            url = '%s%s' % (baseUrl, urlIndex)
            html = self.getDataFromUrl(url)
            if (html.strip() == ""):
                isError = True
                break;
            lastUrl = url
            soup = BeautifulSoup(html, 'lxml')
            self.saveData(soup, fileName)
        return (isError, lastUrl)

    def getDataFromUrl(self, url):
        req = urllib2.Request(url)
        opener = urllib2.build_opener()
        html = ""
        try:
            response = opener.open(req)
            isGzip = response.headers.get('Content-Encoding')
            if isGzip:
                compressedData = response.read()
                compressedStream = StringIO.StringIO(compressedData)
                gziper = gzip.GzipFile(fileobj=compressedStream)
                html = gziper.read()
            else:
                html = response.read().decode('utf-8')
        except urllib2.HTTPError, e:
            print u"================== 出错啦：%s".encode('utf-8') %url
            print e.code
            print e.read()
        return html

    def saveData(self, soup, fileName):
        title = self.find_title(soup)
        content = self.find_content(soup)
        with open('%s.txt' % fileName, 'a') as f:
            f.write(title.encode('utf-8'))
            for stri in content.contents:
                pos = stri.find('br')
                if pos == -1:
                    f.write(stri.encode('utf-8') + '\n')
            f.write(u'=========================== 我是分隔线 =============================== \n'.encode('utf-8'))
        print u' =========== 完成章节 %s 的下载 =============== '.encode('utf-8') %title.encode('utf-8')
        
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
