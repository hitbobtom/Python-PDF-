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

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
pathPrefix = up_dir_path + "\\" + "torrents"
pathPrefixImg = "D:\\04_code\\qtf\\03_image\\src\\main\\resources\\static\\img\\ehentai_thumbnail"
# pathPrefixImg = up_dir_path + "\\" + "img" + "\\" + "Thumbnail" + "\\"
httpPrefix = "http://localhost/img/ehentai_thumbnail/"


# 爬取网页
def getData(baseurl, endUrl, pages):
    datalist = []
    url = baseurl

    page = 1
    index = 1
    days = 0

    while (1 > 0):
        print("========== 开始爬取第%d页 ==========" % (page))
        # 1.爬取总条数
        j = 1
        while (1 > 0):
            # 抓取失败时无限重试
            try:
                html = askURL(url)  # 保存获取到的网页源码
                # 逐一解析数据
                soup = BeautifulSoup(html, "epub.parser")

                item1 = soup.find('table', attrs={'class': 'itg glte'})
                item1 = str(item1)
                findCount = re.compile(r'<td class="gl1e"(.*?)</td>')

                list = re.findall(findCount, item1)
                count = len(list)
                break
            except:
                print("第%d次重试" % (j))
                j = j + 1

        # 下一个链接
        try:
            item1 = soup.find('div', attrs={'class': 'searchnav'})
            item1 = str(item1)

            findNextUrl = re.compile(r'Jump/Seek</a></div><div><a href="(.*?)" id="unext"')
            nextUrl = re.findall(findNextUrl, item1)[0].replace('amp;', '')
        except:
            print("已经是最后一页")
            nextUrl = ''

        # 2.逐个抓取
        li_all1 = soup.find_all('td', attrs={'class': 'gl1e'})
        li_all2 = soup.find_all('div', attrs={'class': 'gl3e'})
        li_all3 = soup.find_all('td', attrs={'class': 'gl2e'})
        li_all4 = soup.find_all('div', attrs={'class': 'gl4e glname'})
        for i in range(0, count):
            data = []  # 保存一个PDF所有信息

            # 2.1 序号
            print("========== 开始爬取第 %d 条 ==========" % index)
            data.append(index)

            item1 = li_all1[i]
            item1 = str(item1).replace('\'', '\"')

            # 2.2 文件夹名称
            findFolderName = re.compile(r'title="(.*?)"')
            folderName = re.findall(findFolderName, item1)[0]  # 通过正则表达式查找
            data.append(folderName)

            # 2.3 详情页链接
            findFolderUrl = re.compile(r'<a href="(.*?)">')
            folderUrl = re.findall(findFolderUrl, item1)[0]  # 通过正则表达式查找
            data.append(folderUrl)

            # 2.4 缩略图
            findImageThumbnailUrl = re.compile(r'src="(.*?)"')
            imageThumbnailUrl = re.findall(findImageThumbnailUrl, item1)[0]  # 通过正则表达式查找

            # 下载缩略图
            # list = imageThumbnailUrl.split('/')
            # imageName = list[len(list) - 1]
            # imageName = str(index).zfill(4) + "_" + imageName
            # print("开始下载: " + imageName)
            # downloads(imageName, imageThumbnailUrl)
            # print("下载完成: " + imageName)
            # imageThumbnailUrl = httpPrefix + imageName

            data.append(imageThumbnailUrl)

            item1 = li_all2[i]
            item1 = str(item1)

            # 2.5 文件夹分类
            findCategory = re.compile(r'<div class="cn(.*?)</div>')
            temp = re.findall(findCategory, item1)[0]  # 通过正则表达式查找
            category = temp.split('>')[1]
            data.append(category)

            # 2.6 上传日期
            findUploadTime = re.compile(r'675,415\)">(.*?)</div>')
            uploadTime = re.findall(findUploadTime, item1)[0]  # 通过正则表达式查找
            data.append(uploadTime)

            result = 0
            # result = compareTime(uploadTime)
            if result == 1:
                break

            # 2.7 星级
            findScore = re.compile(r'background-position:(.*?)px')
            temp = re.findall(findScore, item1)[0]  # 通过正则表达式查找
            score = int(temp)
            rank = getRank(score)
            data.append(rank)

            item2 = li_all3[i]
            item2 = str(item2)

            # 2.8 图片总页码数
            # findImageCount = re.compile(r'</a></div><div>(.*?) pages</div>')
            findImageCount = re.compile(r'</div><div>(.*?) pages</div>')
            list = re.findall(findImageCount, item2)
            if (len(list) != 0):
                imageCount = list[0]
            else:
                imageCount = '1'

            imageCount = re.sub(r'<a.*<div>', '', imageCount)

            data.append(int(imageCount))

            item3 = li_all4[i]
            item3 = str(item3)
            # 2.9 语言
            findLanguage = re.compile(r'title="language:chinese">(.*?)</div>')
            list = re.findall(findLanguage, item3)
            if (len(list) != 0):
                language = 1
            else:
                language = 0

            data.append(language)

            # 保存到集合中
            print("data:" + str(data))
            datalist.append(data)

            index = index + 1
            print("========== 爬取完毕第 %d 条 ==========" % index)

        # 3.抓取下一页
        page = page + 1
        url = nextUrl
        if ((nextUrl == '') or (url == endUrl) or (page > pages) or (days == 1)):
            break

    return datalist


