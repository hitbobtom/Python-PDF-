import os
import shutil


def read_image(folder_path):
    image_list = []
    file_extensions = [".png", ".jpg", ".jpeg"]
    for filename in os.listdir(folder_path):
        if any(file_extension in filename for file_extension in file_extensions):
            image_list.append(filename)
    return image_list


def move_photo(folder_path, image_list):
    img_path = folder_path + "\\img"
    if os.path.exists(img_path) == False:
        os.makedirs(img_path)
    for i in range(0, len(image_list)):
        filename = image_list[i]
        source_path = os.path.join(folder_path, filename)
        destination_path = os.path.join(img_path, filename)
        shutil.move(source_path, destination_path)


def line_format(line):
    if '_p000' in line:
        line = '\n' + line
    return line


def write_txt(folder_path, image_list):
    txt_path = os.path.join(folder_path, '01_image_list.txt')
    f_txt = open(txt_path, 'w', encoding="utf-8")
    folder = os.path.basename(folder_path)
    f_txt.write(folder + '(' + str(len(image_list)) + 'p)' + '\n')

    for i in range(0, len(image_list)):
        line = line_format(image_list[i])
        f_txt.write(line)
        if i != len(image_list) - 1:
            f_txt.write('\n')
    f_txt.close()


def generate_txt(folder_path):
    # 1.读取所有图片的名称
    image_list = read_image(folder_path)
    # 2.移动图片到同目录的img目录下
    move_photo(folder_path, image_list)
    # 3.写出txt文件
    write_txt(folder_path, image_list)
    print("Done! You can find {}".format(folder_path))


if __name__ == "__main__":
    folder_path = input('请输入包含小说文件的文件夹完整路径：')
    generate_txt(folder_path)
