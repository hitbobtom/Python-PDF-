import os
import shutil

# 遍历所有文件夹
def read_img_save(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            # 如果文件是jpg文件
            if (file.endswith('.jpg') or file.endswith('.png')):
                # 构造原始文件路径和目标文件路径
                src_path = os.path.join(root, file)
                dst_path = os.path.join(path, file)
                # 剪切文件到目标文件夹
                shutil.move(src_path, dst_path)


def delete_subfolders(path):
    for item_name in os.listdir(path):
        item_path = os.path.join(path, item_name)
        if os.path.isdir(item_path):
            try:
                os.rmdir(item_path)
                print(f"Subfolder {item_path} has been deleted.")
            except OSError as e:
                print(f"Error: {e.strerror} - {e.filename}")


if __name__ == "__main__":
    folder_path = input('请输入需要合并的文件夹完整路径：')
    read_img_save(folder_path)
    delete_subfolders(folder_path)



