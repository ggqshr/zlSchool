# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZlschoolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()  # 由工作名+公司名 生成的base32编码
    link = scrapy.Field()  # //p[@class='searchResultJobName']/a[1]/@href
    job_name = scrapy.Field()  # //p[@class="searchResultJobName clearfix"]/a/text()
    # salary = scrapy.Field() # 暂无
    place = scrapy.Field()  # //div[@class='searchResultItemSimple clearfix ']//em[@class='searchResultJobCityval']
    company_name = scrapy.Field()  # //div[@class='searchResultItemSimple clearfix ']//p[@class='searchResultCompanyname']
    # //p[@class='searchResultCompanyInfodetailed
    company_nuture = scrapy.Field()  # .//em/text() [0]
    company_size = scrapy.Field()  # .//em/text() [1]
    company_industry = scrapy.Field()  # .//em/text() [2]
    job_kind = scrapy.Field()  # .//em/text() [3]
    job_number = scrapy.Field()  # .//em/text() [4]

    # 深一层页面
    post_time = scrapy.Field()  # //li[@id='liJobPublishDate']/text()
    job_place = scrapy.Field()  # //li[@id='currentJobCity']/@title
    job_nature = scrapy.Field()  # //li[@class='cJobDetailInforWd2 marb'][5]
    company_address = scrapy.Field()  # //div[@class='cRightTab mt20']/div[@class='clearfix p20']/p[1]/text() # 可能为空，且需要去除特殊符号
    job_content = scrapy.Field()  # //div[@class='j_cJob_Detail']//p/text() 是一个列表
    education = scrapy.Field()  # //li[@class='cJobDetailInforWd2 marb'][6]
    company_homepage = scrapy.Field()  # //div[@class='cRightTab mt20']/div[@class='clearfix p20']/p[2]/a/text()
    # experience = scrapy.Field() # 暂无
    # advantage = scrapy.Field() # 暂无
