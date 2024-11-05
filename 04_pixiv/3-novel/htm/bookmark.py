import os
import re


class Line:
    type = None
    href = None
    content = None


def href_format(content):
    return content.replace(' ', '-')


def build_index(content_list):
    line_list = []
    for i in range(0, len(content_list)):
        content = content_list[i].strip()
        line = Line()
        line.content = content

        FIRST_LEVEL_TITLE_CONTENT = r'^(第)?\d+(章|节|话|幕)?\s+(.*)$'
        first_level_title_match = re.search(FIRST_LEVEL_TITLE_CONTENT, content)
        if first_level_title_match is not None:
            line.type = 'first_level_title'
            line.href = href_format(content)

        SECOND_LEVEL_TITLE_CONTENT = r'^(第)?\d+\.\d+(章|节|话|幕)?\s*(.*)$'
        second_level_title_match = re.search(SECOND_LEVEL_TITLE_CONTENT, content)
        if second_level_title_match is not None:
            line.type = 'second_level_title'
            line.href = href_format(content)

        THIRD_LEVEL_TITLE_CONTENT = r'^(第)?\d+\.\d+\.\d+(章|节|话|幕)?\s*(.*)$'
        third_level_title_match = re.search(THIRD_LEVEL_TITLE_CONTENT, content)
        if third_level_title_match is not None:
            line.type = 'third_level_title'
            line.href = href_format(content)

        line_list.append(line)
    return line_list
