# ehentai链接爬取: 读取no_download_file.txt中的种子hash值，得到对应的详情页链接追加到download_url.txt中
# -*- codeing = utf-8 -*-

import xlrd  # 读取excel
import os

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
pathPrefix = up_dir_path + "\\" + "torrents"
folderName = ''


# index: 某一列的索引数
def readExcel(path, index):
    # 打开excel
    readbook = xlrd.open_workbook(path)
    # 确定sheet页
    sheet = readbook.sheet_by_index(0)

    col = sheet.col_values(index, 1)
    return col


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


def getDiffList(list1, list2):
    list = []
    for i in range(0, len(list1)):
        for j in range(0, len(list2)):
            if list1[i] == list2[j]:
                list.append(i)
                continue

    return list


# 保存数据到文件中
def writeFile(path, list):
    f = open(path, "a")

    # 下载链接
    for i in range(0, len(list)):
        f.write(list[i])
        f.write('\n')

    f.close()


def getList(baseUrlList, indexList):
    downloadUrlList = []
    for i in range(0, len(indexList)):
        index = indexList[i]
        downloadUrlList.append(baseUrlList[index])
    return downloadUrlList


def getHash(baseNameList):
    list = []
    for i in range(0, len(baseNameList)):
        url = baseNameList[i]
        if url != '':
            li = url.split('/')
            url = url.split('/')[5].replace('.torrent','')
        list.append(url)

    return list


def main(base_excel_path, no_download_path, download_url_path):
    # 1.读取excel文件
    baseNameList = readExcel(base_excel_path, 16)
    baseNameList = getHash(baseNameList)
    baseUrlList = readExcel(base_excel_path, 11)

    # 2.读取未下载的文件名
    noDownloadFileList = readFile(no_download_path)

    # 3.比较得到差集
    indexList = getDiffList(baseNameList, noDownloadFileList)
    downloadUrlList = getList(baseUrlList, indexList)

    # 4.保存下载链接
    writeFile(download_url_path, downloadUrlList)


if __name__ == "__main__":  # 当程序执行时
    base_excel_path = pathPrefix + "\\" + "02_download" + ".xls"
    no_download_path = pathPrefix + "\\" + "no_download_file" + ".txt"
    download_url_path = pathPrefix + "\\" + "03_download_url" + ".txt"

    main(base_excel_path, no_download_path, download_url_path)

    print("执行完毕！")
