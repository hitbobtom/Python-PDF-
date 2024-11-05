# 80电子书链接爬取
# -*- codeing = utf-8 -*-

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作

# 爬取网页
def getData(start, end):
    datalist = []  # 用来存储爬取的网页信息

    baseurl1 = "https://www.xz577.com/e/"

    for i in range(start, end + 1):
        print("开始爬取第%d条" % (i))
        data = []  # 保存一个PDF所有信息

        try:
            # 1.序号
            data.append(i)

            url1 = baseurl1 + str(i) + ".epub"
            html1 = askURL(url1)  # 保存获取到的网页源码
            # 逐一解析数据
            soup1 = BeautifulSoup(html1, "epub.parser")

            item1 = soup1.findAll('h1', class_="f-22 mb10 txt-ov")[0]
            item1 = str(item1)
            # 2.PDF名称
            findPDFName = re.compile(r'<h1 class="f-22 mb10 txt-ov">(.*?)</h1>')
            pdfName = re.findall(findPDFName, item1)[0]
            data.append(pdfName)

            item2 = soup1.findAll('div', class_="soft-box tx-flex-dtc tx-flex-gr")[0]
            item2 = str(item2)
            # 3.分类
            findCategory = re.compile(r'<li class="col-12 col-p-12 waphide"><span>类别：</span>(.*?)</li>')
            category = re.findall(findCategory, item2)[0]  # 通过正则表达式查找
            data.append(category)
            # 4.作者
            findAuthor = re.compile(r'<li class="col-12 col-p-12" id="zuozhe"><span>作者：</span>(.*?)</li>')
            author = re.findall(findAuthor, item2)[0]
            data.append(author)
            # 5.出版社
            findPress = re.compile(r'<li class="col-12 col-p-12" id="chubanshe"><span>出版：</span>(.*?)</li>')
            press = re.findall(findPress, item2)[0]
            data.append(press)
            # 6.格式
            findFormat = re.compile(r'<li class="col-12 col-p-12"><span>格式：</span>(.*?)</li>')
            format = re.findall(findFormat, item2)[0]
            data.append(format)
            # 6.大小
            findSize = re.compile(r'<li class="col-12 col-p-12"><span>大小：</span>(.*?)</li>')
            size = re.findall(findSize, item2)[0]
            data.append(size)

            # 7.详情页
            data.append(baseurl1 + str(i) + ".epub#downn")

            item3 = soup1.findAll('div', class_="downnotice waphide")[0]
            item3 = str(item3)
            # 8.下载地址
            findDownloadHref = re.compile(r'<p class="xiazaidizhi">下载地址：<a href="(.*?)" rel="nofollow">网盘下载')
            downloadHref = re.findall(findDownloadHref, item3)[0]  # 通过正则表达式查找
            data.append(downloadHref)

            item4 = soup1.findAll('div', class_="tx-text pd20-3 f-16 tx-text-em imgce")[0]
            item4 = str(item4)
            # 8.评分
            findScore = re.compile(r'综合评分为：(.*?)分')
            score = re.findall(findScore, item4)[0]  # 通过正则表达式查找
            data.append(score)

            # 9.资源介绍
            item4 = str(item4).replace('\t', '') \
                .replace('\n</div>', '') \
                .replace('<div class="tx-text pd20-3 f-16 tx-text-em imgce">\n', '')
            data.append(item4)
            # 10.资源介绍(去换行)
            item4 = str(item4).replace('\n', '<br>').replace('\r', '').replace('\t', '') \
                .replace('\n</div>', '') \
                .replace('<div class="tx-text pd20-3 f-16 tx-text-em imgce">\n', '')
            data.append(item4)

            item5 = soup1.findAll('span', class_="img-box mb10 ecenter")[0]
            item5 = str(item5)
            # 11.封面图片
            findCover = re.compile(r'src="(.*?)"/>')
            cover = re.findall(findCover, item5)[0]  # 通过正则表达式查找
            data.append("https://www.xz577.com" + cover)

            # 保存到集合中
            datalist.append(data)
            print("爬取完毕第%d条" % (i))

        except:
            print("转换异常")
            continue

    return datalist


# 保存数据到表格
def saveData(datalist, savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('下载链接', cell_overwrite_ok=True)  # 创建工作表

    col = ("序号", "书名", "分类", "作者", "出版社", "格式", "大小", "详情页", "下载地址", "评分", "资源介绍", "资源介绍(去换行)", "封面图片")
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
    book.save(savepath)  # 保存


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


def main(start, end):
    # 1.爬取网页
    datalist = getData(start, end)

    # 2.保存数据
    savepath = "下载链接：" + str(start) + "-" + str(end) + ".xls"  # 当前目录新建XLS，存储进去
    saveData(datalist, savepath)


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    # start = 1001
    # end = 8094

    main(1, 1200)
    main(279900, 282850)
    main(339200, 339600)
    # main(200, 201)
    print("爬取完毕！")
