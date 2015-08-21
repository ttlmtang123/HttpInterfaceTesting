# -*- coding: utf-8 -*-
##  时间: 2015-02-13
##  跟新内容：
##  增加URL请求时间计算
##  时间: 2015-04-01
##  跟新内容：
##  将指定的测试文件名写入配置文件中，同时增加一个获取当前路径的类
##

import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
import json
import io
import sys
import traceback
import os
import os.path
import  time
import gc
import logging
import configparser
import xml.etree.ElementTree as ET
import random #用于产生随机数字及字母

# this class will create  customer url request

class handleurl(object):

##  for the future account
##   URL_FILE_PATH = 'E:/Work/script/SimulatorAccountlist.xml'

## for the stock account
## StockAccountURLlistxml
    #URL_FILE_PATH = 'StrategyURLlist.xml'
    CONFIG_FILE=r'/conf/xmlFilename.conf'
    URLTypes = []##保存<protocol name="https" brokername="微量期货仿真账户">name 属性
    urllinks =[] #
    URLSubNames=[]  #login link
    brokernames = [] #保存<protocol name="https" brokername="微量期货仿真账户">brokename 属性
    httpstatus = ""
    httpreason = ""
    httpReturnValue= ""   #JSON 对象
    urltaketime ="" #URL请求花费时间
    ISDEBUG=False ### True:debug模式，False:运行模式
    
    global null # JSON 数据返回包含null 数据
    null = 'null'
    def __init__(self):

        super()
        
    def getConfigFile(self):
        """ 测压文件已经放在config文件里"""
        cf = configparser.ConfigParser()
        if self.ISDEBUG:    ## Use debug mode 
            cfFile= r'../conf/xmlFilename.conf'
        else:    
            cfFile= os.path.normcase(os.getcwd() + os.sep +self.CONFIG_FILE)
        print("[cofiguurefie]"+ cfFile)
        cf.read(cfFile)
        xmlfilename = cf['xmlfile']['FileName']
        
        return xmlfilename
    
    def getConfigFolder(self):
        """ 返回配置文件xml所在的目录"""
        cf = configparser.ConfigParser()

        cf = configparser.ConfigParser()
        if self.ISDEBUG:    ## Use debug mode 
            cfFile= r'../conf/xmlFilename.conf'
        else:    
            cfFile= os.path.normcase(os.getcwd() + os.sep +self.CONFIG_FILE)
        print(cfFile)

        cf.read(cfFile)
        foldername = cf['xmlfile']['FoldName']
        print(foldername)
        return foldername
    
    def getXMLFileFullPath(self):
        if self.ISDEBUG:    ## Use debug mode
                xmlfilepath =os.path.normcase(r'..\\' +self.getConfigFolder() +os.sep +self.getConfigFile())
        else:
            xmlfilepath= os.path.normcase(os.getcwd() + os.sep +self.getConfigFolder() +os.sep +self.getConfigFile())
            
        print(xmlfilepath)
        return xmlfilepath
    
    def getRootElement(self,xmlfilepath):
        """ get Root element  """
        tree =ET.parse(xmlfilepath)
        root =tree.getroot()
        return root
        
    def initTestArguments(self):
        "Retyrb arry for link"
        root = self.getRootElement(self.getXMLFileFullPath())
        for child in root:
            
            for item in child:
                self.URLTypes.append(child.get('name'))
                self.brokernames.append(child.get('Target'))
                
##                rdmNum = random.randrange(1000,9999,4)
##                rdmChar = random.choice('abcdefghijklmnopqrstuvwxyz')+ random.choice('abcdefghijklmnopqrstuvwxyz')
##                itemurllink = item.get('url').replace('tang123','tang123'+str(rdmNum)+rdmChar)
                itemurllink = item.get('url')
                self.urllinks.append(itemurllink)
                #self.urllinks.append(item.get('url'))
                self.URLSubNames.append(item.text)
                #print( self.URLTypes, self.brokernames,self.urllinks,self.URLSubNames)
                
    def getURLType(self,urllink):
        Re = urllib.parse.urlparse(urllink)
        self.URLType = Re.scheme
        return self.URLType
    
    def getBaselink(self,urllink):
        Re = urllib.parse.urlparse(urllink)
        baseurl = Re.scheme + '://' + Re.netloc + Re.path + "?"
        return baseurl     

    def getparams(self,urllink):
        """return interl parse mapping obj """
        Re = urllib.parse.urlparse(urllink)
        parm = urllib.parse.parse_qsl(Re.query)
       
        return urllib.parse.urlencode(parm)

    def PrpcesshttpRequest(self, baseurl,parms,encodemethod='utf-8',processmethod='GET'):

        #print(baseurl)
        #print(parms.encode(encodemethod))
        #req = urllib.request.Request(url=baseurl,data=parms.encode(encodemethod),method=processmethod)
        #print("[Handle URL]:",baseurl+str(parms.urldecode))
        print('\n[URL]', baseurl + urllib.parse.unquote(parms))
        
        try:
            
            
