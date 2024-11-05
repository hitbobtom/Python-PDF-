import os

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))
pathPrefix = up_dir_path


# 读取路径文件
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


def covertMkvToMp4(source_folder, destination_folder):
    # 确保目标文件夹存在
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 遍历源文件夹中的所有MKV文件
    for filename in os.listdir(source_folder):
        if filename.endswith('.mkv'):
            # 构建源文件路径和目标文件路径
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, os.path.splitext(filename)[0] + '.mp4')

            # 构建FFmpeg转换命令
            command = f'ffmpeg -i "{source_path}" "{destination_path}"'

            # 打印进度信息
            print(f'Converting {filename} to MP4...')

            # 执行FFmpeg命令
            os.system(command)

            # 打印转换完成信息
            print(f'Converted {filename} to MP4.')


if __name__ == "__main__":
    # 1.定义源文件夹和目标文件夹
    source_folder = readFile(pathPrefix + "\\" + "epub.txt")
    destination_folder = source_folder + "\\" + "mkv"

    # 2.执行转换命令
    covertMkvToMp4(source_folder, destination_folder)
