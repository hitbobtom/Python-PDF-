"""
按照音声文件的文件命名给pr导出的wav文件命名，并将原始音频文件移动到‘原版’文件夹中
"""

import os
import shutil


def copy_and_rename(src_path, dest_dir, new_name):
    """
    将文件从src_path复制到dest_dir，并重命名为new_name
    """
    dest_path = os.path.join(dest_dir, new_name)
    shutil.copy2(src_path, dest_path)


def rename_from_audioFolder_to_wavFolder(audio_folder_path, wav_folder_path):
    audio_list = []
    wav_list = []
    backups_folder_path = os.path.join(audio_folder_path, '原版')

    # 1.音频文件
    if not os.path.exists(backups_folder_path):
        os.makedirs(backups_folder_path)
    for filename in os.listdir(audio_folder_path):
        if filename.endswith('.mp3') or filename.endswith('.wav') or filename.endswith('.m4a')or filename.endswith('.aac'):
            audio_list.append(filename)
            # 将原始音频文件移动到‘原版’文件夹中
            audio_path = os.path.join(audio_folder_path, filename)
            shutil.move(audio_path, backups_folder_path)
    # 2.wav文件
    for filename in os.listdir(wav_folder_path):
        if filename.endswith('.wav'):
            timestamp = os.path.getctime(os.path.join(wav_folder_path, filename))
            wav_list.append([filename, timestamp])
    # 3.按照文件夹名称排序
    audio_list.sort()
    wav_list.sort(key=lambda x: x[0])  # 文件夹名称
    # wav_list.sort(key=lambda x: x[1])    # 创建时间
    # 4.给wav文件按照顺序重命名
    for i in range(0, len(wav_list)):
        # wav的文件名
        wav_filename = wav_list[i][0]
        wav_base_name, wav_file_extension = os.path.splitext(wav_filename)
        source_file_path = os.path.join(wav_folder_path, wav_filename)
        # 原始音频文件的文件名
        audio_filename = audio_list[i]
        audio_base_name, audio_file_extension = os.path.splitext(audio_filename)
        # wav的新文件路径
        new_filename = audio_base_name + wav_file_extension
        destination_folder_path = audio_folder_path
        copy_and_rename(source_file_path, destination_folder_path, new_filename)
        print(f"Renamed {wav_filename} to {new_filename}")
        os.remove(source_file_path)


if __name__ == "__main__":
    audio_folder_path = input('请输入包含原始音频文件的文件夹完整路径：')
    # wav_folder_path = input('请输入需要重命名的音频文件的文件夹完整路径：')
    wav_folder_path = r'C:\Users\qtf\Videos\PR\output'
    rename_from_audioFolder_to_wavFolder(audio_folder_path, wav_folder_path)
