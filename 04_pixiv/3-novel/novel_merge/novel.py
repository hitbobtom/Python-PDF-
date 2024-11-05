import os
import shutil
import re

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))
pathPrefix = up_dir_path

index = 0

# 1.读取路径文件
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


# 2.合并文件夹
def mergeDir(root_path):
    dir_list = os.listdir(root_path)  # 获取当前文件夹下的所有文件
    for dir_name in dir_list:
        complete_dir_path = os.path.join(root_path, dir_name)  # 获取包含路径的文件名
        if os.path.isdir(complete_dir_path):  # 如果是文件夹
            # 将文件夹下所有文件复制到根目录下
            readFileAndSave(root_path, complete_dir_path)
            # 删除文件夹
            shutil.rmtree(complete_dir_path)


# 遍历所有文件夹
def readFileAndSave(parent_path, path):
    folder_name = os.path.basename(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            # 1.构造原始文件路径和目标文件路径
            src_path = os.path.join(root, file)
            dst_path = os.path.join(parent_path, file)
            # 2.剪切文件到目标文件夹
            shutil.move(src_path, dst_path)
            # 3.重命名txt文件和jpg文件
            old_name = os.path.join(parent_path, file)
            new_name = ''
            if file.endswith('.jpg'):
                new_name = os.path.join(parent_path, folder_name + '.jpg')
            elif file.endswith('.png'):
                new_name = os.path.join(parent_path, folder_name + '.png')
            elif file.endswith('.txt'):
                new_name = os.path.join(parent_path, folder_name + '.txt')
            os.rename(old_name, new_name)


# 3.合并txt文件
def copyToTxt(path, file_name):
    f1 = open(os.path.join(path, file_name), encoding='utf-8')
    f2 = open(os.path.join(path, "merge.txt"), 'a+', encoding='utf-8')

    # 3.1 给每个文件加入章节符
    line = f1.readline()
    global index
    index += 1
    f2.write("第" + str(index) + "章 " + line)

    # 3.2 替换文本中所有的“<”和“>”

    # 利用循环全部读出
    while 1 > 0:
        line = f1.readline()
        if line == "":
            break
        f2.write(line)

    f2.write('\n')
    f1.close()
    f2.close()


def renamePhoto(path, file_name):
    file_name = re.sub(r"\.txt$", "", file_name)
    file_list = os.listdir(path)  # 获取当前文件夹下的所有文件
    for file in file_list:
        if not file.endswith('.txt'):
            # 获取包含路径的文件名
            complete_image_path = os.path.join(path, file)
            # 获取文件后缀
            file_extension = os.path.splitext(file)[1]
            # 去除文件后缀得到不带后缀的文件名
            file_name_without_extension = file.replace(file_extension, "")

            if (file_name == file_name_without_extension):
                new_name = os.path.join(path, "image_" + str(index).zfill(2) + file_extension)
                os.rename(complete_image_path, new_name)
                break


if __name__ == "__main__":
    # 1.设置根目录
    path = input('请输入包含小说文件的文件夹完整路径：')
    # 2.合并根目录下所有文件夹中的文件
    mergeDir(path)
    # 3.遍历所有的文件
    file_list = os.listdir(path)  # 获取当前文件夹下的所有文件
    for file_name in file_list:
        if file_name.endswith('.txt'):
            # 3.1 复制每个txt中的内容到总txt中
            copyToTxt(path, file_name)
            # 3.2 重命名对应的图片
            renamePhoto(path, file_name)
