# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field

class Zhihu1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 知乎用户的个人主页链接
    url = Field()

    # 知乎用户的用户名
    name = Field()

    # 知乎用户获得的赞的总数
    agree = Field()

    # 知乎用户的个人签名
    title = Field()

    # 知乎用获得感谢的次数
    thanks = Field()

    # 知乎用户的所在地
    location = Field()

    # 接受教育的学校
    education = Field()

    # 用户工作行业
    employment = Field()

    # 用户工作的公司
    business = Field()

    # 用户关注和被关注的人数
    follow = Field()

    # 提问、回答、专栏分别的书数量
    AskAswClu = Field()

