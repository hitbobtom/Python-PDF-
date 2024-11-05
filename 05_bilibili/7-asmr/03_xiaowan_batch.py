"""
去掉小丸工具箱批量压制后文件名中的"_batch",并删除源文件
"""

import os

if __name__ == "__main__":
    folder_path = input('请输入包含原始文件的文件夹完整路径：')
    # folder_path = 'C:\\Users\\qtf\\Videos\\PR\\output'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if ('_batch') not in filename:
            os.remove(file_path)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if ('_batch') in filename:
            new_filename = filename.replace('_batch', '')
            new_file_path = os.path.join(folder_path, new_filename)
            os.rename(file_path,new_file_path)

