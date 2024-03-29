# -*- coding: utf-8 -*-
import base64
import random

import scrapy
from functools import partial
import re

from scrapy import Request
from scrapy_splash import SplashRequest

from ZLSchool import ZlschoolItem
from ZLSchool.settings import USER_AGENT_POOL
from datetime import datetime

regSpace = re.compile(r'([\s\r\n\t])+')


def extract_info(response, xp):
    return response.xpath(xp).extract()

def parse_time(time_str):
    time = datetime.strptime(time_str,"%Y-%m-%d")
    return time.strftime("%Y-%m-%d")

# 去掉多余的符号
def replace_all_n(text):
    # 以防止提取不到
    try:
        if type(text) == str:
            rel = re.sub(regSpace, "", text)
            return rel
        elif type(text) == list:
            return "".join([re.sub(regSpace, "", t) for t in text])
    except TypeError as e:
        return "空"


class ZlSpider(scrapy.Spider):
    name = 'zl'
    allowed_domains = ['zhaopin.com']
    COMMON_HEADER = {
        "User-Agent": random.choice(USER_AGENT_POOL),
        "Referer": "https://www.zhaopin.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    base_url = ["https://xiaoyuan.zhaopin.com/full/0/489_0_0_0_1_-1_0_{pn}_0",
                "https://xiaoyuan.zhaopin.com/part/0/489_0_0_0_1_-1_0_{pn}_0"]

    def start_requests(self):
        # 获取共有多少页
        for url in self.base_url:
            yield Request(
                url=url.format(pn="1"),
                headers=self.COMMON_HEADER,
                callback=self.get_total_page_and_start,
                meta={"url": url}
            )

    def get_total_page_and_start(self, response):
        total_page_num = extract_info(response, "//span[@class='searchResultPagePer fr']/text()")[0][1:]
        for page_num in range(1, int(total_page_num) + 1):
            yield Request(
                url=response.meta['url'].format(pn=page_num),
                headers=self.COMMON_HEADER,
                callback=self.get_data
            )

    def get_data(self, response):
        extract = partial(extract_info, response)
        item = ZlschoolItem()
        item['link'] = list(map(lambda x: "https:" + x, extract("//p[@class='searchResultJobName']/a[1]/@href")))
        item['job_name'] = extract('//p[@class="searchResultJobName clearfix"]/a/text()')
        item['place'] = extract(
            "//div[@class='searchResultItemSimple clearfix ']//em[@class='searchResultJobCityval']/text()")
        item['company_name'] = extract(
            "//div[@class='searchResultItemSimple clearfix ']//p[@class='searchResultCompanyname']//text()")
        info = response.xpath("//p[@class='searchResultCompanyInfodetailed']")
        info = list(map(lambda x: x.xpath(".//em/text()").extract(), info))
        item['company_nuture'] = list()
        item['company_size'] = list()
        item['company_industry'] = list()
        item['job_kind'] = list()
        item['job_number'] = list()
        try:
            for i in info:
                if len(i) == 3:
                    item['company_industry'].append(i[0])
                    item['job_kind'].append(i[1])
                    item['job_number'].append(i[2])
                    item['company_nuture'].append("空")
                    item['company_size'].append("空")
                elif len(i) == 5:
                    item['company_nuture'].append(i[0])
                    item['company_size'].append(i[1])
                    item['company_industry'].append(i[2])
                    item['job_kind'].append(i[3])
                    item['job_number'].append(i[4])
                else:
                    item['company_industry'].append("空")
                    item['job_kind'].append(i[0])
                    item['job_number'].append(i[1])
                    item['company_nuture'].append("空")
                    item['company_size'].append("空")
        except:
            # from scrapy.shell import inspect_response
            # inspect_response(response, self)
            pass
        item['id'] = [base64.b32encode((n + c).encode("utf-8")).decode("utf-8") for n, c in
                      zip(item['job_name'], item['company_name'])]
        all_data = [{key: item[key][index] for key in item.keys()} for index in range(len(item['id']))]
        for data in all_data:
            yield SplashRequest(
                url=data['link'],
                meta={"item": data},
                callback=self.get_other,
                # headers=self.COMMON_HEADER,
                args={'wait': 3,'images': 0,}
            )

    def get_other(self, res):
        item = ZlschoolItem(res.meta['item'])
        extract = partial(extract_info, res)
        item['post_time'] = parse_time(extract("//span[@class='time']/text()")[0])
        item['job_place'] = replace_all_n(extract("string(//span[@class='address'])")[0])
        item['job_nature'] = replace_all_n(extract("string(//span[@class='position-type'])")[0])
        company_address = extract("string(//p[@class='company-location commonStyle'])")
        item['company_address'] = replace_all_n(company_address) if len(company_address) != 0 else "空"
        item['job_content'] = replace_all_n("".join(extract("string(//div[@class='describe'])")))
        education = extract("string(//span[@class='edu-level'])")
        item['education'] = replace_all_n(education[0]) if len(education) != 0 else "空"
        company_page = extract("string(//p[@class='company-domain commonStyle'])")
        item['company_homepage'] = replace_all_n(company_page) if len(company_page) != 0 else "空"
        yield item
