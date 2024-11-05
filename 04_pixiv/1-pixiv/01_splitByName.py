import numpy as np
import pickle, glob
import os  # 导入创建文件夹模块
import shutil
import re

# {page_title}/{bmk_1000}&{user}&{date}&{id}

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))
pathPrefix = up_dir_path


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


# 拆分标签
def seplabel(fname):
    # .前面的字符
    filestr = fname.split(".")[0]
    # -前面的字符
    label = str(filestr.split("&")[0])
    return label


# 把图片中的类别总个数找出来，即要创建多少个文件夹
def labelnum(fname):  # C:/Users/sinyjam/Desktop/xingzuotu/*.jpg
    # 图片数记录
    num = len(imglist)
    labelnumber = []
    maxlabel = 0
    for i in range(0, num):
        imglist2 = os.path.basename(imglist[i])  # 获取路径下图片名称
        a = seplabel(imglist2)
        labelnumber.append(a)
        set(labelnumber)
        # set去除多余元素，最后数量为[1,2,3,4,5]
        num = len(set(labelnumber))
    return num


# 把图片中的类别保存下来
def labellist(fname):  # C:/Users/sinyjam/Desktop/xingzuotu/*.jpg
    # 图片数记录
    num = len(imglist)
    labelnumber = []
    labelnumberlist = []
    maxlabel = 0
    for i in range(0, num):
        imglist2 = os.path.basename(imglist[i])  # 获取路径下图片名称
        a = seplabel(imglist2)
        labelnumber.append(a)
        set(labelnumber)
        # set去除多余元素，最后数量为举例：[1,2,3,4,5] 5个
    labelnumberlist = set(labelnumber)
    return labelnumberlist


# 创建文件夹
def createfilefloder(path, fname):
    # path = 'C:/Users/sinyjam/Desktop/xingzuotu2/'  # 设置创建后文件夹存放的位置
    for i in labellist(fname):  # 这里创建类别个数个文件夹
        # *定义一个变量判断文件是否存在,path指代路径,str(i)指代文件夹的名字*
        isExists = os.path.exists(path + str(i))
        if not isExists:  # 判断如果文件不存在,则创建
            os.makedirs(path + str(i))
            print("%s 目录创建成功" % i)
        else:
            print("%s 目录已经存在" % i)
            continue  # 如果文件不存在,则继续上述操作,直到循环结束


# 读取文件并且复制文件到相应的文件夹,
# 这里的fname2不能是全路径到jpg，最后是文件夹"/"结尾
# C:/Users/sinyjam/Desktop/xingzuotu
def readImgAndSave(path):
    ls = os.listdir(path)
    for i in ls:
        if os.path.isfile(path + '/' + i):
            print(i)
            istr = i.split(".")[0]
            label = istr.split("&")[0]
            dst = os.path.join(path, label)
            new_image = os.path.join(dst, i)
            # print(istr)
            # print(label)
            if not os.path.exists(new_image):
                shutil.move(path + '/' + i, path + '%s' % label + '/')
            else:
                images = os.listdir(dst)
                max_serial = -1
                for im in images:
                    _, serial_num = im.split('-')[0], im.split('-')[1]
                    theNum = re.compile('0*([1-9][0-9]*)').findall(serial_num)[0]
                    max_serial = max(max_serial, int(theNum))
                max_serial += 1
                new_name = label + '-' + str(max_serial).zfill(4) + '.jpg'
                new_file_path = os.path.join(dst, new_name)
                shutil.copy(path + '/' + i, new_file_path)


if __name__ == "__main__":
    source_path = readFile(pathPrefix + "\\" + "resource.txt")

    source_path = source_path + "/"
    imglist = glob.glob(source_path + "/*.*")

    # 根据类别数创造文件夹
    createfilefloder(source_path, labelnum(imglist))
    # 打印list里有哪些
    readImgAndSave(source_path)
