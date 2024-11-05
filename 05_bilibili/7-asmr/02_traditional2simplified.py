"""
Python实战：使用zhconv实现简繁体中文的轻松转换
https://developer.baidu.com/article/details/3331529
"""

import os
import zhconv

def trad_to_simp(trad_path, simp_path):
    """
    将单个繁体中文文件转换为简体中文文件。

    :param lrc_path: LRC文件的路径
    :param srt_path: 要保存的SRT文件的路径
    :param min_duration: 每段歌词的最小持续时间（秒），用于避免时间戳过近导致的重叠
    """
    with open(trad_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    simp_lines = []

    for i in range(0, len(lines)):
        traditional_text = lines[i]
        # 转换为简体
        simplified_text = zhconv.convert(traditional_text, 'zh-cn')
        simp_lines.append(simplified_text)

    with open(simp_path, 'w', encoding='utf-8') as file:
        file.writelines(simp_lines)


def show_files(path, all_files):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            parent_dir = os.path.dirname(cur_path)
            dirname = os.path.basename(cur_path)
            new_path = os.path.join(parent_dir, zhconv.convert(dirname, 'zh-cn'))
            os.rename(cur_path, new_path)
            show_files(new_path, all_files)

    return all_files

def convert_trad_folder_to_simp(folder_path, output_folder_path):
    """
    将指定文件夹下的所有繁体中文文件转换为简体中文文件。
    :param folder_path: 包含繁体中文文件的文件夹路径
    :param output_folder_path: 存放生成的简体中文文件的文件夹路径
    """
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    source_path = folder_path
    for root, dirs, files in os.walk(source_path):
        for filename in files:
            # 1.将原目录下的所有文件名都转换为简体中文
            trad_path = os.path.join(root, filename)
            # 使用splitext分割文件名和后缀
            base_name, file_extension = os.path.splitext(filename)
            base_name = zhconv.convert(base_name, 'zh-cn')
            simp_path = os.path.join(root, base_name+file_extension)
            os.rename(trad_path, simp_path)

            # 2.将字幕文件的内容转换为简体中文
            if filename.endswith('.ass') or filename.endswith('.lrc') or filename.endswith('.srt') or filename.endswith('.vtt'):
                simp_zh_filename = base_name + "_zh" + file_extension
                simp_zh_path = os.path.join(root, simp_zh_filename)
                trad_to_simp(simp_path, simp_zh_path)
                print(f"Converted {simp_path} to {simp_zh_path}")
                # 删除源文件
                os.remove(simp_path)
                os.rename(simp_zh_path, simp_zh_path.replace('_zh', ''))

    # 使用递归更改文件夹名称
    show_files(folder_path,[])



if __name__ == "__main__":
    folder_path = input('请输入包含繁体中文文件的文件夹完整路径：')
    # output_folder_path = input('请输入存放生成的简体中文文件的文件夹完整路径：')
    convert_trad_folder_to_simp(folder_path, folder_path)
