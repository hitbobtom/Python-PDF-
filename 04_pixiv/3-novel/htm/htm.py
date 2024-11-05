import os
import shutil
import css_style
import bookmark

up_dir_path = os.path.abspath(os.path.join(os.getcwd(), ""))


class Line:
    type = None
    href = None
    content = None


def read_txt_file(txt_path):
    content_list = []
    f_txt = open(txt_path, 'r', encoding="utf-8")
    # 利用循环全部读出
    while 1 > 0:
        line = f_txt.readline()
        if line == '':
            break
        content_list.append(line)
    f_txt.close()
    return content_list


def write_html(html_path, line_list):
    f_html = open(html_path, 'w', encoding="utf-8")
    template_path = up_dir_path + '\\template'

    #################### 1.写入文件头 ####################
    HEAD_CONTENT = read_txt_file(os.path.join(template_path, 'head.txt'))
    f_html.write(''.join(HEAD_CONTENT) + '\n')
    #################### 2.写入索引header ####################
    f_html.write('<div id="header">' + '\n')
    f_html.write('<h1>Reference Documentation</h1>' + '\n')
    f_html.write('<div id="toc" class="toc2">' + '\n')
    f_html.write('<div id="toctitle">Table of Contents</div>' + '\n')
    ########## 2.1 写入<ul class="mobile-toc"> ##########
    f_html.write('<ul class="mobile-toc">' + '\n')
    f_html.write('<li><a href="#legal">Legal</a></li>' + '\n')
    f_html.write('<li><a href="#contents">目录</a>' + '\n')
    f_html.write('<ul class="sectlevel2">' + '\n')
    ##### 写入目录索引 li #####
    isFirst = False
    isSecond = False
    isThird = False
    for i in range(0, len(line_list)):
        line = line_list[i]
        # 处理一级标题
        if line.type == 'first_level_title':
            if isThird == True:
                f_html.write('</ul>' + '\n')
                isThird = False
            if isSecond == True:
                f_html.write('</li>' + '\n')
                f_html.write('</ul>' + '\n')
                isSecond = False
            if isFirst == True:
                f_html.write('</li>' + '\n')
            f_html.write(css_style.add_li(line.href, line.content) + '\n')
            isFirst = True
        # 处理二级标题
        if line.type == 'second_level_title':
            if isThird == True:
                f_html.write('</ul>' + '\n')
                isThird = False
            if isSecond == True:
                f_html.write('</li>' + '\n')
            if isSecond == False:
                f_html.write('<ul class="sectlevel3">' + '\n')
            f_html.write(css_style.add_li(line.href, line.content) + '\n')
            isSecond = True
        # 处理三级标题
        if line.type == 'third_level_title':
            if isThird == False:
                f_html.write('<ul class="sectlevel4">' + '\n')
                isSecond = True
            f_html.write(css_style.add_li(line.href, line.content) + '</li>\n')
            isThird = True
    # 处理结尾
    if isThird == True:
        f_html.write('</ul>' + '\n')
    if isSecond == True:
        f_html.write('</ul>' + '\n')
    if isFirst == True:
        f_html.write('</li>' + '\n')
    ##### 写入目录索引 li END #####
    f_html.write('</ul>' + '\n')
    f_html.write('</li>' + '\n')
    f_html.write('</ul><!--<ul class="mobile-toc">-->' + '\n')
    ########## 2.2 写入<div id="tocbot" class="js-toc desktop-toc"> ##########
    f_html.write('<div id="tocbot" class="js-toc desktop-toc">' + '\n')
    f_html.write('<ol class="toc-list ">' + '\n')
    f_html.write(
        '<li class="toc-list-item is-active-li"><a href="#legal" class="toc-link node-name--H2  is-active-link">Legal</a></li>' + '\n')
    f_html.write('<li class="toc-list-item"><a href="#contents" class="toc-link node-name--H2 ">目录</a>' + '\n')
    f_html.write('<ol class="toc-list  is-collapsible is-collapsed">' + '\n')
    ##### 写入目录索引 li #####
    isFirst = False
    isSecond = False
    isThird = False
    for i in range(0, len(line_list)):
        line = line_list[i]
        # 处理一级标题
        if line.type == 'first_level_title':
            if isThird == True:
                f_html.write('</ol>' + '\n')
                isThird = False
            if isSecond == True:
                f_html.write('</li>' + '\n')
                f_html.write('</ol>' + '\n')
                isSecond = False
            if isFirst == True:
                f_html.write('</li>' + '\n')
            f_html.write(css_style.add_toc_li(1, line.href, line.content) + '\n')
            isFirst = True
        # 处理二级标题
        if line.type == 'second_level_title':
            if isThird == True:
                f_html.write('</ol>' + '\n')
                isThird = False
            if isSecond == True:
                f_html.write('</li>' + '\n')
            if isSecond == False:
                f_html.write('<ol class="toc-list  is-collapsible is-collapsed">' + '\n')
            f_html.write(css_style.add_toc_li(2, line.href, line.content) + '\n')
            isSecond = True
        # 处理三级标题
        if line.type == 'third_level_title':
            if isThird == False:
                f_html.write('<ol class="toc-list  is-collapsible is-collapsed">' + '\n')
            f_html.write(css_style.add_toc_li(3, line.href, line.content) + '</li>\n')
            isThird = True
    # 处理结尾
    if isThird == True:
        f_html.write('</ol>' + '\n')
    if isSecond == True:
        f_html.write('</li>' + '\n')
        f_html.write('</ol>' + '\n')
    if isFirst == True:
        f_html.write('</li>' + '\n')
    ##### 写入目录索引 li END #####
    f_html.write('</ol>' + '\n')
    f_html.write('</ol>' + '\n')
    f_html.write('</div><!--<div id="tocbot" class="js-toc desktop-toc">-->' + '\n')
    f_html.write('</div><!--<div id="toc" class="toc2">-->' + '\n')
    f_html.write('</div><!--<div id="header">-->' + '\n')
    ############### 3.写入正文content ###############
    f_html.write('<div id="content">' + '\n')
    f_html.write('<div class="sect1">' + '\n')
    f_html.write('<h2 id="legal"><a class="anchor" href="#legal"></a>Legal</h2>' + '\n')
    f_html.write(
        '<div class="sectionbody">\n    <div class="paragraph">\n        <p>2.3.6.RELEASE</p>\n    </div>\n    <div class="paragraph">\n        <p>Copyright © 2012-2020</p>\n    </div>\n</div>\n</div>' + '\n')
    f_html.write('<div class="sect1">' + '\n')
    f_html.write('<h2 id="contents"><a class="anchor" href="#contents"></a>目录</h2>' + '\n')
    ########## 3.1 正文目录 ##########
    f_html.write(
        '<div class="admonitionblock tip">\n    <table>\n        <tbody>\n        <tr>\n            <td class="icon">\n                <i class="fa icon-tip" title="Tip"></i>\n            </td>\n            <td class="content">' + '\n')
    for i in range(0, len(line_list)):
        line = line_list[i]
        if line.type == 'first_level_title':
            str = '<a href="#' + line.href + '">' + line.content + '</a>' + '<br>'
            f_html.write(str + '\n')
        elif line.type == 'second_level_title':
            str = '<a href="#' + line.href + '">' + '&nbsp;&nbsp;&nbsp;&nbsp;' + line.content + '</a>' + '<br>'
            f_html.write(str + '\n')
        elif line.type == 'third_level_title':
            str = '<a href="#' + line.href + '">' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + line.content + '</a>' + '<br>'
            f_html.write(str + '\n')
    f_html.write('            </td>\n        </tr>\n        </tbody>\n    </table>\n</div>' + '\n')
    ########## 3.2 正文 ##########
    f_html.write('<div class="sectionbody">' + '\n')
    ##### 写入正文 li #####
    file_extensions = [".png", ".jpg", ".jpeg"]
    isFirst = False
    isSecond = False
    isThird = False
    for i in range(0, len(line_list)):
        line = line_list[i]
        # 处理一级标题
        if line.type == 'first_level_title':
            if isThird == True:
                f_html.write('</div>' + '\n')
                isThird = False
            if isSecond == True:
                f_html.write('</div>' + '\n')
                isSecond = False
            if isFirst == True:
                f_html.write('</div>' + '\n')
            f_html.write('<div class="sect2">' + '\n')
            f_html.write(css_style.add_h3(line.href, line.content) + '\n')
            isFirst = True
        # 处理二级标题
        if line.type == 'second_level_title':
            if isThird == True:
                f_html.write('</div>' + '\n')
                isThird = False
            if isSecond == True:
                f_html.write('</div>' + '\n')
            f_html.write('<div class="sect3">' + '\n')
            f_html.write(css_style.add_h4(line.href, line.content) + '\n')
            isSecond = True
        # 处理三级标题
        if line.type == 'third_level_title':
            if isThird == True:
                f_html.write('</div>' + '\n')
            f_html.write('<div class="sect4">' + '\n')
            f_html.write(css_style.add_h5(line.href, line.content) + '\n')
            isThird = True
        # 处理段落
        if line.type == None:
            if any(file_extension in line.content for file_extension in file_extensions):
                line.content = '<img src="img/' + line.content + '">'
            f_html.write(css_style.add_p(line.content) + '\n')
    # 处理结尾
    if isThird == True:
        f_html.write('</div>' + '\n')
    if isSecond == True:
        f_html.write('</div>' + '\n')
    if isFirst == True:
        f_html.write('</div>' + '\n')
    ##### 写入正文 li 结束 #####
    f_html.write('</div>' + '\n')
    f_html.write('</div>' + '\n')
    f_html.write('</div><!--<div id="content">-->' + '\n')
    ############### 4.写入文件尾 ###############
    END_CONTENT = read_txt_file(os.path.join(template_path, 'end.txt'))
    f_html.write(''.join(END_CONTENT) + '\n')

    f_html.close()


def copy_css_html(html_path):
    css_folder = up_dir_path + "\\static"
    html_folder = os.path.dirname(html_path) + "\\static"
    if os.path.exists(html_folder):
        return
    shutil.copytree(css_folder, html_folder)


def txt_to_html(txt_path, html_path):
    # 1.读取文件头、文件尾
    content_list = read_txt_file(txt_path)
    # 2.生成索引
    line_list = bookmark.build_index(content_list)
    # 3.复制css样式文件
    copy_css_html(html_path)
    # 4.写出html文件
    write_html(html_path, line_list)
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
            html_filename = filename.replace('.txt', '.htm')
            html_path = os.path.join(output_folder_path, html_filename)
            txt_to_html(txt_path, html_path)
            print(f"Converted {txt_path} to {html_path}")


if __name__ == "__main__":
    folder_path = input('请输入包含小说文件的文件夹完整路径：')
    # output_folder_path = input('请输入存放生成的html文件的文件夹完整路径：')
    output_folder_path = folder_path
    convert_txt_folder_to_html(folder_path, output_folder_path)
