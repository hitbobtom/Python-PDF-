import re
import os
import requests
from multiprocessing.dummy import Pool

# 爬取的主网站地址
start_url = 'https://www.kanunu8.com/book2/11138/'
"""
获取网页源代码
:param url: 网址
:return: 网页源代码
"""
def get_source(url):
    html = requests.get(url)
    return html.content.decode('gbk')  # 这个网页需要使用gbk方式解码才能让中文正常显示

"""
获取每一章链接，储存到一个列表中并返回
:param epub: 目录页源代码
:return: 每章链接
"""
def get_article_url(html):
    article_url_list = []
    article_block = re.findall('正文(.*?)<div class="clear">', html, re.S)[0]
    article_url = re.findall('<a href="(\d*.epub)">', article_block, re.S)
    for url in article_url:
        article_url_list.append(start_url + url)
    return article_url_list

"""
获取每一章的正文并返回章节名和正文
:param epub: 正文源代码
:return: 章节名，正文
"""
def get_article(html):
    chapter_name = re.findall('<h1>(.*?)<br>', html, re.S)[0]
    text_block = re.search('<p>(.*?)</p>', html, re.S).group(1)
    text_block = text_block.replace('&nbsp;', '')           # 替换 &nbsp; 网页空格符
    text_block = text_block.replace('<p>', '')              # 替换 <p></p> 中的嵌入的 <p></p> 中的 <p>
    return chapter_name, text_block

"""
将每一章保存到本地
:param chapter: 章节名, 第X章
:param article: 正文内容
:return: None
"""
def save(chapter, article):
    os.makedirs('北欧众神', exist_ok=True)  # 如果没有"北欧众神"文件夹，就创建一个，如果有，则什么都不做"
    with open(os.path.join('北欧众神', chapter + '.txt'), 'w', encoding='utf-8') as f:
        f.write(article)

"""
根据正文网址获取正文源代码，并调用get_article函数获得正文内容最后保存到本地
:param url: 正文网址
:return: None
"""
def query_article(url):
    article_html = get_source(url)
    chapter_name, article_text = get_article(article_html)
    # print(chapter_name)
    # print(article_text)
    save(chapter_name, article_text)

if __name__ == '__main__':
    toc_html = get_source(start_url)
    toc_list = get_article_url(toc_html)
    pool = Pool(4)
    pool.map(query_article, toc_list)
