# 抓取链接 baseurl: 开始链接 endurl:结束链接 生成详情页链接到url.txt中
# -*- codeing = utf-8 -*-

import sys
import os
import datetime
import shutil

from bs4 import BeautifulSoup  # 网页解析，获取数据
import requests
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import pymysql

import functools  # 任务超时处理
from concurrent import futures

executor = futures.ThreadPoolExecutor(1)

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))
pathPrefix = up_dir_path


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        'Cookie': ''
        , "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
        , 'Host': 'acgus.top'
        , 'Accept': 'text/epub,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        , 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
        , 'Sec-Fetch-Dest': 'document'
        , 'Sec-Fetch-Mode': 'navigate'
        , 'Sec-Fetch-Site': 'none'
        , 'Sec-Fetch-User': '?1'
        , 'TE': 'trailers'
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


#################### 下载图片 ####################
def downloads(imageName, imgLink):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        'Cookie': 'ipb_member_id=7569132; ipb_pass_hash=3e2da9a0293d1a1132d5b2759d5a7bfa; yay=louder; igneous=3e2482fa5; sk=gz6u25bg3v7z60cutug5heb2sj30',
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    filePath = pathPrefix + "\\photo" + "\\" + imageName

    j = 0

    while (1 > 0):
        try:
            # VPN暂时断网之后无限重试拉取当前图片
            con = ''
            while (1 > 0):
                try:
                    con = getImgContent(imgLink, head)
                    if len(con) == 28658:
                        con = ''

                    break
                except TimeoutError:
                    # 写入文件失败
                    print("重新拉取图片链接: " + imageName)
                except Exception:
                    break

            # 写入文件
            with open(f'{filePath}', 'wb') as w:
                w.write(con)

            break
        except Exception as result:
            # 写入文件失败
            print(result)
            print("下载失败: " + imageName)
            j = j + 1
            print("开始第 %d 次重试" % (j))
            if j > 5:
                print("删除文件: " + imageName)
                os.remove(filePath)
                break


def getImgContent(imgLink, head):
    con = requests.get(url=imgLink, headers=head).content
    return con


# 保存数据到表格
def saveData(datalist):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('download', cell_overwrite_ok=True)  # 创建工作表

    # 列名
    # col = ("序号", "文件夹名称", "链接", "缩略图", "分类", "上传时间")
    col = (
        "no", "folder_name", "folder_url", "image_thumbnail_url", "category", "upload_time")
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])

    # datalist
    for i in range(0, len(datalist)):
        print("第%d条" % (i + 1))  # 输出语句，用来测试
        data = datalist[i]
        for j in range(0, len(col)):
            if j == 2:
                sheet.write(i + 1, 6, data[j])
                sheet.write(i + 1, j, '=HYPERLINK(G' + str(i + 2) + ',G' + str(i + 2) + ')')
                continue
            if j == 3:
                sheet.write(i + 1, 7, data[j])
                sheet.write(i + 1, j, '=HYPERLINK(H' + str(i + 2) + ',H' + str(i + 2) + ')')
                continue
            if len(str(data[j])) < 32766:
                sheet.write(i + 1, j, data[j])  # 数据
            else:
                sheet.write(i + 1, j, '')

    book.save(pathPrefix + "\\" + "download" + ".xls")  # 保存


# 爬取网页
def getData(baseurl):
    datalist = []
    url = baseurl + "2/"

    page = 2
    index = 1

    while (1 > 0):
        print("========== 开始爬取第%d页 ==========" % (page))

        j = 1
        while (1 > 0):
            # 抓取失败时无限重试
            try:
                html = askURL(url)  # 保存获取到的网页源码
                # 逐一解析数据
                soup = BeautifulSoup(html, "epub.parser")

                li_all = soup.find_all('div', attrs={'class': 'article-sort-item'})
                count = len(li_all)
                break
            except:
                print("第%d次重试" % (j))
                j = j + 1

        for i in range(1, count):
            data = []  # 保存一个PDF所有信息

            # 2.1 序号
            print("========== 开始爬取第 %d 条 ==========" % index)
            data.append(index)

            item1 = li_all[i]

            li_all1 = item1.find_all('a', attrs={'class': 'article-sort-item-img'})
            item2 = li_all1[0]
            item2 = str(item2)

            # 2.2 名称
            findFolderName = re.compile(r'title="(.*?)"')
            folderName = re.findall(findFolderName, item2)[0]  # 通过正则表达式查找
            data.append(folderName)

            # 2.2 链接地址
            findFolderUrl = re.compile(r'href="(.*?)"')
            folderUrl = re.findall(findFolderUrl, item2)[0]
            data.append('https://acgus.top' + folderUrl)

            # 2.3 缩略图
            findImageThumbnailUrl = re.compile(r'data-lazy-src="(.*?)"')
            imageThumbnailUrl = re.findall(findImageThumbnailUrl, item2)[0]
            data.append(imageThumbnailUrl)

            # 下载缩略图
            imageName = str(index).zfill(4)+ ".webp"
            print("开始下载: " + imageName)
            downloads(imageName, imageThumbnailUrl)
            print("下载完成: " + imageName)

            # 2.4 分类
            li_all2 = item1.find_all('a', attrs={'class': 'article-meta__tags'})
            category = ''
            for k in range(0, len(li_all2)):
                item3 = li_all2[k]
                item3 = str(item3)

                findCategory = re.compile(r'</i>(.*?)</span>')
                temp = re.findall(findCategory, item3)[0]
                category = category + '&' + temp

            data.append(category)

            # 2.6 上传日期
            li_all3 = item1.find_all('div', attrs={'class': 'article-sort-item-time'})
            item4 = li_all3[0]
            item4 = str(item4)

            findUploadTime = re.compile(r'datetime="(.*?)T')
            uploadTime = re.findall(findUploadTime, item4)[0]
            data.append(uploadTime)

            # 保存到集合中
            print("data:" + str(data))
            datalist.append(data)

            index = index + 1
            print("========== 爬取完毕第 %d 条 ==========" % index)

        # 3.抓取下一页
        page = page + 1
        url = baseUrl + str(page) + "/"
        if (page == 127):
            break

    return datalist


if __name__ == "__main__":  # 当程序执行时
    # baseUrl = 'https://acgus.top/categories/PC/page/2/'
    baseUrl = 'https://acgus.top/categories/PC/page/'

    datalist = getData(baseUrl)

    saveData(datalist)
