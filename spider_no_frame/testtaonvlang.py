# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 16:20:31 2018

@author: tarena
"""
from spider_tools.basic_spider import *
import urllib

#url = 'https://mm.taobao.com/search_tstar_model.htm'
#url = 'http://maoyan.com/board/4?offset=0'
#url = 'https://movie.douban.com/subject/26673947/'
#url = 'https://www.meituan.com/'

#url = 'http://www.baidu.com/s?'
#keyword = input('请输入您要查询的信息:')
#wd = {'wd': keyword}
## 做urlencode
#wd = urllib.parse.urlencode(wd)
#fullUrl = url + wd

url = 'http://www.fruitday.com/prolist/index/40'
user_agent = [('User-Agent', get_user_agent())]
data = get_data_get(url, header=user_agent)
with open('fruitday_fresh.html', 'wb') as f:
    f.write(data.encode('utf-8'))
