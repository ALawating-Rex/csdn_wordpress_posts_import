#coding=utf-8

from tools import *
from lxml import etree
from bs4 import BeautifulSoup

class Crawl_helper_parse_page:

    url = ''
    html = ''
    title = ''
    tag = []
    content = ''

    def __init__(self,url):
        self.url = url

    def getText(self,elem):
        rc = []
        for node in elem.itertext():
            rc.append(node.strip())
        return ''.join(rc)

    def getTitle(self,url = '',data = {},headers = {}):
        print 'in function getTitle'
        print url
        if (self.html):
            response = self.html
        else:
            if (url):
                response = Crawl_helper_tools_url.getCurl(url,data,headers)
            else:
                response = Crawl_helper_tools_url.getCurl(self.url,data,headers)

        self.html = response
        # print(response)
        print 'start etree 2'
        tree = etree.HTML(self.html)
        xpath_title = '//*[@id="article_details"]/div[1]/h1/span/a'
        print 'start etree 3'
        node = tree.xpath(xpath_title)[0]
        print '文章标题是： '
        print self.getText(node)

        xpath_content = '//*[@id="article_content"]'
        node_content = tree.xpath(xpath_content)[0]
        print '文章内容是： '
        print self.getText(node_content)


        print node
        print node.itertext()
        print self.getText(node)
        print node.text
        print node.tag
        print node.attrib
        print node.getchildren()
        print '========'
        for i in node.getchildren():
            print i.text
            print i.tag
            print i.attrib
            print self.getText(i)
            print '++++++'
        sys.exit()
        return  'title'
        pass


    def getTitle_soup(self,url = '',data = {},headers = {}):
        print url
        if (self.html):
            response = self.html
        else:
            if (url):
                response = Crawl_helper_tools_url.getCurl(url,data,headers)
            else:
                response = Crawl_helper_tools_url.getCurl(self.url,data,headers)
        if(response == 'fail'):
            return 'FAIL'

        self.html = response
        soup = BeautifulSoup(self.html,"lxml")
        title_parent = soup.find("span","link_title").contents[0].contents
        # print(len(title_parent))

        '''
        title = soup.title.string
        print(title)
        '''

        if (len(title_parent) > 1):
            title = soup.find("span","link_title").contents[0].contents[2]
        else:
            title = soup.find("span","link_title").contents[0].contents[0]

        title = title.strip()
        return title
    def getTag(self,url = '',data = {},headers = {}):
        return ['tag1','tag2']
        pass

    def getTag_soup(self,url = '',data = {},headers = {}):
        if (self.html):
            response = self.html
        else:
            if (url):
                response = Crawl_helper_tools_url.getCurl(url,data,headers)
            else:
                response = Crawl_helper_tools_url.getCurl(self.url,data,headers)
        if(response == 'fail'):
            return 'FAIL'

        self.html = response
        soup = BeautifulSoup(self.html,"lxml")
        res_tags = []

        try:
            tags = soup.find("span","link_categories").contents
        except Exception , e:
            return []

        #print(tags)
        for tag_content in tags:
            if (tag_content.name == "a") and (tag_content.string != ""):
                res_tags.append(tag_content.string)

        #res_tags.append('from csdn')
        return  res_tags

    def getContent(self,url = '',data = {},headers = {}):
        return 'content'
        pass

    def getContent_soup(self,url = '',data = {},headers = {}):
        if (self.html):
            response = self.html
        else:
            if (url):
                response = Crawl_helper_tools_url.getCurl(url,data,headers)
            else:
                response = Crawl_helper_tools_url.getCurl(self.url,data,headers)
        if(response == 'fail'):
            return 'FAIL'

        self.html = response
        soup = BeautifulSoup(self.html,"lxml")
        contents = soup.find("div","article_content")

        return  contents

