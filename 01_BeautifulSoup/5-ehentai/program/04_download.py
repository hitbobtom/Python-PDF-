# ehentai链接爬取: 读取download_url.txt中的详情页链接，下载图片
# -*- codeing = utf-8 -*-

from bs4 import BeautifulSoup  # 网页解析，获取数据
import requests
import urllib.request, urllib.error  # 制定URL，获取网页数据
import re  # 正则表达式，进行文字匹配`
import xlwt  # 进行excel操作
import os
import time
import random
from multiprocessing.dummy import Pool

import functools  # 任务超时处理
from concurrent import futures

executor = futures.ThreadPoolExecutor(1)

parentFolderName = 'today'
up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
pathPrefix = up_dir_path + "\\" + "img" + "\\" + parentFolderName + "\\"
pathPrefix1 = up_dir_path + "\\" + "torrents"
folderName = ''


def get_source(url):
    i = 1
    while (1 > 0):
        # 抓取失败时无限重试
        try:
            html = askURL(url)  # 保存获取到的网页源码
            soup = BeautifulSoup(html, "epub.parser")

            # 遇到Content Warning的解决方案
            item1 = soup.find('p', attrs={'style': 'text-align:center'})
            item1 = str(item1)
            findWarning = re.compile(r'View Gallery')
            list = re.findall(findWarning, item1)
            if len(list) != 0:
                print(
                    "This gallery has been flagged as Offensive For Everyone. Due to its content, it should not be viewed by anyone.")
                soup = ''
                return soup

            # 校验是否拉取正确
            item1 = soup.find('div', attrs={'id': 'gd2'})
            item1 = str(item1)
            findFolderName = re.compile(r'<h1 id="gj">(.*?)</h1>')
            findFolderNameEng = re.compile(r'<h1 id="gn">(.*?)</h1>')

            folderNameTest = re.findall(findFolderName, item1)[0]  # 通过正则表达式查找
            if folderNameTest == '':
                folderNameTest = re.findall(findFolderNameEng, item1)[0]  # 通过正则表达式查找

            # 文件夹名称
            global folderName
            if folderName == '':
                folderName = re.findall(findFolderName, item1)[0]  # 通过正则表达式查找
                if folderName == '':
                    folderName = re.findall(findFolderNameEng, item1)[0]  # 通过正则表达式查找

            break
        except:
            print("第%d次重试" % (i))
            i = i + 1

    return soup


def get_img_info(soup):
    data = []

    item1 = soup.find('div', attrs={'id': 'gd2'})
    item1 = str(item1)

    # 文件夹日文名
    findFolderName = re.compile(r'<h1 id="gj">(.*?)</h1>')
    folderName = re.findall(findFolderName, item1)[0]
    data.append(folderName)

    # 文件夹英文名
    findFolderNameEng = re.compile(r'<h1 id="gn">(.*?)</h1>')
    folderNameEng = re.findall(findFolderNameEng, item1)[0]
    data.append(folderNameEng)

    # 文件夹分类
    item2 = soup.find('div', attrs={'id': 'gdc'})
    item2 = str(item2)

    findCategory = re.compile(r'<div class="cs(.*?)</div>')
    temp = re.findall(findCategory, item2)[0]  # 通过正则表达式查找
    category = temp.split('>')[1]
    data.append(category)

    item3 = soup.find('div', attrs={'id': 'gdd'})
    item3 = str(item3)

    findInfo = re.compile(r'<td class="gdt2">(.*?)<')
    list = re.findall(findInfo, item3)

    # Posted
    Posted = list[0]
    data.append(Posted)

    # Language
    language = list[3]
    data.append(language)

    # File Size
    fileSize = list[4]
    data.append(fileSize)

    # Length
    length = int(list[5].replace(' pages', ''))
    data.append(length)

    # Favorited
    item2 = soup.find('td', attrs={'id': 'favcount'})
    item2 = str(item2)

    findFavcount = re.compile(r'>(.*?) times')
    favcount = re.findall(findFavcount, item2)[0]  # 通过正则表达式查找
    data.append(int(favcount))

    item4 = soup.find('div', attrs={'id': 'gdr'})
    item4 = str(item4)

    # 评分人数
    findRatingCount = re.compile(r'<span id="rating_count">(.*?)</span>')
    ratingCount = re.findall(findRatingCount, item4)[0]
    data.append(int(ratingCount))

    # 平均分
    findRatingLabel = re.compile(r'>Average: (.*?)</td>')
    ratingLabel = re.findall(findRatingLabel, item4)[0]
    data.append(float(ratingLabel))

    print("data:" + str(data))
    return data