def compareTime(uploadTime):
    result = 0

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d") + " 23:59"
    if uploadTime <= yesterday_str:
        result = 1

    return result


def getRank(score):
    rank = 0
    if score == 80:
        rank = 0
    elif score > -80 and score < -60:
        rank = 1
    elif score >= -60 and score < -40:
        rank = 2
    elif score >= -40 and score < -20:
        rank = 3
    elif score >= -20 and score < 0:
        rank = 4
    elif score == 0:
        rank = 5
    return rank


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        'Cookie': 'ipb_member_id=7569132; ipb_pass_hash=3e2da9a0293d1a1132d5b2759d5a7bfa; yay=louder; igneous=3e2482fa5; sk=gz6u25bg3v7z60cutug5heb2sj30',
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


# 保存url到文件中
def writeFile(path, list):
    f = open(path, "w")

    # 下载链接
    for i in range(0, len(list)):
        f.write(list[i])
        if i != len(list) - 1:
            f.write('\n')

    f.close()


def clear_folder_shutil(path):
    shutil.rmtree(path)
    os.mkdir(path)


#################### 下载图片 ####################
def downloads(imageName, imgLink):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        'Cookie': 'ipb_member_id=7569132; ipb_pass_hash=3e2da9a0293d1a1132d5b2759d5a7bfa; yay=louder; igneous=3e2482fa5; sk=gz6u25bg3v7z60cutug5heb2sj30',
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    filePath = pathPrefixImg + "\\" + imageName

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


def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            future = executor.submit(func, *args, **kw)
            return future.result(timeout=seconds)

        return wrapper

    return decorator


@timeout(60)
def getImgContent(imgLink, head):
    con = requests.get(url=imgLink, headers=head).content
    return con


#################### 保存数据到表格 ####################
def saveData(datalist):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('search', cell_overwrite_ok=True)  # 创建工作表

    # 列名
    col = ("no", "flie_name", "file_detail_url", "thumbnail_url", "category", "page_size")
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])

    # datalist
    for i in range(0, len(datalist)):
        print("第%d条" % (i + 1))  # 输出语句，用来测试
        data = datalist[i]
        for j in range(0, len(col)):
            if len(str(data[j])) < 32766:
                sheet.write(i + 1, j, data[j])  # 数据
            else:
                sheet.write(i + 1, j, '')

    book.save(pathPrefix + "\\" + "01_search" + ".xls")  # 保存


# 获取mysql连接
def getConnection():
    host = 'localhost'
    user = 'root'
    password = '123456'
    db = 'image'
    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    return connection


def insertMysql(datalist):
    # 1.mysql
    conn = getConnection()
    # 获得游标对象
    cursor = conn.cursor()

    cursor.execute("truncate table ehentai_info")

    # 2.处理数据
    for i in range(len(datalist)):
        data = datalist[i]

        insert = (
            "insert into ehentai_info(`file_no`, `flie_name`, `file_detail_url`, `thumbnail_url`, `category`, `upload_time`,`ranks`,`page_size`,`languages`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        data = (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
        print(data)

        cursor.execute(insert, data)
    conn.commit()
    conn.close()


def main(baseUrl, endUrl, pages, urlPath):
    # clear_folder_shutil(pathPrefixImg)
    # 1.爬取网页
    datalist = getData(baseUrl, endUrl, pages)
    # 2.保存url到url文件中
    url_list = []
    for i in range(0, len(datalist)):
        data = datalist[i]
        url_list.append(data[2])
    writeFile(urlPath, url_list)
    # 3.保存数据到表格
    insertMysql(datalist)


if __name__ == "__main__":  # 当程序执行时
    baseUrl = sys.argv[1]
    pages = int(sys.argv[2])
    print(baseUrl)
    print(pages)
    # baseUrl =  'https://exhentai.org/?f_search=language%3Achinese&advsearch=1'
    # pages = 3
    endUrl = 'https://e-hentai.org/popular'

    urlPath = pathPrefix + "\\" + '01_url.txt'
    main(baseUrl, endUrl, pages, urlPath)

    print("爬取完毕！")
