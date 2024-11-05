import os
import re

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))
pathPrefix = up_dir_path


# 将带有帧的时间戳转换为时分秒格式  381933  00:06:21.28 ((6*60+21)*30+28)*100/3
def convertTime(time):
    # 帧
    frame = round(time * 3 / 100)
    # 取商  381
    seconds = frame // 30
    # 取余数  28
    remainder = frame % 30
    # 计算小时
    hours = seconds // 3600
    # 计算分钟
    minutes = (seconds % 3600) // 60
    # 计算秒钟
    seconds = seconds % 60

    # 输出转换后的结果
    if hours == 0:
        result = str(minutes).zfill(2) + ':' + str(seconds).zfill(2)
    else:
        result = str(hours) + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2)

    return result


def convertBookmarkTotime(originPath, dealPath):
    f1 = open(originPath, encoding='utf-8')
    f2 = open(dealPath, 'w', encoding='utf-8')

    # 利用循环全部读出
    while 1 > 0:
        line = f1.readline()
        if line == "":
            break

        # 若该行是书签，则读取并转换
        findBookmark = re.compile(r'=[\d]+')
        list = re.findall(findBookmark, line)
        if (len(list) != 0):
            # 1.替换掉所有的括号
            line = re.sub(r'.*=', '', line)
            line = str(line).replace('\n', '')

            # 2.按*进行分割，如果有时间戳则进行转换
            lineList = line.split('*')
            timestamp = convertTime(int(lineList[0]))
            bookmark = lineList[1]
            f2.write(timestamp + ' ' + bookmark)
            f2.write('\n')

    f1.close()
    f2.close()


if __name__ == "__main__":
    originPath = pathPrefix + "\\" + "t1.txt"
    dealPath = pathPrefix + "\\" + "t2.txt"

    convertBookmarkTotime(originPath, dealPath)
