#coding=utf-8

import sys
import urllib
import urllib2
import re
import socket
import base64

class Crawl_helper_tools_url:

    url = ''
    root_url = ''
    page = 0
    count = 0

    def __init__(self,url,root_url):
        self.url = url
        self.root_url = root_url

    @staticmethod
    def getCurl(url,data = {},headers = {}):
        # data - dict
        if (not data):
            data = urllib.urlencode(data)
            url = url + '?' + data
        request = urllib2.Request(url, '', headers)
        try:
            response = urllib2.urlopen(request,timeout=2)
        except socket.timeout:
            print('except time time time time out')
            return 'fail'
        except Exception , e:
            print Exception,":",e
            print('except open URL time out')
            print('超时了')
            return 'fail'

        return  response.read()


    @staticmethod
    def postCurl(url,data = ''):
        # data - dict
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        return response.read()

    def parse_html_page_count(self,tree,xpath = '/html'):
        page_count_text = ''  # 85条  共9页
        nodes = tree.xpath(xpath)
        for node in nodes:
            page_count_text = node.text
        if(page_count_text == ''):
            print 'wrong page count parse exit'
            sys.exit()

        page_count_text = page_count_text.encode("utf-8")

        reg_page_count = re.findall(ur'([0-9]+)',page_count_text)
        if len(reg_page_count) >= 2:
            self.count = reg_page_count[0]
            self.page = reg_page_count[1]
        else:
            print '不能得到正确的页数'
            sys.exit()

        # count = int(page_count_text[1:3])
        # print count

        # reg_page_count = re.search(r'共([0-9]+)页',page_count_text)
        # print reg_page_count
        # print reg_page_count.group(1)
        # reg_page_count = re.findall(ur'([0-9]+)',page_count_text)
        # print reg_page_count
        # print reg_page_count[0]
        # print reg_page_count[1]

    @staticmethod
    def http_auth(username, password, url, data = {}, headers = {}):

        auth = base64.b64encode(username+ ':'+ password)
        headers["Authorization"] = "Basic "+ auth

        # data - dict
        data = urllib.urlencode(data)
        #req = urllib2.Request(url, data)
        req = urllib2.Request(url, data, headers)
        #response = urllib2.urlopen(req)
        try:
            response = urllib2.urlopen(req,timeout=5)
        except socket.timeout:
            #print('except time out')
            return 'fail'
        except Exception , e:
            #print Exception,":",e
            #print('except open URL time out')
            return 'fail'

        return response.read()

    @staticmethod
    def http_auth_handle_get_tag(url,data = {}):
        # data - dict
        if (data):
            data = urllib.urlencode(data)
            url = url + '?' + data
        try:
            response = urllib2.urlopen(url)
        except socket.timeout:
            # print('except time out')
            return 'fail'
        except Exception , e:
            # print Exception,":",e
            # print('except open URL time out')
            return 'fail'
        return  response.read()

    @staticmethod
    def http_auth_handle_create_tag(username, password, url, new_tag, headers = {}):

        auth = base64.b64encode(username+ ':'+ password)
        headers["Authorization"] = "Basic "+ auth

        # data - dict
        data = {"name":new_tag}
        data = urllib.urlencode(data)
        #req = urllib2.Request(url, data)
        req = urllib2.Request(url, data, headers)
        #response = urllib2.urlopen(req)
        try:
            response = urllib2.urlopen(req,timeout=5)
        except socket.timeout:
            #print('except time out')
            return 'fail'
        except Exception , e:
            #print Exception,":",e
            #print('except open URL time out')
            return 'fail'

        return response.read()


    def getPageTitleUrl(self,tree,xpath):
        nodes = tree.xpath(xpath)
        for node in nodes:
            # print self.root_url + node.attrib['href']
            return self.root_url + node.attrib['href']

    def getPageTitle(self,tree,xpath = '/html'):
        res = []
        nodes = tree.xpath(xpath)
        if(not nodes):
            print '没有内容'
        for node in nodes:
            j = 1
            for m in node.getchildren():
                url_nodes_xpath = xpath + '/div['+ str(j) +']/div[1]/h1/span/a'
                url_nodes = self.getPageTitleUrl(tree,url_nodes_xpath)
                res.append(url_nodes)
                j += 1

        return res

    def getCount(self):
        return self.count

    def getPage(self):
        return  self.page

    @staticmethod
    def testfunction(var):
        return var + 'test function'

    def test2(self):
        return  self.url
