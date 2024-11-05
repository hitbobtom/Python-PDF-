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
from tqdm import trange
from pydub import AudioSegment
from mutagen.mp3 import MP3
import wave
from Levenshtein import distance

REGEX_CONTENT = r"\[(\d{2}:\d{2}(.\d+)?)\]"
REGEX_NO_CONTENT = r"\[(\d{2}:\d{2}(.\d+)?)\]$"


def read_lrc_file(lrc_path):
    subtitle = []
    f_lrc = open(lrc_path, 'r', encoding="utf-8")
    # 利用循环全部读出
    while 1 > 0:
        line = f_lrc.readline()
        if line == '':
            break
        if ('汉化' or '字幕') in line:
            continue
        line = line.strip().replace('﻿', '')
        content_match = re.search(REGEX_CONTENT, line)
        if content_match is not None:
            subtitle.append(line)
    f_lrc.close()
    return subtitle


def write_srt(srt_path, srt_lines):
    f_srt = open(srt_path, 'w', encoding="utf-8")
    f_srt.writelines(srt_lines)
    f_srt.close()


def get_srt_subtitle(time_text):
    srt_subtitle = []
    print("Preparing the srt subtitle...")
    for i in trange(len(time_text)):   # python中添加进度条--trange的使用
        srt_line = str(i + 1) + "\n" + time_text[i][0] + "\n" + time_text[i][1] + "\n"
        srt_subtitle.append(srt_line)
    print("\n")
    return srt_subtitle


def get_closest_filename(target_filename, filename_list):
    closest_dist = float('inf')
    closest_name = None
    for name in filename_list:
        dist = distance(target_filename, name)
        if dist < closest_dist and dist != 0:
            closest_dist = dist
            closest_name = name
    return closest_name


def get_wav_duration(file_path):
    wave_file = wave.open(file_path, 'rb')
    num_frames = wave_file.getnframes()
    sample_rate = wave_file.getframerate()
    duration = num_frames / float(sample_rate)
    wave_file.close()
    return duration


def get_mp3_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length


def get_audio_duration(folder_path, filename):
    # 获取与歌词文件最接近的音频文件名
    audio_filename = get_closest_filename(filename, os.listdir(folder_path))
    audio_path = os.path.join(folder_path, audio_filename)
    audio_length = 0.0
    # 获取音频长度
    if audio_path.endswith('.mp3'):
        audio_length = get_mp3_duration(audio_path)
    if audio_path.endswith('.wav'):
        try:
            audio_length = get_wav_duration(audio_path)
        except:
            audio = AudioSegment.from_file(audio_path)
            audio_length = len(audio)
    return audio_length


def get_element(start_time_str, end_time_str, text, min_duration=0.1):
    start_time = parse_time_str(start_time_str)
    end_time = parse_time_str(end_time_str)
    # text = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", text)
    if end_time - start_time < min_duration:
        # 如果时间差小于最小持续时间，则调整结束时间为当前时间加上最小持续时间
        end_time_str = format_time_str_srt(start_time + min_duration)
    return ["{} --> {}".format(start_time_str, end_time_str), ''.join(text) + "\n"]


def get_time_and_text(subtitle, audio_length, min_duration=0.1):
    """
        获取时间与文本
        :param min_duration: 每段歌词的最小持续时间（秒），用于避免时间戳过近导致的重叠
        """
    time_text = []

    for i in range(0, len(subtitle)):
        line = subtitle[i]
        # 跳过内容为空的行
        content_match = re.search(REGEX_NO_CONTENT, line)
        if content_match is not None:
            continue

        start_time_match = re.search(REGEX_CONTENT, line)
        # 2.判断下一行是否有内容（除最后一行外）
        if i < len(subtitle) - 1:
            next_line = subtitle[i + 1]
            next_line = next_line.strip()

            end_time_match_1 = re.search(REGEX_NO_CONTENT, next_line)
            end_time_match_2 = re.search(REGEX_CONTENT, next_line)
            # 获取时间与文本
            start_time_str = start_time_match.group(1)
            if end_time_match_1 is not None:
                end_time_str = end_time_match_1.group(1)
            else:
                end_time_str = end_time_match_2.group(1)
            text = line[start_time_match.end():].strip()

            element = get_element(start_time_str, end_time_str, text)
            time_text.append(element)

        # 3.处理最后一行，此时需要读取对应音频文件的时长
        if i == len(subtitle) - 1:
            # 获取时间与文本
            start_time_str = start_time_match.group(1)
            end_time_str = format_time_str_lrc(audio_length)
            text = line[start_time_match.end():].strip()

            element = get_element(start_time_str, end_time_str, text)
            time_text.append(element)

    return time_text


def parse_time_str(time_str):
    """
    将时间字符串（如"01:02.345"）解析为秒数。
    注意：此脚本无法解决大于一个小时的 lrc 文件转换问题
    """
    hours = 0
    minutes, seconds = map(float, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds


def format_time_str_srt(seconds):
    """
    将秒数格式化为SRT时间字符串（如"00:01:02,345"）。
    注意：SRT文件使用逗号作为毫秒分隔符。
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = seconds % 60
    milliseconds = int((remaining_seconds - int(remaining_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(remaining_seconds):02d},{milliseconds:03d}"


def format_time_str_lrc(seconds):
    """
    将秒数格式化为LRC时间字符串（如"27:10.11"）。
    注意：LRC文件使用句号作为毫秒分隔符。
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = seconds % 60
    milliseconds = int((remaining_seconds - int(remaining_seconds)) * 1000)
    return f"{minutes:02d}:{int(remaining_seconds):02d}.{milliseconds:02d}"

def convert_lrc_folder_to_srt(folder_path, output_folder_path, min_duration=1.0):
    """
    将指定文件夹下的所有LRC文件转换为SRT文件。
    :param folder_path: 包含LRC文件的文件夹路径
    :param output_folder_path: 存放生成的SRT文件的文件夹路径
    :param min_duration: 每段歌词的最小持续时间（秒）
    """
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(folder_path):
        if filename.endswith('.lrc'):
            # 1.设置导出的srt文件路径
            lrc_path = os.path.join(folder_path, filename)
            srt_filename = filename.replace('.lrc', '.srt')
            srt_path = os.path.join(output_folder_path, srt_filename)
            # 2.获取对应音频文件的信息
            audio_length = get_audio_duration(folder_path, filename)
            # 3.读取文件并处理
            subtitle = read_lrc_file(lrc_path)
            time_text = get_time_and_text(subtitle, audio_length)
            # 4.写出到srt文件中
            srt_subtitle = get_srt_subtitle(time_text)
            write_srt(srt_path, srt_subtitle)

            print(f"Converted {lrc_path} to {srt_path}")

            # 删除原来的lrc文件
            # os.remove(lrc_path)


# 使用示例
if __name__ == "__main__":
    folder_path = input('请输入包含LRC文件的文件夹完整路径：')
    output_folder_path = input('请输入存放生成的SRT文件的文件夹完整路径：')
    convert_lrc_folder_to_srt(folder_path, output_folder_path, min_duration=2.0)
