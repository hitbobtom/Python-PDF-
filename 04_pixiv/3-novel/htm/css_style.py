import os


def add_li(href, title):
    return '<li><a href="#' + href + '">' + title + '</a>\n'


def add_toc_li(level, href, title):
    str = ''
    if level == 1:
        str = 'toc-link node-name--H3 '
    elif level == 2:
        str = 'toc-link node-name--H4 '
    elif level == 3:
        str = 'toc-link node-name--H5 '

    return '<li class="toc-list-item"><a href="#' + href + '" class="' + str + '">' + title + '</a>\n'


def add_h2(href, title):
    return '<h2 id="' + href + '"><a class="anchor" href="#' + href + '"></a>' + title + '</h2>'


def add_h3(href, title):
    return '<h3 id="' + href + '"><a class="anchor" href="#' + href + '"></a>' + title + '</h3>'


def add_h4(href, title):
    return '<h4 id="' + href + '"><a class="anchor" href="#' + href + '"></a>' + title + '</h4>'


def add_h5(href, title):
    return '<h5 id="' + href + '"><a class="anchor" href="#' + href + '"></a>' + title + '</h5>'


def add_p(line):
    return '<div class="paragraph"><p>' + line + '</p></div>'

