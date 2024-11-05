import os
import re
from pathlib import Path

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


# 提取时间戳
def extractTimestamp(originPath, dealPath):
    f1 = open(originPath, encoding='utf-8')
    f2 = open(dealPath, 'w', encoding='utf-8')

    list = []
    pbfPath = ''

    # 1.读取每一行，将读到的时间戳保存到list中
    while 1 > 0:
        line = f1.readline()
        if line == "":
            break

        # 若该行存在 【"key": 】，则提取出来
        findUrl = re.compile(r'"key": [\d]+')
        temp = re.findall(findUrl, line)
        if (len(temp) != 0):
            line = str(line).replace('"key": ', '')
            list.append(int(line))

        # 若该行存在文件名，则提取出来
        findFileNamePath = re.compile(r'fileNamePath')
        temp2 = re.findall(findFileNamePath, line)
        if (len(temp2) != 0):
            filePath = line.split('"')[3]
            pbfPath = os.path.splitext(filePath)[0] + '.pbf'

    # 2.对list集合从小到大进行排序
    list.sort()

    # 3.将list转换为时分秒格式输出到t1文件夹中
    for i in range(0, len(list)):
        result = list[i]
        result = convertTime(result)
        f2.write(result)
        f2.write(' ')
        f2.write('\n')

    # 4.在视频所在的文件夹中新建同名的.pbf书签文件
    f3 = open(pbfPath, 'w', encoding='utf-8')
    f3.write('[Bookmark]\n')
    for i in range(0, len(list)):
        result = list[i]
        f3.write(str(i) + '=')
        f3.write(str(result) + '* *')
        f3.write('\n')

    f1.close()
    f2.close()
    f3.close()


def list_files(directory, sort_by='name'):
    # 获取所有文件和文件夹
    files = [f for f in Path(directory).iterdir() if f.is_file()]

    # 根据不同的排序方式进行排序
    if sort_by == 'name':
        files.sort(key=lambda x: x.name)
    elif sort_by == 'mtime':
        files.sort(key=lambda x: x.stat().st_mtime)  # 修改时间
    elif sort_by == 'size':
        files.sort(key=lambda x: x.stat().st_size)  # 文件大小
    else:
        raise ValueError("Invalid sort option. Choose 'name', 'mtime', or 'size'.")

    return files


# 读取文件名称排序最大的json文件
def readJson(originPath):
    fileList = list_files(originPath, sort_by='name')
    fileNameList = []
    for i in range(0, len(fileList)):
        fileName = fileList[i].name
        if ('.json' in fileName):
            fileNameList.append(fileList[i].name)
    return fileNameList[len(fileNameList) - 1]


if __name__ == "__main__":
    # 1.设置根目录
    path = readFile(pathPrefix + "\\" + "epub.txt")

    # 2.读取路径下所有的json文件，选择最大的一个
    originPath = path + "\\" + readJson(path)
    dealPath = pathPrefix + "\\" + "t2.txt"

    # 3.提取时间戳
    extractTimestamp(originPath, dealPath)