def get_all_page(soup):
    all_page_list = []

    item1 = soup.find('table', attrs={'class': 'ptt'})
    item1 = str(item1)

    findAllUrl = re.compile(r'<a href="(.*?)" ')
    urlList = re.findall(findAllUrl, item1)

    length = len(urlList) - 1
    if (length == 0):
        length = 1
    for i in range(0, length):
        all_page_list.append(urlList[i])

    return all_page_list


def get_img_url(soup):
    list = []

    li_all = soup.find_all('div', attrs={'class': 'gdtm'})
    for i in range(0, len(li_all)):
        item1 = li_all[i]
        item1 = str(item1)
        findImgUrl = re.compile(r'<a href="(.*?)"')
        imgUrl = re.findall(findImgUrl, item1)[0]  # 通过正则表达式查找
        list.append(imgUrl)

    return list


def query_img(url):
    data = []

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

    # 文件夹名称
    item1 = soup.find('div', attrs={'id': 'i1'})
    item1 = str(item1)
    findFolderNameEng = re.compile(r'<h1>(.*?)</h1>')
    folderNameEng = re.findall(findFolderNameEng, item1)[0]  # 通过正则表达式查找
    data.append(folderName)
    data.append(folderNameEng)

    item2 = soup.find('div', attrs={'id': 'i2'})
    item2 = str(item2)

    # 图片序号
    findImageNo = re.compile(r'<div><span>(.*?)</span>')
    imageNo = re.findall(findImageNo, item2)[0]  # 通过正则表达式查找
    data.append(int(imageNo))

    # 图片总页码数
    findImageCount = re.compile(r'/ <span>(.*?)</span></div>')
    imageCount = re.findall(findImageCount, item2)[0]  # 通过正则表达式查找
    data.append(int(imageCount))

    findImageInfo = re.compile(r'l.png"/></a></div><div>(.*?)B</div>')
    imageInfo = re.findall(findImageInfo, item2)[0]  # 通过正则表达式查找
    list = imageInfo.split("::")
    # 图片名称
    imageName = list[0].strip()
    data.append(imageName)

    # 图片名称黑名单
    if ("zzz" in imageName) or ("ver" in imageName) or ("ZZZ" in imageName):
        data.append('')
        data.append('')
        data.append('')
        data.append('')
        data.append('')
        data.append('')
        # 保存到集合中
        data.insert(0, int(data[2]))
        print("data:" + str(data))
        print("========== 爬取完毕 ==========")
        return data


    # 图片分辨率
    data.append(list[1].strip())
    # 图片大小
    data.append((list[2] + "B").strip())

    # 本张图片链接
    data.append(url)

    # 下张图片链接
    findNextUrl = re.compile(r'</span></div><a href="(.*?)" id="next"')
    url = re.findall(findNextUrl, item2)[0]  # 通过正则表达式查找
    data.append(url)

    # 页面图片链接
    item1 = soup.find('div', attrs={'id': 'i3'})
    item1 = str(item1)
    findLink = re.compile(r'src="(.*?)"')
    imgLink = re.findall(findLink, item1)[0]  # 通过正则表达式查找
    data.append(imgLink)

    # 下载图片
    print("开始下载: " + imageNo.zfill(4) + "_" + imageName)
    downloads(folderName, imageNo.zfill(4), imageName, imgLink)
    print("下载完成: " + imageNo.zfill(4) + "_" + imageName)

    try:
        # 下载链接
        item1 = soup.findAll('div', class_="if")[1]
        item1 = str(item1)
        findLink = re.compile(r'<a href="(.*?)"')
        downloadLink = re.findall(findLink, item1)[0]  # 通过正则表达式查找
        data.append(downloadLink.replace('amp;', ''))

    except:
        print("下载链接转换异常")
        data.append('')

    finally:
        # 保存到集合中
        data.insert(0, int(data[2]))
        print("data:" + str(data))
        print("========== 爬取完毕 ==========")

        # 延时函数
        time.sleep(2)

    return data


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


