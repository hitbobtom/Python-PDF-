# nga链接爬取
# -*- codeing = utf-8 -*-

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import datetime
import time


def main(baseurl, page, start, end):
    # 1.爬取网页
    datalist = getData(baseurl, start, end)
    sorted_datalist = sorted(datalist, key=lambda x: (x[1], x[5]), reverse=True)

    # 2.保存数据
    savepath = str(page) + "_下载链接_" + str(start) + "-" + str(end) + ".xls"  # 当前目录新建XLS，存储进去
    saveData(sorted_datalist, savepath)


# 爬取网页
def getData(baseurl, start, end):
    datalist = []  # 用来存储爬取的网页信息

    for i in range(start, end + 1):
        print("开始爬取第%d页" % (i))

        index = 0

        try:
            # 2.1 要爬取的详情页
            url = baseurl + str(i)
            html = askURL(url)  # 保存获取到的网页源码

            # 逐一解析数据
            soup = BeautifulSoup(html, "epub.parser")

            item = soup.findAll('div', attrs={'id': 'm_threads'})[0]
            item = str(item)
            # PDF名称
            li_all1 = soup.find_all('td', attrs={'class': 'c1'})
            li_all2 = soup.find_all('td', attrs={'class': 'c2'})
            li_all3 = soup.find_all('td', attrs={'class': 'c3'})
            li_all4 = soup.find_all('td', attrs={'class': 'c4'})
            for j in range(0, len(li_all1)):
                data = []  # 保存一个PDF所有信息
                # 序号
                index = index + 1
                data.append(index)

                item1 = li_all1[j]
                item1 = str(item1)

                item2 = li_all2[j]
                item2 = str(item2)

                item3 = li_all3[j]
                item3 = str(item3)

                item4 = li_all4[j]
                item4 = str(item4)

                if ("大舰队招募" in item2) or ("晒欧帖" in item2) or ("版务公告" in item2):
                    continue

                # 发布时间
                findPostdate = re.compile(r'class="silver postdate"(.*?)</span>')
                temp = re.findall(findPostdate, item3)[0]  # 通过正则表达式查找
                postdate = temp.split('>')[1]
                dt = datetime.datetime.fromtimestamp(int(postdate))
                data.append(dt.strftime("%Y-%m-%d"))

                # 分类
                findTitle = re.compile(r'<a class="topic"(.*?)</a>')
                temp = re.findall(findTitle, item2)[0]  # 通过正则表达式查找
                title = temp.split('>')[1]

                findCategory = re.compile(r'^\[(.*?)]')
                try:
                    category = re.findall(findCategory, title)[0]
                    data.append(category)
                except:
                    data.append('')
                    pass

                # 标题
                data.append(title)

                # 超链接
                data.append('')

                # 评价数
                findCount = re.compile(r'title="打开新窗口">(.*?)</a>')
                commentCount = re.findall(findCount, item1)[0]  # 通过正则表达式查找
                data.append(int(commentCount))

                # 作者
                findAuthor = re.compile(r'<a class="author"(.*?)</a>')
                temp = re.findall(findAuthor, item3)[0]  # 通过正则表达式查找
                author = temp.split('>')[1]
                data.append(author)

                # 完整时间
                data.append(dt.strftime("%Y-%m-%d %H:%M:%S"))

                # 链接
                findHref = re.compile(r'href="(.*?)"')
                href = re.findall(findHref, item1)[0]  # 通过正则表达式查找
                data.append('https://bbs.nga.cn' + href)

                # 标记
                data.append(0)

                print('data: ' + str(data))

                # 保存到集合中
                datalist.append(data)

        except:
            print("转换异常")
            continue

        print("爬取完毕第%d页" % (i))
        time.sleep(5)

    return datalist


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        'Cookie': 'ngaPassportUid=61178806; guestJs=1696817829; lastpath=/thread.php?fid=564&page=2; bbsmisccookies=%7B%22uisetting%22%3A%7B0%3A%22e%22%2C1%3A1696818198%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-44%2C1%3A1696870830%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1696870830%7D%7D; ngaPassportOid=ae8a250a40dfe1e72257d9f8e64f9f82; ngacn0comUserInfo=lqy%25B8%25A1%25C9%25FA%25C8%25F4%25C3%25CE%09lqy%25E6%25B5%25AE%25E7%2594%259F%25E8%258B%25A5%25E6%25A2%25A6%0939%0939%09%0910%090%094%090%090%09; ngacn0comUserInfoCheck=5e2cd3fa6a70c1f28380ad4bc5e8c53e; ngacn0comInfoCheckTime=1696817892; ngaPassportUrlencodedUname=lqy%25B8%25A1%25C9%25FA%25C8%25F4%25C3%25CE; ngaPassportCid=X8s587o8952nl24ba7qdclbknkvc2o7ciu6u0pgi',
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("gbk")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据到表格
def saveData(datalist, savepath):
    print("save.......")

    # 1.创建表格
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('下载链接', cell_overwrite_ok=True)  # 创建工作表

    # 2.设置样式
    # 设置列宽，一个中文等于两个英文等于两个字符，11为字符数，256为衡量单位
    sheet.col(3).width = 90 * 256  # 标题
    sheet.col(1).width = 15 * 256  # 发布时间
    sheet.col(6).width = 25 * 256  # 完整时间

    alignment = xlwt.Alignment()
    # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
    alignment.horz = 0x02

    # 样式一：表头
    font0 = xlwt.Font()
    font0.name = '微软雅黑'
    font0.height = 20 * 11
    font0.bold = True

    style0 = xlwt.XFStyle()
    style0.font = font0
    style0.alignment = alignment

    # 样式二：正文
    font1 = xlwt.Font()
    font1.name = '微软雅黑'
    font1.height = 20 * 11

    style1 = xlwt.XFStyle()
    style1.font = font1

    # 样式三：标注
    font2 = xlwt.Font()
    font2.name = '微软雅黑'
    font2.height = 20 * 11

    # 设置背景颜色
    pattern = xlwt.Pattern()
    # 设置背景颜色的模式
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    # 背景颜色
    pattern.pattern_fore_colour = 5

    style2 = xlwt.XFStyle()
    style2.font = font2
    style2.pattern = pattern

    # 3.写入数据
    # 3.1 表头
    col = ("id", "发布时间", "分类", "标题", "超链接", "评论数", "作者", "完整时间", "链接", "标记")
    for i in range(0, len(col)):
        sheet.write(0, i, col[i], style0)
    # 3.2 数据
    day = ''
    # 行
    for i in range(0, len(datalist)):
        print("第%d条" % (i + 1))
        data = datalist[i]
        # 每天的第一条数据高亮
        if day != data[1]:
            day = data[1]
            style = style2
        else:
            style = style1
        # 列
        for j in range(0, len(col)):
            if j == 4:
                sheet.write(i + 1, j, '=HYPERLINK(I' + str(i + 2) + ',F' + str(i + 2) + ')', style)
                continue
            if len(str(data[j])) < 32766:
                sheet.write(i + 1, j, data[j], style)  # 数据
            else:
                sheet.write(i + 1, j, '', style)
    # 4.保存
    book.save(savepath)


if __name__ == "__main__":  # 当程序执行时

    main("https://bbs.nga.cn/thread.php?fid=-195362&page=", '少女前线2', 1, 500)
    main("https://bbs.nga.cn/thread.php?fid=428&page=", '手机网页游戏综合讨论', 1, 100)
    # main("https://bbs.nga.cn/thread.php?fid=564&page=", '碧蓝航线', 1, 100)


    # baseurl = ""
    # main(baseurl, '', 1, 100)

    print("爬取完毕！")
