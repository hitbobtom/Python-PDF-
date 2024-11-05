"""  lrc文件格式3：
[00:00.41]青春×恋物
[00:02.81]
[00:03.07]纯情
[00:06.73]
[00:07.17]Q：请介绍一下你的名字和年龄
[00:10.10]我的名字叫法条枣。请称呼我为枣。高中三年级，年龄是18岁
"""

import os
import re

REGEX_CONTENT = r"(\d{2}:\d{2}(.\d+)?)"
SCRIPT_INFO = '[by:Arctime字幕软件 Pro 2.4]'


def read_srt_file(srt_path):
    subtitle = []
    f_srt = open(srt_path, 'r', encoding="utf-8")
    # 利用循环全部读出
    while 1 > 0:
        line = f_srt.readline()
        if line == '':
            break
        line = line.strip().replace('﻿', '')
        if len(line) == 0:
            continue
        subtitle.append(line)
    f_srt.close()
    return subtitle


def get_time_and_text(subtitle):
    time_text = []
    for i in range(0, len(subtitle)):
        line = subtitle[i]
        # 跳过内容为数字和文字的行
        content_match = re.search(REGEX_CONTENT, line)
        if content_match is None:
            continue
        next_line = subtitle[i + 1]
        time_list = line.split('-->')
        start_time_str = format_time_str_lrc(time_list[0].strip())
        end_time_str = format_time_str_lrc(time_list[1].strip())
        time_text.append([start_time_str, end_time_str, next_line])

    return time_text


def write_lrc(lrc_path, time_text):
    f_lrc = open(lrc_path, 'w', encoding="utf-8")

    # 1.写入文件头
    f_lrc.write(SCRIPT_INFO + '\n')

    # 2.将数组的每一项写出到正文中
    for i in range(0, len(time_text)):
        Start = time_text[i][0]
        End = time_text[i][1]
        Text = time_text[i][2]
        f_lrc.write('[' + Start + ']' + Text)
        f_lrc.write('\n')
        f_lrc.write('[' + End + ']')
        f_lrc.write('\n')
    f_lrc.close()


def format_time_str_lrc(srt_time_str):
    """
    将SRT时间字符串（00:00:16.006、00:00.41）转换为LRC时间字符串（如"04:53.74"）。
    """
    srt_time_str = srt_time_str.replace(',', '.')
    str = srt_time_str.split('.')[0]
    milliseconds = srt_time_str.split('.')[1]

    list = str.split(':')
    if len(list) == 2:  # 00:00.41
        minutes = list[0]
        seconds = list[1]
    elif len(list) == 3:  # 00:00:16.006
        hour = list[0]
        minutes = int(hour) * 60 + int(list[1])
        minutes = format(minutes)
        seconds = list[2]

    return minutes.zfill(2) + ':' + seconds + '.' + milliseconds[:2]


def srt_to_lrc(srt_path, lrc_path):
    subtitle = read_srt_file(srt_path)
    time_text = get_time_and_text(subtitle)
    write_lrc(lrc_path, time_text)
    print("Done! You can find {}".format(lrc_path))


def convert_srt_folder_to_lrc(folder_path, output_folder_path):
    """
    将指定文件夹下的所有SRT文件转换为LRC文件。
    :param folder_path: 包含SRT文件的文件夹路径
    :param output_folder_path: 存放生成的LRC文件的文件夹路径
    """
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(folder_path):
        if filename.endswith('.srt'):
            srt_path = os.path.join(folder_path, filename)
            lrc_filename = filename.replace('.srt', '.lrc')
            lrc_path = os.path.join(output_folder_path, lrc_filename)
            srt_to_lrc(srt_path, lrc_path)
            print(f"Converted {srt_path} to {lrc_path}")

            # 删除原来的srt文件
            os.remove(srt_path)


# 使用示例
if __name__ == "__main__":
    folder_path = input('请输入包含SRT文件的文件夹完整路径：')
    # output_folder_path = input('请输入存放生成的LRC文件的文件夹完整路径：')
    convert_srt_folder_to_lrc(folder_path, folder_path)
