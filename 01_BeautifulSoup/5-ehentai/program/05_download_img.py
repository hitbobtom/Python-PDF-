# ehentai链接爬取: 读取download_url.txt中的详情页链接，下载图片
# -*- codeing = utf-8 -*-

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import requests
import urllib.request, urllib.error  # 制定URL，获取网页数据
import os
import xlrd  # 读取excel

import functools  # 任务超时处理
from concurrent import futures

executor = futures.ThreadPoolExecutor(1)

pathPrefix = ''
up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
pathPrefix1 = up_dir_path + "\\" + "torrents"


# 爬取网页
def getData(folderName, url):
    j = 1
    while (1 > 0):
        # 抓取失败时无限重试
        try:
            html = askURL(url)  # 保存获取到的网页源码
            # 逐一解析数据
            soup = BeautifulSoup(html, "epub.parser")

            item1 = soup.find('div', attrs={'id': 'i1'})
            item1 = str(item1)
            findFolderNameEng = re.compile(r'<h1>(.*?)</h1>')

            folderNameEng = re.findall(findFolderNameEng, item1)[0]
            break
        except:
            print("第%d次重试" % (j))
            j = j + 1

    item2 = soup.find('div', attrs={'id': 'i2'})
    item2 = str(item2)

    # 图片序号
    findImageNo = re.compile(r'<div><span>(.*?)</span>')
    imageNo = re.findall(findImageNo, item2)[0]  # 通过正则表达式查找

    findImageInfo = re.compile(r'<img src="https://ehgt.org/g/l.png"/></a></div><div>(.*?)B</div>')
    imageInfo = re.findall(findImageInfo, item2)[0]  # 通过正则表达式查找
    list = imageInfo.split("::")
    # 图片名称
    imageName = list[0].strip()

    # 页面图片链接
    item1 = soup.find('div', attrs={'id': 'i3'})
    item1 = str(item1)
    findLink = re.compile(r'src="(.*?)"')
    imgLink = re.findall(findLink, item1)[0]  # 通过正则表达式查找

    # 下载图片
    print("开始下载")
    downloads(folderName, imageNo.zfill(4), imageName, imgLink)
    print("下载完成")


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
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
def downloads(folderName, imageNo, imageName, imgLink):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        'Cookie': 'ipb_session_id=a7de4f5f8ab07725ed1f17c3ae325ef4; ipb_member_id=7529754; ipb_pass_hash=c46228dbc2650e82eee75d8b69246b5d',
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    filePath = pathPrefix + folderName + "\\" + imageNo + "_" + imageName

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
                    print("重新拉取图片链接: " + imageNo + "-" + imageName)
                except Exception:
                    break

            # 写入文件
            with open(f'{filePath}', 'wb') as w:
                w.write(con)

            break
        except Exception as result:
            # 写入文件失败
            print(result)
            print("下载失败: " + imageNo + "-" + imageName)
            j = j + 1
            print("开始第 %d 次重试" % (j))
            if j > 5:
                print("删除文件: " + imageNo + "-" + imageName)
                os.remove(filePath)
                break


def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            future = executor.submit(func, *args, **kw)
            return future.result(timeout=seconds)

        return wrapper

    return decorator


@timeout(20)
def getImgContent(imgLink, head):
    con = requests.get(url=imgLink, headers=head).content
    return con


def readFile(path):
    list = []
    f4 = open(path, encoding='utf-8')
    # 利用循环全部读出
    while 1 > 0:
        line = f4.readline()
        if line == '':
            break
        line = line.strip().replace('\n', '')
        if line == '':
            break
        list.append(line)

    f4.close()
    return list


def readExcel(path, col, row):
    # 打开excel
    readbook = xlrd.open_workbook(path)
    # 确定sheet页
    sheet = readbook.sheet_by_index(0)

    cols = sheet.col_values(col, 1)
    row = int(row)
    url = cols[row - 1]
    return url


def main(folderName, baseurl):
    getData(folderName, baseurl)


if __name__ == "__main__":  # 当程序执行时

    # 1.拼接路径
    index_list = readFile(pathPrefix1 + "\\" + "epub.txt")

    parentFolderName = index_list[0]
    pathPrefix = up_dir_path + "\\img\\" + parentFolderName + "\\"
    folderName = index_list[1]

    # 调用函数
    for i in range(2, len(index_list)):
        # 序号
        print("========== 开始下载第 %d 张 ==========" % (i - 1))
        url = readExcel(pathPrefix + "\\" + folderName + "\\" + "download.xls", 8, index_list[i])
        main(folderName, url)
        print("========== 第 %d 张下载完成 ==========" % (i - 1))

    print("下载完毕！")
