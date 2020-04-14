# -*- coding: utf-8 -*-
import json

import scrapy
import re
import urllib
from twitterSpider.items import TwitterspiderImgItem, TwitterspiderVideoItem
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')
sys.setrecursionlimit(1000000)


class TwitterSpider(scrapy.Spider):
    name = 'twitter'
    allowed_domains = ['twitter.com']
    start_urls = "https://twitter.com/{}"

    # 初始化Item
    twitterimgItem = TwitterspiderImgItem()
    twittervideoItem = TwitterspiderVideoItem()

    # 翻页所需数据
    init_max_position = ''

    # 请求头所需数据
    authorization = "Bearer AAAAAAAAAAAAAAAAAAAAAPYXBAAAAAAACLXUNDekMxqa8h%2F40K4moUkGsoc%3DTYfbDKbT3jJPCEVnMYqilB28NHfOPqkca3qaAxGfsyKCs0wRbw"
    User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36x-csrf-token: c92e7921d5d4bd7f143fef205256a097"

    guest_token = ""
    count = 1

    # 开始爬虫
    def start_requests(self):

        header_withoutcookie = {
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding" : "gzip, deflate, br",
            "accept-language" : "zh-CN,zh;q=0.9",
            "upgrade-insecure-requests" : "1",
            "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
        }

        # headers = {
        #     'cookies': self.cookie,
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        #     'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, * / *;q = 0.8',
        #     'Host': 'twitter.com',
        #     'Accept-Language': 'zh-cn',
        #     'Accept-Encoding': 'br, gzip, deflate',
        #     'Referer': 'https://twitter.com/ygofficialblink',
        #     'Connection': 'keep-alive'
        # }
        #cookie = {i.split("=")[0]: i.split("=")[1] for i in cookie.split('; ')}
        # Request 是Scrapy发送GET请求的方法

        header_guest = {
            "authorization": self.authorization,
            "User-Agent": self.User_Agent
        }

        # 发送POST请求获取guest数值
        yield scrapy.FormRequest(
            url="https://api.twitter.com/1.1/guest/activate.json",
            method='POST',
            headers=header_guest,
            callback=self.get_guest_token
        )

        User_Group = [
            "BTS_twt",
            "realDonaldTrump",
            "ygofficialblink",
            "jnloops"

        ]
        for name in User_Group:
            yield scrapy.Request(
                url=self.start_urls.format(name),
                headers=header_withoutcookie,
                callback=self.parse_deal

            )

    # 处理首页数据
    def parse_deal(self, response):
        init_max_position = response.xpath('//div[@class = "stream-container  "]/@data-max-position').extract_first().decode('utf-8')
        img_nodes = response.xpath('//div[@class = "AdaptiveMedia-photoContainer js-adaptive-photo "]/@data-image-url | //div[@class = "QuoteMedia-photoContainer js-quote-photo"]/@data-image-url').extract()  # 提取本页图片链接
        video_background = response.xpath('//div[@class = "PlayableMedia-container"]').re('https://pbs.twimg.com/.*\.jpg')
        uid = response.xpath('//span[@class = "username u-dir"]/b/text()').extract_first().decode('utf-8')
        print uid

        for i in range(len(img_nodes)):
            self.twitterimgItem['uid'] = uid
            self.twitterimgItem['img_url'] = img_nodes[i]
            self.twitterimgItem['video_img_url'] = None
            yield self.twitterimgItem

        for i in range(len(video_background)):
            self.twitterimgItem['uid'] = uid
            self.twitterimgItem['img_url'] = None
            self.twitterimgItem['video_img_url'] = video_background[i]
            yield self.twitterimgItem

        content_list = response.xpath('//li[@data-item-type = "tweet"]')
        a = content_list.extract()
        for i in range(len(a)):
            if re.findall(r'PlayableMedia-player', a[i]):
                video_id = content_list.xpath('./@data-item-id').extract()
                video_id = video_id[i].decode('utf-8')
                yield self.get_video_json(video_id)
            else:
                pass

        yield self.page_page(init_max_position)

    # 爬取下一页，并将返回传给处理非首页的
    def page_page(self, max_position):
        data = {
            "include_available_features": '1',
            "include_entities": '1',
            "max_position": max_position,
            "reset_error_state": 'false',
        }
        params = urllib.urlencode(data)

        url = 'https://twitter.com/i/profiles/show/{}/timeline/tweets?' + params
        return scrapy.Request(url.format("BTS_twt"), callback=self.parse_more)

    # 处理第一页往后的json数据
    def parse_more(self, response):
        res = json.loads(response.text)
        has_more_items = res['has_more_items']
        min_position = res['min_position']

        selector = scrapy.Selector(text=res['items_html'], type="html")
        msg_nodes = selector.xpath('//div[@class = "AdaptiveMedia-photoContainer js-adaptive-photo "]/@data-image-url | //div[@class = "QuoteMedia-photoContainer js-quote-photo"]/@data-image-url').extract()  # 提取本页图片链接
        video_background = selector.xpath('//div[@class = "PlayableMedia-container"]').re('https:.*jpg')
        uid = response.xpath('//span[@class = "username u-dir"]/b/text()').extract_first().decode('utf-8')
        for i in range(len(msg_nodes)):
            self.twitterimgItem['uid'] = uid
            self.twitterimgItem['img_url'] = msg_nodes[i]
            self.twitterimgItem['video_img_url'] = None

            yield self.twitterimgItem

        for i in range(len(video_background)):
            self.twitterimgItem['uid'] = uid
            self.twitterimgItem['video_img_url'] = video_background[i]
            self.twitterimgItem['img_url'] = None

            yield self.twitterimgItem

        content_list = selector.xpath('//li[@data-item-type = "tweet"]')
        a = content_list.extract()
        for i in range(len(a)):
            if re.findall(r'PlayableMedia-player', a[i]):
                video_id = content_list.xpath('./@data-item-id').extract()
                video_id = video_id[i].decode('utf-8')
                yield self.get_video_json(video_id)
            else:
                pass

        if self.count < 5:
            if has_more_items:
                self.count += 1
                yield self.page_page(min_position)

    # 获取爬json文件所需要的header值：x-guest-token
    def get_guest_token(self, response):

        guest_token = response.text.split('\"')[3]
        self.guest_token = guest_token

    # 爬取包含有视频链接的json文件
    def get_video_json(self, video_id):
        url = "https://api.twitter.com/1.1/videos/tweet/config/{}.json"
        url = url.format(video_id)

        header = {
            "authorization" : self.authorization,
            "User-Agent" : self.User_Agent,
            "x-guest-token" : self.guest_token
        }

        return scrapy.Request(url, headers=header, callback=self.get_video_url)

    # 从json文件中获取playbackUrl
    def get_video_url(self, response):
        text = json.loads(response.text)
        self.twittervideoItem['video_url'] = text['track']['playbackUrl']
        self.twittervideoItem['GK'] = None
        yield self.twittervideoItem


""" cookie 处理 

    cookie = ''
    cookie_list = ''
    def __init__(self):
        cookies = {}
        for line in self.cookie.split(';'):
            key, value = line.split('=', 1)
            cookies[key] = value
        self.cookie_list = cookies   
        
"""




