#coding=utf-8
import sys
# import urllib
# import urllib2
# import cookielib
from helper.tools import *
from helper.parse_page import *
from lxml import etree
import json

# todo 尝试使用 scrapy

reload(sys)
sys.setdefaultencoding('utf8')
sys.setrecursionlimit(2000)

wp_url = "http://127.0.0.1/myaliyun/share345/trunk/share345/wp-json/wp/v2/posts"
wp_url_tags = "http://127.0.0.1/myaliyun/share345/trunk/share345/wp-json/wp/v2/tags"
username = "simael"
password = "123456"
# ready_cate_id = "4"
ready_cate_id = "11"
wp_data = {}
wp_headers = {}
old_tags = {}

# todo 先获取所有的 old tags
res_old_tags = Crawl_helper_tools_url.http_auth_handle_get_tag(wp_url_tags,wp_data)
if (res_old_tags == "fail"):
    print('获取标签失败')
    sys.exit()
decode_res_tags = json.loads(res_old_tags)
for res_tag in decode_res_tags:
    old_tags[res_tag['name']] = res_tag['id']
print('已经存在的标签列表：')
print(old_tags)

url = 'http://blog.csdn.net/m0sh1'
root_url = 'http://blog.csdn.net'
# var = 'this is a var in'
# print(Crawl_helper_tools_url.testfunction(var))

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer' : 'http:www.baidu.com'}

crawl_url = Crawl_helper_tools_url(url,root_url)
html = crawl_url.getCurl(url,{},headers)
# print html
if html == '' or html == 'None':
    print '读取 html 失败'
    sys.exit()

# print html

tree = etree.HTML(html)
crawl_url.parse_html_page_count(tree,'//*[@id="papelist"]/span')
# 多线程  一页一个线程 还是一个链接一个线程
# 链接类似：  http://blog.csdn.net/m0sh1/article/list/1  1表示第一页
count = crawl_url.getCount()
page = crawl_url.getPage()
i = 1


#   TODO 每页创建 一个线程
#   TODO 分析每页循环取出每篇文章的内容等

while(i <= int(page)):
    # http://blog.csdn.net/m0sh1/article/list/1
    next_page_url = url + '/article/list/' + str(i)
    # 重新获取 新的 tree

    # next_page_crawl_url = crawl_url
    # TODO 上面一行是测试代码 下面的三行才是每次循环取出来的真正的HTML页面
    next_page_crawl_url = Crawl_helper_tools_url(next_page_url,root_url)

    try:
        next_page_html = next_page_crawl_url.getCurl(next_page_url,{},headers)
    except Exception , e:
        print 'except 读取某一页异常....',e
        continue

    next_page_tree = etree.HTML(next_page_html)

    # next_page_tree = tree
    i += 1
    print(next_page_url)
    # TODO 置顶的文章不需要读取  在后面页码中还会有真和谐文章的
    top_page_list = next_page_crawl_url.getPageTitle(next_page_tree,'//*[@id="article_toplist"]')
    if(top_page_list):
        pass
        # print len(top_page_list)
        # print top_page_list
    else:
        print '没有文章哦'

    page_list = next_page_crawl_url.getPageTitle(next_page_tree,'//*[@id="article_list"]')
    if(page_list):
        pass
        # print len(page_list)
        # print page_list
    else:
        print '没有文章哦'
    real_page_list_len = len(top_page_list) + len(page_list)
    real_page_list = top_page_list + page_list
    print real_page_list_len
    print real_page_list
    for n in real_page_list:
        try:
            print n
            parse_page = Crawl_helper_parse_page(n)
            try:
                page_title = parse_page.getTitle_soup(n,{},headers)
                if(page_title == "FAIL"):
                    print(n + "超时了 下一条数据")
                    continue
                print page_title
            except Exception , e:
                print 'except 标题异常....',e
                continue

            try:
                page_tags = parse_page.getTag_soup(n,{},headers)
                print '此文章的 tags 是：'
                print page_tags
                #todo 处理 tags
                for i_page_tag in page_tags:
                    if old_tags.has_key(i_page_tag):
                        print('tag 存在')
                        print(old_tags[i_page_tag])
                    else:
                        print('tag 不存在')
                        print(i_page_tag)
                        #todo 不存在创建tag
                        res = Crawl_helper_tools_url.http_auth_handle_create_tag(username,password,wp_url_tags,i_page_tag,wp_headers)
                        if (res != "fail"):
                            decode_res_create_tag = json.loads(res)
                            old_tags[i_page_tag] = decode_res_create_tag[u'id']

                print('old tags 更新为:')
                print(old_tags)
            except Exception , e:
                print 'except 标签异常....',e
                continue

            try:
                page_content = parse_page.getContent_soup(n,{},headers)
                #print page_content
            except Exception , e:
                print 'except 内容异常....',e
                continue

            # page_cates = next_page_crawl_url.getCates()

            page_content = str(page_content) + "<br><p>此文章通过 python 爬虫创建，原文是自己的csdn 地址: <a target=\"_blank\" href=\"" + str(n) + "\">" + page_title + "</a></p><br>"

            wp_data['status'] = "publish"
            wp_data['title'] = page_title
            wp_data['content'] = page_content
            wp_data['author'] = 1
            wp_data['slug'] = n[-8:]
            wp_data['categories[0]'] = ready_cate_id

            for tag_i in range(len(page_tags)):
                print(page_tags[tag_i])
                wp_data["tags["+str(tag_i)+"]"] = old_tags[page_tags[tag_i].decode('utf-8')]

            # todo 爬虫 添加至 github
            # todo 源代码 带有 script 在 wp中显示有问题

            # print('创建文章 参数')
            # print(wp_data)
            res = Crawl_helper_tools_url.http_auth(username,password,wp_url,wp_data,wp_headers)
            if (res == "fail"):
                print("添加失败")
            # sys.exit()

        except Exception , e:
            print 'except 某篇文章出错....',e
            continue
