import os
import shutil

HEAD_CONTENT = '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE epub PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n\n<epub xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<title></title>\n<link href="Styles/Style0001.css" type="text/css" rel="stylesheet"/>\n</head>\n<body>\n<div class="wrap article">'
END_CONTENT = '</div>\n</body>\n</epub>'


def line_format(line):
    # 1.去除文件标识符
    line = line.strip().replace('﻿', '')
    return line


def read_txt_file(txt_path):
    content = []
    f_txt = open(txt_path, 'r', encoding="utf-8")
    # 利用循环全部读出
    while 1 > 0:
        line = f_txt.readline()
        if line == '':
            break
        line = line_format(line)
        if len(line) == 0:
            continue
        content.append(line)
    f_txt.close()
    return content


def write_html(html_path, content):
    f_html = open(html_path, 'w', encoding="utf-8")

    # 1.写入文件头
    f_html.write(HEAD_CONTENT + '\n')
    # 2.将数组的每一项写出到正文中
    for i in range(0, len(content)):
        line = '<p>' + content[i] + '</p>'
        f_html.write(line + '\n')
    # 3.写入文件尾
    f_html.write(END_CONTENT)
    f_html.close()


def copy_css_html(html_path):
    up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))
    css_folder = up_dir_path + "\\Styles"
    html_folder = os.path.dirname(html_path) + "\\Styles"
    shutil.copytree(css_folder, html_folder)


def txt_to_html(txt_path, html_path):
    content = read_txt_file(txt_path)
    copy_css_html(html_path)
    write_html(html_path, content)
    print("Done! You can find {}".format(html_path))


def convert_txt_folder_to_html(folder_path, output_folder_path):
    """
    将指定文件夹下的所有TXT文件转换为HTML文件。
    :param folder_path: 包含TXT文件的文件夹路径
    :param output_folder_path: 存放生成的HTML文件的文件夹路径
    """
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            txt_path = os.path.join(folder_path, filename)
            html_filename = filename.replace('.txt', '.epub')
            html_path = os.path.join(output_folder_path, html_filename)
            txt_to_html(txt_path, html_path)
            print(f"Converted {txt_path} to {html_path}")
            # 删除原来的txt文件
            # os.remove(txt_path)


if __name__ == "__main__":
    folder_path = input('请输入包含小说文件的文件夹完整路径：')
    # output_folder_path = input('请输入存放生成的html文件的文件夹完整路径：')
    output_folder_path = folder_path
    convert_txt_folder_to_html(folder_path, output_folder_path)