##            strtime = time.process_time()
            strtime = time.perf_counter() 
            req = urllib.request.Request(url=baseurl+str(parms))
            httpresp = urllib.request.urlopen(req)

##            endtime = time.process_time()
            endtime = time.perf_counter()
##            logging.info("URL tale time:", str((endtime-strtime)/1000000)) #计算http请求花费的时间
            print("\n[URL 请求花费时间]:", str((endtime-strtime)/1000000),"秒") #计算http请求花费的时间
            print("【URL 请求花费时间】:", str((endtime-strtime)/1000),"豪秒") #计算http请求花费的时间
            self.urltaketime = str((endtime-strtime)/1000)#计算http请求花费的时间
            self.httpstatus =httpresp.status
            self.httpreason =httpresp.reason
            #self.httpReturnValue = httpresp.read().decode('utf-8')
            jstr = httpresp.read().decode('utf-8')
            self.httpReturnValue = self.handleJsonString(jstr) 
        except urllib.error.HTTPError as httperr: 
            print("[Http Error]",httperr)
        except urllib.error.URLError as urlerr:
            print("[Error]",urlerr)
               
    def handleJsonString(self, jstr):
        """
            处理 http response 字串
             返回一个处理好的 html 表的字串
            # html 表格式：
            ===============================================================
            |状态 （k）|返回值（v）|状态 （k）|返回值（v）| 状态 （k）|返回值（v）|
            ===============================================================
            | state   | 0        |info     |xxxxx    |total     |XXXX      |
            ================================================================
            |Data| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX|
            ================================================================
        """
        tbstr = r'<table border="1">'\
                + r'<tr>'\
                + r'<td align="center">状态(k)</td>'\
                + r'<td align="center">值(v)</td>'\
                + r'<td align="center">状态(k)</td>'\
                + r'<td align="center">值(v)</td>'\
                + r'<td align="center">状态(k)</td>'\
                + r'<td align="center">值(v)</td>'\
                + r'</tr>'
        tbend = r'</table>'
        trstr = r'<tr>'
        trend = r'</tr>'
        tdstr = r'<td align="center">'
        tdend = r'</td>'
        tdfull = ""  #完整的td标签 <td></td>
        dictre = json.loads(jstr)#转为dict

        for key,value in dictre.items():
            if key != 'data':
                tdfull = tdfull + tdstr+ key +tdend + tdstr+ str(value) +tdend  #完整的td标签

        trfull = trstr +  tdfull + trend   #完整的tr标签
        

        
        datastr = dictre['data']

        datacollect = ""
##        print(type(datastr))
        if type(datastr) == type (None):
            datacollect = null
        elif type(datastr) == type(dict()):
            for k,v in datastr.items():
                 datacollect = datacollect +  str(k) + r' : ' + str(v) + r'<hr />'
##                 print(k,"===.",v )
        elif type(datastr) == type(list()):
                if len(datastr) == 0:
                   datacollect = datacollect + '[]'
                else:
                    for item in datastr:
                         datacollect = datacollect + str(item) + r'<hr />'
                        
        else:
            datacollect = datacollect + str(datastr) 
                
                
        
        
        datatdfull = tdstr + "data" + tdend \
                + r'<td align="left" colspan ="5">' \
                + datacollect \
                + tdend

        trfull = trfull + trstr + datatdfull + tdend #完整的td标签
        
        tbstr = tbstr + trfull + tbend
        return tbstr
      
        
        
##    def getBaseURL(self,urlstr):
##        """ Return base url"""
##        Re = parse.urlparse(urlstr)
##        baseurl = Re.scheme  + "://" +Re.netloc + Re.path
##        return baseurl
##
##    def getEncodeParameters(self,urlstr):
##        """ Return Parameters """
##        Re = parse.urlparse(urlstr)
##        PsRe= urllib.parse.parse_qsl(Re.query)
##        params = PsRe.urlencode(PsRe)
##        return params
##
##    
##    def getRequest(self,urlstr):
##        """ Return  overwrite Request """
##        baseurl = getBaseURL(urlstr)
##        encodeparams = getEncodeParameters(urlstr)
##        req = request.Request(url = baseurl,data = encodeparams,method = 'GET')
##        return req

##    def getStatus(self,urlrequest):
##        """Return  http accwss status"""
##        f = urllib.request.urlopen(urlrequest)
##        return f.status
##
##    def getReason(self,urlrequest):
##        """Return  http accwss status"""
##        f = urllib.request.urlopen(urlrequest)
##        return f.reason
##    
##    def  getReturnVaile(self,urlrequest):
##        """Return  http accwss status"""
##        f = urllib.request.urlopen(urlrequest)
##        return f.read().decode('utf-8')

##if __name__ =='__main__':
##
##   handURL =  handleurl()
##   handURL.initTestArguments()
##   
