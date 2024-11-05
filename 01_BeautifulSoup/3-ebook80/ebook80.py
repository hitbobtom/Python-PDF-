# 80电子书链接爬取
# -*- codeing = utf-8 -*-

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作

findLink = re.compile(r'<a href="(.*?)" target="_blank')  # 创建正则表达式对象，标售规则   影片详情链接的规则
findPDFName = re.compile(r'<h1>(.*?)</h1>')
findCategory = re.compile(r'<a class="dc" href=".*.epub">(.*?)</a>')
findImg = re.compile(r'<img.*src="(.*?)" style')
findAuthor = re.compile(r'作者：(.*?)</p>')
findPress = re.compile(r'出版社：(.*?)</p>')
findSubtitle = re.compile(r'副标题：(.*?)</p>')
findPublicationYear = re.compile(r'出版年：(.*?)</p>')
findFormat = re.compile(r'电子书格式：(.*?)</p>')
findISBN = re.compile(r'ISBN：(.*?)</p>')


def main(start, end):
    # 1.爬取网页
    datalist = getData(start, end)

    # 2.保存数据
    savepath = "下载链接：" + str(start) + "-" + str(end) + ".xls"  # 当前目录新建XLS，存储进去
    saveData(datalist, savepath)


# 爬取网页
def getData(start, end):
    datalist = []  # 用来存储爬取的网页信息

    # 1.1 要爬取的详情页

    baseurl1 = "http://www.ebook80.com/index.php?c=content&a=show&id="
    # 1.2 要爬取的下载链接
    baseurl2 = "http://www.ebook80.com/index.php?c=download&id="

    for i in range(start, end + 1):
        print("开始爬取第%d条" % (i))

        try:
            data = []  # 保存一个PDF所有信息
            # 序号
            data.append(i)

            # 2.1 要爬取的详情页
            url1 = baseurl1 + str(i)
            html1 = askURL(url1)  # 保存获取到的网页源码

            # 逐一解析数据
            soup1 = BeautifulSoup(html1, "epub.parser")

            item1 = soup1.findAll('div', class_="logbox")[0]
            item1 = str(item1)
            # PDF名称
            pdfName = re.findall(findPDFName, item1)[0]
            data.append(pdfName.replace('《', '').replace('》', ''))
            # 分类
            category = re.findall(findCategory, item1)[0]  # 通过正则表达式查找
            data.append(category)

            item2 = soup1.findAll('div', class_="logcon")[0]
            item2 = str(item2)
            # 作者
            author = re.findall(findAuthor, item2)[0]
            data.append(author)
            # 出版社
            press = re.findall(findPress, item2)[0]
            data.append(press)
            # 副标题
            subtitle = re.findall(findSubtitle, item2)[0]
            data.append(subtitle)
            # 出版年
            publicationYear = re.findall(findPublicationYear, item2)[0]
            data.append(publicationYear)
            # 格式
            format = re.findall(findFormat, item2)[0]
            data.append(format)
            # ISBN
            ISBN = re.findall(findISBN, item2)[0]
            data.append(ISBN)

            item3 = soup1.findAll('div', class_="logcon")[1]
            item3 = str(item3).replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace('<span>', '').replace('</span>', '') \
                .replace('<h2>', '').replace('</h2>', '') \
                .replace('<div>', '').replace('</div>', '') \
                .replace('\"<div class=""logcon"">', '') \
                .replace('<div class="logcon">', '') \
                .replace(' ', '').replace('</a>', '') \
                .replace('<p>', '').replace('</p>', '')

            # new_text = re.sub(r"<a href=""/index\.php\?c=tag&amp;a=list&amp;kw=[a-zA-Z]{0,30}"" target=""_blank"">", "", item3)
            # logcon
            data.append(item3)

            # 2.2 要爬取的下载链接
            url2 = baseurl2 + str(i)
            html2 = askURL(url2)  # 保存获取到的网页源码

            # 逐一解析数据
            soup2 = BeautifulSoup(html2, "epub.parser")
            item = soup2.findAll('div', class_="boxbody")[0]
            item = str(item)

            # 下载链接
            downloadLink = re.findall(findLink, item)[0]  # 通过正则表达式查找
            data.append(downloadLink)

            # 保存到集合中
            datalist.append(data)
        except:
            print("转换异常")
            continue

        print("爬取完毕第%d条" % (i))

    return datalist


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


# 保存数据到表格
def saveData(datalist, savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('下载链接', cell_overwrite_ok=True)  # 创建工作表

    col = ("id", "书名", "分类", "作者", "出版社", "副标题", "出版年", "格式", "ISBN", "logcon", "下载链接")
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


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    # start = 1001
    # end = 8094

    # main(1000, 1999)
    # main(2000, 2999)
    # main(3000, 3999)
    # main(4000, 4999)
    # main(5000, 5999)
    # main(6000, 6999)
    # main(7000, 7999)
    # main(8000, 8094)
    main(4709, 5802)

    print("爬取完毕！")
