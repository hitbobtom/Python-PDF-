import os


# 按&拆分
# {bmk_1000} & {user} & {date} & {id}
def get_newname(filename):
    base_name, file_extension = os.path.splitext(filename)
    str_list = base_name.split("&")

    id = ''
    date = ''
    for i in range(0, len(str_list)):
        name = str_list[i]
        if '_p' in name:
            pid = name.split("_p")[0]
            no = name.split("_p")[1]
            id = pid + '_p' + str(no).zfill(3)
        if '-' in name:
            date = name

    return id + file_extension


def rename_file(dir_path):
    """
    递归获取所有文件
    :param dir_path:文件夹路径
    :return: 该文件夹下的所有文件的列表
    """
    file_list = os.listdir(dir_path)  # 获取当前文件夹下的所有文件
    for filename in file_list:
        complete_file_name = os.path.join(dir_path, filename)  # 获取包含路径的文件名
        if os.path.isdir(complete_file_name):  # 如果是文件夹
            rename_file(complete_file_name)  # 文件夹递归
        if os.path.isfile(complete_file_name):  # 文件名判断是否为文件
            print(complete_file_name)  # 输出找到的文件的路径
            parent = os.path.dirname(complete_file_name)

            old_name = os.path.join(parent, filename)
            new_name = os.path.join(parent, get_newname(filename))

            os.rename(old_name, new_name)


if __name__ == "__main__":
    folder_path = input('请输入包含pixiv图片的文件夹完整路径：')
    rename_file(folder_path)
