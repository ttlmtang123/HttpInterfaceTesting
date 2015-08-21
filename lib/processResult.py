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

class  processResult:
    #XML file path
    logfile= ""
    newlines = [] # 保存html内容
    
    itemstr = ""
    
    #result log file

    def __init__(self):

        super()
    def __del__(self):
        print("Call del function")

        
    def checkFile(self,filepath):
        """ this function wil check thie tet file exist or not"""
        if os.path.lexists(filepath):
            print ("[OK] test target is exist, continue")
            return True
        else:
            print("[Error] Target is not exist!!!")
            return False

    def getResultFile(self):
        """  return result file path """
        extensiontype = ".html"
        #fileName = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        #fileName = self.basedir + fileName + extensiontype
        self.logfile = os.path.normcase(os.getcwd() + os.sep + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime()) + extensiontype)
        
        print ("[Process] create log file",self.logfile )
       
        try:
            with open(self.logfile, 'w') as file:
                file.write('')
            file.close()

            if os.path.lexists(self.logfile):
                print ("[OK] Create log file completed")
                return os.path.normcase(self.logfile)
            else:
                print("[Failed] reatel og file completed!!")
                
        except FileExistsError:
            print(sys.exc_info()[2])

        return None
    
    def generationHTMLHeadString(self):
        """  retrurn String  as the html hand"""
##        strHTML ='<head>'
##                +'<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />'
##                + '<Title> 量邦软件URL测试结果报告</tilte>' 
##                + '</head>'    
##
##        table formant
##         -----------------------------------------------
##          ||协议 ||券商 ||链接地址 || 状态  || 结果 || 返回值 ||
##          -----------------------------------------------
##       更新时间  
##        table formant
##         -----------------------------------------------------------
##          ||协议 ||券商 ||链接地址 ||  耗时(毫秒)   ||状态  || 结果 || 返回值 ||
##          -----------------------------------------------------------
        self.newlines.append(r'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
        self.newlines.append(r'<html xmlns="http://www.w3.org/1999/xhtml">')
        self.newlines.append(r'<head>')
        self.newlines.append(r'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
        self.newlines.append(r'<title> 量邦软件URL测试结果报告 </title>')
        self.newlines.append(r'<style type="text/css">')
        self.newlines.append(r'body {background-color: #F7F8E0}')
##        self.newlines.append(r'body {background-color: ##eff9e5}')
        self.newlines.append(r'h1{color:#00F}')
        self.newlines.append(r'</style>')                     
        self.newlines.append(r'</head>')
        self.newlines.append(r'<body>')
        self.newlines.append(r'<h1> 量邦软件URL测试结果报告-</h1>')
        self.newlines.append(r'<p>')
       
        #self.newlines.append(r'<h1>测试结果</h1>')
        self.newlines.append (r'<h1> 测试时间：' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime()) + r'</h1>')
##        self.newlines.append(r'<font size="+1">')
        self.newlines.append(r'<font size="4">')
        self.newlines.append(r'<table border="1">')
        self.newlines.append(r'<tr><th>协议</th><th>测试对象</th><th>链接地址</th><th>耗时(毫秒)</th><th>状态</th><th>结果</th><th>返回值</th></tr>')                
                       

    def appendhtmltag(self,appStr):
        self.newlines.append(appStr)
        
    def getHtmlEnd(self):
        endhtmlScreen = r'</table>'\
                    + r'</font>'\
                    + r'</p>'\
                    + r'<p>'\
                    + r'</body>'\
                    + r'</html>'
        return endhtmlScreen                      

    


    def SetHtmlTestInfo(self,strtype="http", account="none",keyword="none", linkURL="none",strtime="0", httpstatus="N/A", httpreason="none",httpresponseValue="none"):

        tdTagStart = r'<td align="center" bgcolor="#CEF6CE">'
        tdTagEnd = r'</td>'
        
        self.itemstr = r'<tr>' \
                       + tdTagStart + str(strtype) + tdTagEnd \
                       + tdTagStart + str(account) + tdTagEnd \
                       + r'<td  align="center" bgcolor="#CEF6CE"> <a target="_blank" href="' \
                       + str(linkURL) + r'">' \
                       + str(keyword) + r'</a></td>'\
                       + tdTagStart + str(strtime) + tdTagEnd \
                       + tdTagStart + str(httpstatus) + tdTagEnd \
                       + tdTagStart + str(httpreason) + tdTagEnd \
                       + tdTagStart + str(httpresponseValue) + tdTagEnd \
                       +'</tr>'
        
                       
    #def writeResultHand(self,targetfile,htmlContent):
    def writeResultToFile(self,targetfile): 
##        with open(targetfile,'w') as file:
##             file.write(htmlContent)
##        file.close()
        
        with open(targetfile, 'w',encoding="utf-8") as f:
            for line in self.newlines:
##                print(line)
                f.write(line)
   
