"""
按照音声文件的文件命名给pr导出的mp4文件命名
"""

import os
import shutil

def copy_and_rename(src_path, dest_dir, new_name):
    """
    将文件从src_path复制到dest_dir，并重命名为new_name
    """
    dest_path = os.path.join(dest_dir, new_name)
    shutil.copy2(src_path, dest_path)

def rename_from_audioFolder_to_mp4Folder(audio_folder_path, mp4_folder_path):
    audio_list = []
    mp4_list = []

    # 1.音频文件
    for filename in os.listdir(audio_folder_path):
        if filename.endswith('.mp3') or filename.endswith('.wav'):
            audio_list.append(filename)
    # 2.mp4文件
    for filename in os.listdir(mp4_folder_path):
        if filename.endswith('.mp4'):
            timestamp = os.path.getctime(os.path.join(mp4_folder_path, filename))
            mp4_list.append([filename, timestamp])
    # 3.按照文件夹名称排序
    audio_list.sort()
    mp4_list.sort(key=lambda x: x[0])  # 文件夹名称
    # mp4_list.sort(key=lambda x: x[1])    # 创建时间
    # 4.给mp4文件按照顺序重命名
    for i in range(0, len(mp4_list)):
        # mp4的文件名
        mp4_filename = mp4_list[i][0]
        mp4_base_name, mp4_file_extension = os.path.splitext(mp4_filename)
        source_file_path = os.path.join(mp4_folder_path, mp4_filename)
        # 音频文件的文件名
        audio_filename = audio_list[i]
        audio_base_name, audio_file_extension = os.path.splitext(audio_filename)
        audio_base_name = audio_base_name.replace('♪', '').replace('♡', '')
        # mp4的新文件路径
        new_filename = audio_base_name + mp4_file_extension
        destination_folder_path = os.path.join(audio_folder_path, 'mp4')
        # 将文件复制到别的目录并重命名
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)
        copy_and_rename(source_file_path, destination_folder_path, new_filename)
        os.remove(source_file_path)


if __name__ == "__main__":
    audio_folder_path = input('请输入包含音频文件的文件夹完整路径：')
    mp4_folder_path = input('请输入存放生成MP4视频的文件夹完整路径：')
    # mp4_folder_path = 'C:\\Users\\qtf\\Videos\\PR\\output'
    rename_from_audioFolder_to_mp4Folder(audio_folder_path, mp4_folder_path)
