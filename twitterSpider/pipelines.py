# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import os
import settings
import MySQLdb
from items import TwitterspiderVideoItem, TwitterspiderImgItem


class TwitterspiderPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = MySQLdb.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='twitter',  # 数据库名
            user='root',  # 数据库用户名
            passwd='WpQP>yYAF190',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # create = """create database if not exists twitter"""
        # delete = """delete * from twitter"""
        # self.cursor.execute(create)
        # self.cursor.execute(delete)



        # item里面定义的字段和表字段对应
        if isinstance(item, TwitterspiderImgItem):

            """ 下载用户发布推文图片 """

            dir_path = '%s/%s' % (settings.IMAGES_STORE, 'img')
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            image_url = item['img_url']
            img_list_name = image_url.split('/')

            img_name = img_list_name[4]  # 图片名称

            file_path = '%s/%s' % (dir_path, img_name)

            if os.path.exists(img_name):
                pass
            else:
                with open(file_path, 'wb') as file_writer:
                    conn = requests.get(image_url)  # 下载图片
                    file_writer.write(conn.content)
                file_writer.close()

            """ 下载视频背景图 """

            dir_path = '%s/%s' % (settings.IMAGES_STORE, 'video_img')
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            video_img_url = item['video_img_url']
            if video_img_url:
                video_img_list_name = video_img_url.split('/')
                video_img_name = video_img_list_name[4]  # 图片名称
                if video_img_name.find('jpg') > 0:
                    VI_file_path = '%s/%s' % (dir_path, video_img_name)
                else:
                    VI_file_path = '%s/%s%s' % (dir_path, video_img_name, ".jpg")

                if os.path.exists(video_img_name):
                    pass
                else:
                    with open(VI_file_path, 'wb') as file_writer:
                        conn = requests.get(video_img_url)  # 下载图片
                        file_writer.write(conn.content)
                    file_writer.close()

            """ 将链接保存至数据库 """

            self.cursor.execute(
                """insert into twitterImg(img_url, video_img_url, uid)
                values (%s, %s, %s)""",
                (
                 item['img_url'],
                 item['video_img_url'],
                 item['uid']))

        if isinstance(item, TwitterspiderVideoItem):
            self.cursor.execute(
                """insert into twitterVideo(video_url, GK)
                values (%s, %s)""",
                (item['video_url'],
                 item['GK'])
            )

        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回