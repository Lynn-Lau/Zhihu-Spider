# -*- coding: utf-8 -*-
__author__ = 'Lynn'

#############################################
# 利用Scrapy自带的框架进行模拟登录
# 登录网站 知乎:http://www.zhihu.com/#signin
#
# Author : Lynn Lau
# Language : Python 2.7.10 with Scrapy
# Editor : Pycharm 4.5
# Version : 3.1
# Date : 2015\10\27
##############################################

from scrapy.contrib.spiders import CrawlSpider ,Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request,FormRequest
from zhihu1.items import Zhihu1Item


class ZhihuSpider(CrawlSpider):

    # 爬虫的名字，允许的域名，起始地址
    name = "zhihu1"
    allowed_domains = ["zhihu.com"]
    start_urls=[
        "http://zhihu.com"
    ]

    # 抓取规则，通过正则表达式选取可以跟进抓取的网页规则
    # 此处规定的跟进用户的主页
    rules = (
        Rule(SgmlLinkExtractor(allow=('/people/.*')),callback='parse_page',follow=True),
        # Rule(SgmlLinkExtractor(allow=('/question/\d+',)),callback='parse_page',follow=True),
    )

    # 将源代码伪装成为浏览器，headers伪装
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "http://www.zhihu.com/"
    }

    # 保存网站的cookie,完成后调用post_login函数
    def start_requests(self):
        return [Request("http://www.zhihu.com/#signin", meta={'cookiejar':1}, callback=self.post_login)]

    # 登录函数
    def post_login(self,response):
        print 'Preparing login'

        # 在返回的html代码中抓取xsrf验证机制字段，并进行打印
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()
        print xsrf

        # FormRequest.from_response()函数是scrapy框架自带的函数，用于请求登录表单
        # 请求登录表单后将需要填写的内容填写之后，调用after_login函数
        return [
            FormRequest.from_response(response,
                                      # meta 函数是对cookie获取，用于被跟踪
                                      meta = {'cookiejar' : response.meta['cookiejar']},
                                      # headers 伪装
                                      headers = self.headers,
                                      # 将验证机制，email,password 填写进去
                                      formdata = {
                                          'xsrf' : xsrf,
                                          'email' : 'Your E-mail',
                                          'passsword' : 'Your Password',
                                      },
                                      # 调用after_login函数
                                      callback = self.after_login,

                                      dont_filter = True
                                      )
        ]

    def after_login(self,response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)


    def parse_page(self, response):
        problem = Selector(response)
        item = Zhihu1Item()

        # 下面模块为抓取的主要信息
        # 用户个人主页链接URL
        item['url'] = response.url
        # 用户名
        item['name'] = problem.xpath('//div[@class="top"]/div[@class="title-section ellipsis"]/span[@class="name"]/text()').extract()
        # 在知乎获得赞同数
        item['agree'] = problem.xpath('//span[@class="zm-profile-header-user-agree"]/strong/text()').extract()
        # 在知乎获得的感谢数
        item['thanks'] = problem.xpath('//span[@class="zm-profile-header-user-thanks"]/strong/text()').extract()
        # 受教育经历
        item['education'] = problem.xpath('//span[@class="info-wrap"]/span[@class="education item"]/a/text()').extract()
        # 用户所在地
        item['location'] = problem.xpath('//span[@class="info-wrap"]/span[@class="location item"]/a/text()').extract()
        # 用户的行业
        item['business'] = problem.xpath('//span[@class="info-wrap"]/span[@class="business item"]/a/text()').extract()
        # 用户所在的公司
        item["employment"] = problem.xpath('//span[@class="info-wrap"]/span[@class="employment item"]/a/text()').extract()
        # 获取该用户关注&被关注的人数
        item['follow'] = problem.xpath('//div[@class="zu-main-sidebar"]/div[@class="zm-profile-side-following zg-clear"]/a[@class="item"]/strong/text()').extract()
        # 获取该用户的提问数、回答数、专栏数
        item['AskAswClu'] = problem.xpath('//div[@class="zm-profile-header"]/div[@class="profile-navbar clearfix"]/a[@class="item "]/span/text()').extract()




        if len(item['agree'])==0:
            pass
        elif len(item['name'])!=0:
            yield item
        # else:
            # yield item


        '''
        for number in item['agree']:
            if int(number)<10:
                pass
            elif len()


        for mingzi in item['name']:
            if len(mingzi) !=0:
                yield item
            else:
                pass
                '''
        # print

        # item['title'] = problem.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
        # item['description'] = problem.xpath('//div[@class="zm-editable-content"]/text()').extract()
        # item['answer'] = problem.xpath('//div[@class=" zm-editable-content clearfix"]/text()').extract()
        # return item