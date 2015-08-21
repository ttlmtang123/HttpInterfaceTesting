# -*- coding: utf-8 -*-
##  时间: 2015-02-13
##  跟新内容：
##  增加URL请求时间计算
##  时间: 2015-04-01
##  跟新内容：
##  将指定的测试文件名写入配置文件中，同时增加一个获取当前路径的类
##

from pathlib import Path
import json
import io
import sys
import traceback
import os
import os.path
import  time
import gc


sys.path.append(os.path.join(os.path.dirname(__file__),r'lib'))
from handleurl import handleurl
from processResult import processResult

class runTest(object):


    def __init__(self):
        super()

    def __del__(self):

        print('Class runTest delet')

    def getFolderPath(self):
        """ 返回当骨主文件所在的目录 """
        
    def looprun(self):

        count = 0
        while (count < 2):
            self.main()
            count= count +1
        
    def main(self):
        #启动 GC
        gc.enable() 
        instance  = processResult()
        instance.getResultFile()
        instance.generationHTMLHeadString() #末追加前
    
        parseXMLURL = handleurl()

        parseXMLURL.initTestArguments()#将所有的类变量 取出

        for i in range(len(parseXMLURL.urllinks)):

            #ulrtype = parseXMLURL.URLTypes[i]
            #print("url类型： ",parseXMLURL.URLTypes[i])
            brokername =  parseXMLURL.brokernames[i]
            urllink = parseXMLURL.urllinks[i]

            ulrtype = parseXMLURL.getURLType(urllink)
            print("url类型： ",ulrtype)
            ##print(urllink)
            keyword = parseXMLURL.URLSubNames[i]
            baseurl= parseXMLURL.getBaselink(urllink)
            params = parseXMLURL.getparams(urllink)
            #print(params)
        
            #Date:2015-02-27
            #Notes:增加异常处理
            try:
                parseXMLURL.PrpcesshttpRequest(baseurl,params)
            
                httpStatus = parseXMLURL.httpstatus
                httpReason = parseXMLURL.httpreason
                urltooktime = parseXMLURL.urltaketime
                Rvaule = parseXMLURL.httpReturnValue

                instance.SetHtmlTestInfo(ulrtype, brokername,keyword, urllink,urltooktime, httpStatus,httpReason,Rvaule)
                instance. appendhtmltag(instance.itemstr)
                ##休息1s
                time.sleep(1)
            except Exception:
                print("Exception in user code:")
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)

                #发生错误，返回值为零，code 继续执行    
                httpStatus = 0
                httpReason = ''
                urltooktime = 0
                Rvaule = {}

                instance.SetHtmlTestInfo(ulrtype, brokername,keyword, urllink,urltooktime, httpStatus,httpReason,Rvaule)
                instance. appendhtmltag(instance.itemstr)
       
                
        instance.appendhtmltag(instance.getHtmlEnd())#追加完成
        instance.writeResultToFile(instance.logfile)
        ## 删除所有的记录数据
        instance.itemstr="" 
        instance.newlines.clear() 
        instance = None  
if __name__ =='__main__':


    runtest = runTest()
    runtest.main()
