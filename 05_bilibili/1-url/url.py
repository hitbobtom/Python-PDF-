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


def my_replace(s, old, new, max_replacements=-1):
    # 使用切片来分割字符串，并在需要的地方插入新的子串
    result = s[:]
    start = 0
    count = 0
    while True:
        # 查找旧子串的下一个出现位置
        start = result.find(old, start)
        if start == -1:  # 如果找不到更多的旧子串，则退出循环
            break
        count += 1
        if max_replacements != -1 and count > max_replacements:
            break  # 如果已经替换了足够的次数，则退出循环
        if start != 0:
            char = result[start - 1]
            if char != ' ':
                start += len(new)
                continue
        # 使用新子串替换旧子串
        result = result[:start] + new + result[start + len(old):]
        start += len(new)  # 更新搜索的起始位置
    return result


def add_url(baseUrl, input_path, output_path, md_path):
    f1 = open(input_path, encoding='utf-8')
    f2 = open(output_path, 'w', encoding='utf-8')
    f3 = open(md_path, 'w', encoding='utf-8')

    # 利用循环全部读出
    while 1 > 0:
        line = f1.readline()
        if line == "":
            break

        # 1.若为链接，则更新当前的baseurl
        findUrl = re.compile(r'https://www.bilibili.com')
        list = re.findall(findUrl, line)
        if (len(list) != 0):
            line = remove_characters_after_question_mark(line)
            line = str(line).replace('\n', '').rstrip('/')
            baseUrl = line
            continue

        f2.write(line.strip() + '\n')

        # 2.若存在链接，则进行转换，并写入f2文件中
        findTimegap = re.compile(r'(\d+#)?(\d+:)?(\d+:\d+)')
        list = re.findall(findTimegap, line)
        url_list = []
        if (len(list) != 0):
            for i in range(0, len(list)):
                turtle = list[i]
                pages = str(turtle[0]).replace('#', '')
                hour = str(turtle[1])
                minute_second = str(turtle[2])
                timestamp = hour + minute_second
                if len(pages) != 0:
                    # 带有#号 30#00:28
                    seconds = deal_timestamp(timestamp)
                    url = baseUrl + '/?p=' + pages + '&t=' + str(seconds)
                else:
                    # 不带#号 1:51:43
                    seconds = deal_timestamp(timestamp)
                    url = baseUrl + '/?t=' + str(seconds)
                url_list.append(url)
            # 3.写出url
            for i in range(0, len(url_list)):
                url = url_list[i]
                f2.write(url + '\n')
            # 4.写出md
            for i in range(0, len(list)):
                url = url_list[i]
                turtle = list[i]
                timestamp = turtle[0] + turtle[1] + turtle[2]
                new_timestamp = '[' + timestamp + ']' + '(' + url + ')'
                line = my_replace(line, timestamp, new_timestamp)

        f3.write(line.strip() + '\n\n')

    f1.close()
    f2.close()
    f3.close()


if __name__ == "__main__":
    baseUrl = 'https://www.bilibili.com/video/BV1vd4y1J7Ey'

    input_path = os.path.join(pathPrefix, "input.txt")
    output_path = os.path.join(pathPrefix, "output.txt")
    md_path = r'C:\Users\qtf\Desktop\04_code\python\python-pdf\README.md'

    add_url(baseUrl, input_path, output_path, md_path)
