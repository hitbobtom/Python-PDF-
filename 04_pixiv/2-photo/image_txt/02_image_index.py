import os


def read_txt_file(txt_path):
    line_list = []
    f_txt = open(txt_path, 'r', encoding="utf-8")
    while 1 > 0:
        line = f_txt.readline()
        if line == '':
            break
        line_list.append(line)
    f_txt.close()
    return line_list


def write_txt(folder_path, line_list):
    txt_path = os.path.join(folder_path, '02_image_index.txt')
    f_txt = open(txt_path, 'w', encoding="utf-8")
    file_extensions = [".png", ".jpg", ".jpeg"]

    index = 1
    paragraph = 1

    for i in range(0, len(line_list)):
        line = line_list[i].strip()
        if len(line) == 0:
            index = 1
            paragraph += 1
            continue
        # 首行
        if not any(file_extension in line for file_extension in file_extensions):
            f_txt.write('0' + ' ' + line + '\n')
        else:
            if index == 1:
                f_txt.write('第' + str(paragraph) + '章 ' + line.split('.')[0] + '\n')
            f_txt.write(str(paragraph) + '.' + str(index) + ' ' + line.split('.')[0] + '\n')
            f_txt.write(line  + '\n')
            index += 1

    f_txt.close()


def generate_image_index(folder_path):
    line_list = read_txt_file(os.path.join(folder_path, '01_image_list.txt'))
    write_txt(folder_path, line_list)
    print("Done! You can find {}".format(folder_path))


if __name__ == "__main__":
    folder_path = input('请输入包含小说文件的文件夹完整路径：')
    generate_image_index(folder_path)
