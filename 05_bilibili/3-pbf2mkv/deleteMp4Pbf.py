import os
import glob

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

def remove_mp4_pbf(path):
    for filename in glob.glob(os.path.join(path, '*.*')):
        if not filename.endswith('.mkv'):
            os.remove(filename)

if __name__ == '__main__':
    # 1.设置根目录
    path = readFile(pathPrefix + "\\" + "epub.txt")
    # 2.找到所有后缀名不为.mkv的文件并删除
    remove_mp4_pbf(path)
