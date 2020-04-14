# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TwitterspiderImgItem(scrapy.Item):
    # define the fields for your item here like:
    img_url = scrapy.Field()
    video_img_url = scrapy.Field()
    uid = scrapy.Field()


class TwitterspiderVideoItem(scrapy.Item):
    # define the fields for your item here like:
    video_url = scrapy.Field()
    GK = scrapy.Field()
    # uid = scrapy.Field()





