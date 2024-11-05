# ehentai链接爬取:读取url.txt中的详情页链接
# 生成详细表格: download.xls
# 有磁力链接的: torrent.txt
# 没有磁力链接的: download_url.txt
# -*- codeing = utf-8 -*-

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import os
import time
from multiprocessing.dummy import Pool

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
pathPrefix = up_dir_path + "\\" + "torrents"


# 爬取网页
def getData(url):
    data = []  # 保存一个PDF所有信息

    print("开始爬取: " + url)

    j = 1
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
                return data

                # 文件夹名称
            item1 = soup.find('div', attrs={'id': 'gd2'})
            item1 = str(item1)
            findFolderName = re.compile(r'<h1 id="gj">(.*?)</h1>')
            folderName = re.findall(findFolderName, item1)[0]  # 通过正则表达式查找
            if folderName == '':
                folderNameEng = re.compile(r'<h1 id="gn">(.*?)</h1>')
                folderName = re.findall(folderNameEng, item1)[0]  # 通过正则表达式查找

            break
        except:
            print("第%d次重试" % (j))
            j = j + 1

    # 序号
    # data.append(i + 1)

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
    list = re.findall(findRatingLabel, item4)
    if (len(list) != 0):
        ratingLabel = list[0]
    else:
        ratingLabel = '0.0'

    data.append(float(ratingLabel))

    li_all = soup.find_all('div', attrs={'class': 'gdtm'})
    if len(li_all) != 0:
        item5 = li_all[0]
        item5 = str(item5)

        # 首张图片链接
        findImgHref = re.compile(r'<a href="(.*?)">')
        imgHref = re.findall(findImgHref, item5)[0]
        # data.append(imgHref)
        data.append(url)

        # 首张图片缩略图
        findImgUrl = re.compile(r'src="(.*?)"')
        imgUrl = re.findall(findImgUrl, item5)[0]
        data.append(imgUrl)

        # 首张图片名称
        findImgName = re.compile(r'title="(.*?)"/>')
        imgName = re.findall(findImgName, item5)[0]
        data.append(imgName)
    else:
        data.append('')
        data.append('')
        data.append('')

    item6 = soup.find('div', attrs={'id': 'gd5'})
    item6 = str(item6)

    # 种子详情页链接
    findTorrentsUrl = re.compile(r'return popUp\(\'(.*?)\',')
    torrentsUrl = re.findall(findTorrentsUrl, item6)[1]
    torrentsUrl = torrentsUrl.replace('amp;', '')
    data.append(torrentsUrl)

    try:
        # 种子名称
        list = getTorrents(torrentsUrl)
        torrentName = list[1]
        data.append(torrentName)
        # 种子链接
        torrents = list[7]
        data.append(torrents)

    except:
        print("种子链接下载异常")
        data.append('')
        data.append('')

    finally:
        print("data:" + str(data))
        print("爬取完毕: " + url)

        # 延时函数
        time.sleep(2)

    return data


