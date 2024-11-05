"""  ass文件格式：
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:04.88,0:00:07.94,Default,,0,0,0,,什么嘛　原来泽村同学的TOP ONE就这样？
Dialogue: 0,0:00:13.22,0:00:15.82,Default,,0,0,0,,真后悔自己居然看到第三话
Dialogue: 0,0:00:15.82,0:00:19.02,Default,,0,0,0,,怎么看都是神作吧
"""

import os
import re
from tqdm import trange


def read_ass_file(ass_path):
    # function: read the ass file into python
    # input: filename
    # output: 
    # f_ass = open(ass_name,'r',encoding="utf-16-le")
    f_ass = open(ass_path, 'r', encoding="utf-8")
    subtitle = f_ass.readlines()
    f_ass.close()
    return subtitle


def find_event(subtitle):
    # function: find the beginning of the [Event]
    # input: subtitle
    # output: event
    new_subtitle = []
    for i in range(len(subtitle)):
        if "[Events]" in subtitle[i]:
            print("[Events]:from {}th line".format(i + 1))
            print("\n")
            new_subtitle = subtitle[i:]
            break
    return new_subtitle


def get_format(new_subtitle):
    # function: get the structure of the event
    # exzample: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
    # input: new_subtitle
    # output: text_num, i.e. the index of Text in the format
    text_num = -9999
    line_num = 1
    for i in range(1, len(new_subtitle)):
        if "Format" in new_subtitle[i]:
            line_num = i
            break
    if "Format" in new_subtitle[line_num]:
        subtitle_format = new_subtitle[line_num].split(":")[1].split(",")
        # strip the space and "\n"
        for i in range(len(subtitle_format)):
            subtitle_format[i] = subtitle_format[i].strip()
        if "Text" in subtitle_format:
            text_num = subtitle_format.index("Text")
        print("The subtitle structure is {}".format(subtitle_format))
    else:
        print("the structrue of the subtitle can not be processed by this py file")
    return text_num


def line_filter(line):
    if len(line) == 0:
        return 1
    if ("Dialogue") not in line:
        return 1
    else:
        return 0


def get_time_and_text(new_subtitle, text_num):
    time_text = []
    for i in range(2, len(new_subtitle)):
        # 1.添加行自定义过滤条件
        line = new_subtitle[i].strip()
        if line_filter(line) == 1:
            continue

        # 2.获取开始、结束时间、文本
        start = "0" + line.split(",")[1] + "0"
        end = "0" + line.split(",")[2] + "0"
        text = "".join(line.split(",")[text_num:])
        # the information out of the {} is what we need
        p = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", text)
        p = p.lstrip()
        if len(p) == 0:
            continue
        # print('p:{}'.format(p))
        # whether the subtitle is bi-languange
        if "\\N" in p:
            language_a = p.split("\\N")[0]
            language_b = p.split("\\N")[1]
        else:
            language_a = p
            language_b = ""
        if type(language_a) is str and type(language_b) is str:
            pass
        else:
            print('第{}句字幕不是str格式'.format(i))
            print('a:{}'.format(language_a))
            print('b:{}'.format(language_b))

        # 3.将文本添加到数组中
        time_text.append([str(i - 1), "{} --> {}".format(start, end), language_a + "\n"])

    return time_text


def get_srt_subtitle(time_text):
    srt_subtitle = []
    print("Preparing the srt subtitle...")
    for i in trange(len(time_text)):
        # srt_subtitle.append("\n".join(time_text[i]))
        srt_line = str(i + 1) + "\n" + time_text[i][1] + "\n" + time_text[i][2] + "\n"
        srt_subtitle.append(srt_line)
    print("\n")
    return srt_subtitle


def write_srt(srt_path, srt_subtitle):
    f_srt = open(srt_path, 'w', encoding="utf-8")
    f_srt.writelines(srt_subtitle)
    f_srt.close()


def ass_to_srt(ass_path, srt_path):
    subtitle = read_ass_file(ass_path)
    new_subtitle = find_event(subtitle)

    if new_subtitle == []:
        print("Attention!!!!!!")
        print("There is no Event in ass file, please check the file")

    text_num = get_format(new_subtitle)
    print("Text is the {}th of the event".format(text_num + 1))
    if text_num == -9999:
        print("Attention!!!!")
        print("There is no format in event!")

    time_text = get_time_and_text(new_subtitle, text_num)
    srt_subtitle = get_srt_subtitle(time_text)
    print("The content of srt is finished")

    write_srt(srt_path, srt_subtitle)
    print("Done! You can find {}".format(srt_path))


def convert_ass_folder_to_srt(folder_path, output_folder_path):
    """
    将指定文件夹下的所有ASS文件转换为SRT文件。
    :param folder_path: 包含ASS文件的文件夹路径
    :param output_folder_path: 存放生成的SRT文件的文件夹路径
    """
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(folder_path):
        if filename.endswith('.ass'):
            ass_path = os.path.join(folder_path, filename)
            srt_filename = filename.replace('.ass', '.srt')
            srt_path = os.path.join(output_folder_path, srt_filename)
            ass_to_srt(ass_path, srt_path)
            print(f"Converted {ass_path} to {srt_path}")


if __name__ == "__main__":
    folder_path = input('请输入包含ASS文件的文件夹完整路径：')
    output_folder_path = input('请输入存放生成的SRT文件的文件夹完整路径：')
    convert_ass_folder_to_srt(folder_path, output_folder_path)
