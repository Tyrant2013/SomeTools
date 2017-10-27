# -*- coding: utf-8 -*-

import urllib2
import json
import gzip
import StringIO

class TicketCatcher:
    
    def getInfo(self):
        url = 'http://api.12306.com/v1/train/trainInfos?arrStationCode=WHN&deptDate=2017-10-09&deptStationCode=GZQ&findGD=true'
        header = {
            'Host': 'api.12306.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
            'Referer': 'http://12306.com/',
            'origin': 'http://12306.com',
            'Connection': 'keep-alive'
        }
        req = urllib2.Request(url, headers=header)
        #print(req.header_items())
        opener = urllib2.build_opener()
        response = opener.open(req)
        isGzip = response.headers.get('Content-Encoding')
        #print(response.headers)
        html = ''
        if isGzip:
            compressedData = response.read()
            compressedStream = StringIO.StringIO(compressedData)
            gziper = gzip.GzipFile(fileobj=compressedStream)
            html = gziper.read()
        else:
            html = response.read()
        resObj = json.loads(html)
        trainInfos = resObj['data']['trainInfos']
        for item in trainInfos:
            trainCode = item['trainCode'].decode('utf-8')
            startTime = item['deptDate'].decode('utf-8') + ' ' + item['deptTime'].decode('utf-8')
            endTime = item['arrDate'].decode('utf-8') + ' ' + item['arrTime'].decode('utf-8')
            days = item['arriveDays'].encode('utf-8').decode('utf-8')
            seatList = item['seatList']
            seatNum = 0
            for seetItem in seatList:
                if seetItem['seatCode'].decode('utf-8') == 'O':
                    seatNum = seetItem['seatNum'].decode('utf-8')
            print(u'车次: %s\t发车: %s\t到站: %s\t 状态:%s\t余票:%s' %(trainCode, startTime, endTime, days, seatNum))

instance = TicketCatcher()
instance.getInfo()











