"""  vtt文件格式：
WEBVTT

1
00:00:02.100 --> 00:00:05.880
那个，打扰了

2
00:00:07.733 --> 00:00:11.544
啊，打扰了

3
00:00:16.006 --> 00:00:19.646
嗯，我是漫咖应召店的咲音
"""

import os
import re


def vtt_to_srt(vtt_path, srt_path, min_duration=1.0):
    """
    将单个LRC文件转换为SRT文件。

    :param lrc_path: LRC文件的路径
    :param srt_path: 要保存的SRT文件的路径
    :param min_duration: 每段歌词的最小持续时间（秒），用于避免时间戳过近导致的重叠
    """
    with open(vtt_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    srt_lines = []

    for i in range(0, len(lines)):
        line = lines[i]
        if i>=2:
            srt_line = line
            srt_lines.append(srt_line)

    with open(srt_path, 'w', encoding='utf-8') as file:
        file.writelines(srt_lines)


def parse_time_str(time_str):
    """
    将时间字符串（如"01:02.345"）解析为秒数。
    注意：此脚本无法解决大于一个小时的 lrc 文件转换问题
    """
    hours = 0
    minutes, seconds = map(float, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds


def format_time_str(seconds):
    """
    将秒数格式化为SRT时间字符串（如"00:01:02,345"）。
    注意：SRT文件使用逗号作为毫秒分隔符。
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = seconds % 60
    milliseconds = int((remaining_seconds - int(remaining_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(remaining_seconds):02d},{milliseconds:03d}"


def convert_vtt_folder_to_srt(folder_path, output_folder_path, min_duration=1.0):
    """
    将指定文件夹下的所有VTT文件转换为SRT文件。
    :param folder_path: 包含VTT文件的文件夹路径
    :param output_folder_path: 存放生成的SRT文件的文件夹路径
    :param min_duration: 每段歌词的最小持续时间（秒）
    """
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(folder_path):
        if filename.endswith('.vtt'):
            vtt_path = os.path.join(folder_path, filename)
            srt_filename = filename.replace('.wav', '').replace('.mp3', '').replace('.vtt', '.srt')
            srt_path = os.path.join(output_folder_path, srt_filename)
            vtt_to_srt(vtt_path, srt_path, min_duration)
            print(f"Converted {vtt_path} to {srt_path}")
            # 删除原来的vtt文件
            os.remove(vtt_path)


# 使用示例
if __name__ == "__main__":
    folder_path = input('请输入包含VTT文件的文件夹完整路径：')
    # output_folder_path = input('请输入存放生成的SRT文件的文件夹完整路径：')
    convert_vtt_folder_to_srt(folder_path, folder_path, min_duration=2.0)
