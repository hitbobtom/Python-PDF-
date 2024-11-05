import datetime
import os
from pathlib import Path

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))
pathPrefix = up_dir_path


def is_valid_line(line):
    # 定义你的验证逻辑，例如，检查是否包含特定数量的分隔符
    # 以下是一个示例，它假设每行至少应包含一个等号和两个星号
    return line.count('=') >= 1 and line.count('*') >= 2


def pbf_to_mkv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-16-le') as s:
        lines = s.readlines()
    chapters = []
    for line in lines:
        # 忽略不符合条件的行
        if not is_valid_line(line):
            continue

        ####### 提取"="符号前的数字，数字+1，然后转换为2位的十进制数
        num = int(line.split("=")[0]) + 1
        num = str(num).zfill(2)

        ####### 时间戳转换
        # 提取"="和"*"之间的数字
        timestamp = int(line.split("=")[1].split("*")[0])
        # 将时间戳转换为时间差
        td = datetime.timedelta(milliseconds=timestamp)
        # 计算小时、分钟、秒和毫秒
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        seconds, millis = divmod(seconds, 1)
        # 转换为00:00:00.000格式的时间
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{int(millis * 1000):03d}"

        ####### 提取两个"*"之间的字符作为章节名
        content = line.split("*", 1)[1].split("*")[0]

        ####### 合并章节名

        chapters.append((f'CHAPTER{num}={time_str}', f'CHAPTER{num}NAME={content}'))

        ####### 写入OGM风格的简易章节文件
        with open(output_file, 'w', encoding='utf-8') as f:
            for chapter in chapters:
                f.write(f'{chapter[0]}' + '\n')
                f.write(f'{chapter[1]}' + '\n')


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

def readPdfFile(directory):
    # 获取所有文件和文件夹
    files = [f for f in Path(directory).iterdir() if f.is_file()]
    pbf_file_list = []

    for i in range(0, len(files)):
        fileName = files[i].name
        if ('.pbf' in fileName):
            pbf_file_list.append(fileName)

    return pbf_file_list


if __name__ == '__main__':
    # 1.设置根目录
    path = readFile(pathPrefix + "\\" + "epub.txt")

    # 2.读取路径下所有的pbf文件
    pbf_file_list = readPdfFile(path)
    if (len(pbf_file_list) != 0):
        for i in range(0, len(pbf_file_list)):
            input_file = path + "\\" + pbf_file_list[i]
            output_file = os.path.splitext(input_file)[0] + '.txt'
            pbf_to_mkv(input_file, output_file)

