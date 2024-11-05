import os
import re

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))
pathPrefix = up_dir_path


# 将两位或者三位的视频时间戳转换为秒数 1:51:43 00:28
def deal_timestamp(result):
    seconds = 0
    list = result.split(':')
    if len(list) == 2:  # 00:28
        minute = int(list[0])
        second = int(list[1])
        seconds = 60 * minute + second
    elif len(list) == 3:
        hour = int(list[0])
        minute = int(list[1])
        second = int(list[2])
        seconds = 3600 * hour + 60 * minute + second
    return seconds


# 去掉字符串中?后的字符
def remove_characters_after_question_mark(s):
    if '?' in s:
        return s.split('?', 1)[0]
    else:
        return s


def add_url(baseUrl, originPath, dealPath):
    f1 = open(originPath, encoding='utf-8')
    f2 = open(dealPath, 'w', encoding='utf-8')

    # 利用循环全部读出
    while 1 > 0:
        line = f1.readline()
        if line == "":
            break

        # 1.若该行为链接，则更新当前的baseurl
        findUrl = re.compile(r'https://www.bilibili.com')
        list = re.findall(findUrl, line)
        if (len(list) != 0):
            line = remove_characters_after_question_mark(line)
            line = str(line).replace('\n', '').rstrip('/')
            baseUrl = line
            continue

        f2.write(line.strip() + '\n')

        # 2.若存在链接，则进行转换，并写入f2文件中
        findTimegap = re.compile(r'\d\d:\d\d')
        list = re.findall(findTimegap, line)
        url_list = []
        if (len(list) != 0):
            # 2.1 替换掉所有的括号
            line = str(line).replace(')', '')
            line = str(line).replace('(', ' ').replace('~', ' ')
            line = str(line).replace('\n', '').replace('\t', ' ')

            list = line.split(' ')
            # 2.2 按空格进行分割，如果有时间戳则进行转换
            for i in range(0, len(list)):
                result = list[i]
                temp1 = re.findall(findTimegap, result)
                if (len(temp1) != 0):  # 带有时间戳
                    findSharp = re.compile(r'#')
                    temp2 = re.findall(findSharp, result)
                    if (len(temp2) != 0):  # 带有#号 30#00:28
                        list1 = result.split('#')
                        pages = list1[0]
                        timestamp = list1[len(list1) - 1]
                        seconds = deal_timestamp(timestamp)
                        url = baseUrl + '/?p=' + pages + '&t=' + str(seconds)
                    else:  # 不带#号 1:51:43
                        seconds = deal_timestamp(result)
                        url = baseUrl + '/?t=' + str(seconds)
                    url_list.append(url)
                else:  # 文字或者其他
                    continue
        # 3.写出url
        if (len(url_list) != 0):
            for i in range(0, len(url_list)):
                url = url_list[i]
                f2.write(url + '\n')

    f1.close()
    f2.close()


if __name__ == "__main__":
    baseUrl = 'https://www.bilibili.com/video/BV1vd4y1J7Ey'

    originPath = pathPrefix + "\\" + "input.txt"
    dealPath = pathPrefix + "\\" + "output.txt"

    add_url(baseUrl, originPath, dealPath)