def getTorrents(torrentsUrl):
    print("开始爬取torrents")
    datalist = []

    # 1.爬取总条数
    j = 1
    while (1 > 0):
        # 抓取失败时无限重试
        try:
            html = askURL(torrentsUrl)  # 保存获取到的网页源码
            # 逐一解析数据
            soup = BeautifulSoup(html, "epub.parser")

            item1 = soup.find('div', attrs={'id': 'torrentinfo'})
            item1 = str(item1)
            findCount = re.compile(r'<input name="gtid"(.*?)/>')

            list = re.findall(findCount, item1)
            count = len(list)
            break
        except:
            print("第%d次重试" % (j))
            j = j + 1

    # 2.逐个抓取
    li_all = soup.find_all('table')
    for i in range(0, count):
        data = []  # 保存一个PDF所有信息

        # 序号
        data.append(i + 1)

        item1 = li_all[i]
        item1 = str(item1)

        # torrentName
        try:
            findTorrentName = re.compile(r'\'; return false">(.*?)</a>')
            torrentName = re.findall(findTorrentName, item1)[0]  # 通过正则表达式查找
            data.append(torrentName)
        except:
            data.append('')

        # Posted
        findPosted = re.compile(r'Posted:</span> (.*?)</td>')
        posted = re.findall(findPosted, item1)[0]  # 通过正则表达式查找
        data.append(posted)

        # Size
        findSize = re.compile(r'Size:</span> (.*?)</td>')
        size = re.findall(findSize, item1)[0]  # 通过正则表达式查找
        data.append(size)

        # Seeds
        findSeeds = re.compile(r'Seeds:</span> (.*?)</td>')
        seeds = re.findall(findSeeds, item1)[0]  # 通过正则表达式查找
        data.append(seeds)

        # Peers
        findPeers = re.compile(r'Peers:</span> (.*?)</td>')
        peers = re.findall(findPeers, item1)[0]  # 通过正则表达式查找
        data.append(peers)

        # Downloads
        findDownloads = re.compile(r'Downloads:</span> (.*?)</td>')
        downloads = re.findall(findDownloads, item1)[0]  # 通过正则表达式查找
        data.append(int(downloads))

        # href
        try:
            findHref = re.compile(r'<a href="(.*?)" onclick')
            href = re.findall(findHref, item1)[0]  # 通过正则表达式查找
            data.append(href)
        except:
            data.append('')
        finally:
            datalist.append(data)

    # datalist.sort(key=lambda row: (row[1],row[5]), reverse=True)
    datalist.sort(key=lambda row: (row[6]), reverse=True)

    for i in range(0, count):
        if datalist[i][7] != '':
            return datalist[i]

    raise Exception()


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


def create_path(savepath):
    # 创建文件夹 data
    path = pathPrefix + savepath
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    else:
        pass
    return path


# 保存数据到表格
def saveData(datalist):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('download', cell_overwrite_ok=True)  # 创建工作表

    # 列名
    # col = ("序号", "文件夹日文名", "文件夹英文名", "文件夹分类", "Posted", "Language", "File Size", "Length", "Favorited", "评分人数", "平均分","首张图片链接", "首张图片缩略图", "首张图片名称", "种子详情页链接", "种子名称", "种子链接")
    col = (
        "no", "jan_name", "eng_name", "category", "posted", "language", "file_size", "length", "favorited",
        "rating_count",
        "average_score", "base_url", "first_img_url", "first_img_name", "torrent_detail_url", "torrent_name",
        "torrent_url")
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

    book.save(pathPrefix + "\\" + "02_download" + ".xls")  # 保存


def saveUrl(datalist):
    all_list = []
    download_list = []
    torrent_list = []

    for i in range(0, len(datalist)):
        data = datalist[i]
        # 链接
        all_list.append(data[11])
        if data[16] == '':
            download_list.append(data[11])
        else:
            torrent_list.append(data[16])

    # 种子链接
    writeFile(pathPrefix + "\\" + "02_torrent.txt", torrent_list)
    # 下载链接
    writeFile(pathPrefix + "\\" + "03_download_url.txt", download_list)
    # 全部下载链接
    writeFile(pathPrefix + "\\" + "02_all_download_url.txt", all_list)


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
        f.write('\n')

    f.close()


def main(url_list):
    datalist = []

    # 1.多线程爬取网页
    pool = Pool(6)
    list = pool.map(getData, url_list)
    pool.close()

    for i in range(0, len(list)):
        data = list[i]
        if (len(data) != 0):
            data.insert(0, i + 1)
            datalist.append(data)
    # datalist.sort(key=lambda row: (row[7]))

    # 2.保存数据
    saveData(datalist)
    # 3.保存链接
    saveUrl(datalist)


if __name__ == "__main__":  # 当程序执行时
    urlPath = pathPrefix + "\\" + '01_url.txt'
    url_list = readFile(urlPath)

    print("========== 开始爬取 ==========")
    main(url_list)
    print("========== 爬取完成 ==========")
