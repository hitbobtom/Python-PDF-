# 处理pdf书签
# -*- codeing = utf-8 -*-

import re  # 正则表达式，进行文字匹配`
import os

pathPrefix = os.path.abspath('../../03_Bookmark/demo')


def readFile(path):
    list = []
    f4 = open(path, encoding='utf-8')
    # 利用循环全部读出
    while 1 > 0:
        line = f4.readline()
        if line == '':
            break
        line = line.strip().replace('\n', '')
        list.append(line)

    f4.close()
    return list


# 保存数据到文件中
def writeFile(path, list):
    f = open(path, "w", encoding='utf-8')

    # 下载链接
    for i in range(0, len(list)):
        f.write(list[i])
        if i != len(list) - 1:
            f.write('\n')

    f.close()


# 缩进
def indentation(s):
    list = s.split(' ')
    if len(list) >= 2:
        nav = list[0]
        list1 = nav.split('.')
        length = len(list1)

        for i in range(0, length - 1):
            s = "\t" + s

    return s


def main(pdf_list):
    list = []
    # 调用函数
    for i in range(0, len(pdf_list)):
        # 添加缩进
        s = indentation(pdf_list[i])
        list.append(s)

    return list


if __name__ == "__main__":  # 当程序执行时

    pdf_list = readFile(pathPrefix + "\\" + "1.txt")

    list = main(pdf_list)

    result_path = pathPrefix + "\\" + "2.txt"
    writeFile(result_path, list)

    print("处理完毕！")
