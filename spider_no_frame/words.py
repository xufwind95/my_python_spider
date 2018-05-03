# -*- coding: utf-8 -*-
"""
考研英语单词爬取
"""
from spider_tools.basic_spider import get_data_get, get_user_agent 
import re
import os
#import json


def get_one_page(url, decodeInfo):
    """发起Http请求，获取Response的响应结果
    """
    user_agent = [('User-Agent', get_user_agent())]
    data = get_data_get(url, header=user_agent, decodeInfo=decodeInfo, timeout=3)
    return data


def parse_page(html, pattern):
    '''用正则表达式解析页面'''
    matches = pattern.findall(html)
    for it in matches:
        yield it


def save_words(json_data, filename):
    '''保存单词到对应文件中'''
    with open(filename, 'a', encoding='utf-8') as f: 
#        f.write(json.dumps(json_data,ensure_ascii=False)+'\n')
        f.write(json_data + '\n') 


def craw_words_onepage(url, filename, decodeInfo):
    '''处理一页的内容'''
    print('处理:', url, '写入:', filename)
    html = get_one_page(url, decodeInfo)
    pattern = re.compile(r'<td><strong>(\w+)*?</strong></td>[\s\S]*?<td>([\s\S]*?)</td>')
    matches = []
    if html:
        print('get ' + url + ' success')
        matches = [it for it in parse_page(html, pattern)]
    for it in matches:
#        save_words({'word': it[0], 'trans': it[1]}, filename)
        save_words(it[0] + ' ' + it[1], filename)


if __name__ == '__main__':
    url = 'https://www.51test.net/kaoyan/cihui/'
    decodeInfo = 'gb2312'
    pattern = re.compile(r'<li><a href="([\s\S]*?)"[\s\S]*?class="small14">(2019考研[\s\S]*?大纲[Uu]nit[\s\S]?\d+[\s\S]*?【[\s\S]*?】)</a>')
    matches = [it for it in parse_page(get_one_page(url, decodeInfo), pattern)]
    prefix = 'https://www.51test.net'
    filedir = 'words//'
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    for it in matches[:32]:
        url = prefix + it[0]
        filename = it[1].lower().replace(' ','').replace('unit','').replace('【', '单元 ').replace('】','')
        filename = filedir + filename.replace('2019考研英语单词书词汇大纲','').replace('2019考研英语词汇大纲','')
        craw_words_onepage(url, filename + '.txt', decodeInfo)
