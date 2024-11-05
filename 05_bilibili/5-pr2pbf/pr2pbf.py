import os
import re

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))
pathPrefix = up_dir_path


# 读取路径文件
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
    return list[0]


# 将带有帧的时间戳转换为时分秒格式  381933  00:06:21.28 ((6*60+21)*30+28)*100/3 00:17:12:08
def convertTime(timestamp):
    list = timestamp.split(':')
    hour = int(list[0])
    minute = int(list[1])
    second = int(list[2])
    frame = int(list[3])

    seconds = hour * 3600 + minute * 60 + second
    frames = (seconds * 30 + frame) * 100

    return frames // 3


def extractBookmark(originPath, dealPath):
    f1 = open(originPath, encoding='utf-16')
    f2 = open(dealPath, 'w', encoding='utf-8')

    f2.write('[Bookmark]\n')

    index = 0
    # 利用循环全部读出
    while 1 > 0:
        line = f1.readline()
        if line == "":
            break

        # 若存在链接，则进行转换，并写入f2文件中
        findTimegap = re.compile(r'\d\d:\d\d:\d\d')
        list = re.findall(findTimegap, line)
        if (len(list) != 0):
            list = line.split('\t\t\t')
            timestamp = convertTime(list[1])
            bookmark = list[2]
            f2.write(str(index) + '=')
            f2.write(str(timestamp) + '*' + bookmark + '*')
            f2.write('\n')
            index = index + 1

    f1.close()
    f2.close()


if __name__ == "__main__":
    # 1.设置根目录
    fileName = readFile(pathPrefix + "\\" + "epub.txt")

    # 2.读取路径下所有的json文件，选择最大的一个
    prWorkPath = "C:\\Users\\qtf\\Videos\\PR"

    originPath = prWorkPath + "\\" + fileName + ".txt"
    dealPath = prWorkPath + "\\" + fileName + ".pbf"

    # 3.提取时间戳
    extractBookmark(originPath, dealPath)

    # 4.删除原来的txt文件
    os.remove(originPath)
