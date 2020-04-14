# -*- coding: utf-8 -*-
import requests
import os
import re

#下载视频


header = {"user-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

m3u8 = 'https://video.twimg.com/ext_tw_video/1134172704142233600/pu/pl/cbzu0Sm4JxBpf2Qn.m3u8?tag=9'

def gen_url():
    response = requests.get(m3u8, headers=header)

    response = response.text

    m3u8_2 = response.split('ext_tw_video')[-1]

    gen_m3u8_url = 'https://video.twimg.com/ext_tw_video' + m3u8_2

    print gen_m3u8_url

    gen_ts_url(gen_m3u8_url)

def gen_ts_url(m3u8url):

    response_ts = requests.get(url=m3u8url)

    print response_ts.content

    regex = re.compile("/ext_tw_video/.*\.ts")

    result = regex.findall((response_ts.content))

    print result[0]

    root = "/Users/jiang/Pictures/video/"

    if not os.path.exists(root):
        os.mkdir(root)

    if os.path.exists(root):
        length = len(result)
        for i in range(length):
            tsname = str(i) + ".ts"  #result[i].split('/')[-1]
            path = root + tsname
            r = requests.get('https://video.twimg.com' + result[i])
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print('\r' + tsname + " -->OK ({}/{}){:.2f}%".format(i, length, i*100/length))


if __name__ == '__main__':
    gen_url()

#
#     def downloader(url,path):
#         # 整合所有ts文件，保存为mp4格式
#         def tsToMp4():
#             print("开始合并...")
#             root = "D://mp4//"
#             outdir = "output"
#             os.chdir(root)
#             if not os.path.exists(outdir):
#                 os.mkdir(outdir)
#             os.system("copy /b *.ts new.mp4")
#             os.system("move new.mp4 {}".format(outdir))
#             print("结束合并...")