def create_path(folderName):
    path = pathPrefix + "\\" + folderName
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return folderName
    else:
        while 1 > 0:
            random_number = random.randint(1, 10)
            newFolderName = folderName + '-' + str(random_number)
            path = pathPrefix + "\\" + newFolderName
            isExists = os.path.exists(path)
            if not isExists:
                break
        os.makedirs(path)
        return newFolderName


#################### 下载图片 ####################
def downloads(folderName, imageNo, imageName, imgLink):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        'Cookie': 'ipb_member_id=7569132; ipb_pass_hash=3e2da9a0293d1a1132d5b2759d5a7bfa; yay=louder; igneous=3e2482fa5; sk=gz6u25bg3v7z60cutug5heb2sj30',
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    filePath = pathPrefix + "\\" + folderName + "\\" + imageNo + "_" + imageName

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
                    print("重新拉取图片链接: " + imageNo + "_" + imageName)
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


@timeout(60)
def getImgContent(imgLink, head):
    con = requests.get(url=imgLink, headers=head).content
    return con


#################### 保存数据到表格 ####################
def saveData(datalist):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('download', cell_overwrite_ok=True)  # 创建工作表

    col = ("序号", "文件夹名称", "文件夹名称(英文)", "图片序号", "图片总页码数", "图片名称", "图片分辨率", "图片大小", "本张图片链接", "下张图片链接", "页面图片链接", "下载链接")
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, len(datalist)):
        print("第%d条" % (i + 1))  # 输出语句，用来测试
        data = datalist[i]
        for j in range(0, len(col)):
            if len(str(data[j])) < 32766:
                sheet.write(i + 1, j, data[j])  # 数据
            else:
                sheet.write(i + 1, j, '')

    book.save(pathPrefix + "\\" + folderName + "\\" + "download" + ".xls")  # 保存


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


def main(baseurl):
    print("baseurl=" + baseurl)
    global folderName
    folderName = ''

    # 1.获取详情页的html
    toc_soup = get_source(baseurl)
    if toc_soup == '':
        return

    # 创建文件夹
    folderName = re.sub('[\\\/:*?"<>|]', '_', folderName)
    folderName = create_path(folderName)

    # 2.解析获取详情信息
    # 00_base = get_img_info(toc_soup)

    # 3.解析获取所有的图片链接
    url_list = []
    all_page_list = get_all_page(toc_soup)
    for i in range(0, len(all_page_list)):
        print("开始抓取第 %d 页的全部链接" % (i + 1))
        if i != 0:
            toc_soup = get_source(all_page_list[i])
        tmp_list = get_img_url(toc_soup)
        url_list = url_list + tmp_list
        print("第 %d 页的全部链接抓取完成" % (i + 1))

    # 2.多线程下载图片
    pool = Pool(6)
    datalist = pool.map(query_img, url_list)
    pool.close()

    datalist.sort(key=lambda row: (row[0]))

    # 3.保存数据到excel中
    saveData(datalist)


if __name__ == "__main__":  # 当程序执行时

    # 下载多个图集
    url_list = readFile(pathPrefix1 + "\\" + "03_download_url.txt")

    # 调用函数
    for i in range(0, len(url_list)):
        print("========== 开始下载第 %d 个文件，剩余 %d 个文件 ==========" % ((i + 1), (len(url_list) - i - 1)))
        main(url_list[i])
        print('\n')

    print("爬取完毕！")
