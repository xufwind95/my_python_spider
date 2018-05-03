# -*- coding: utf-8 -*-
"""
获取有道在线翻译数据
"""
import urllib.request
import json
import urllib.parse
from spider_tools.basic_spider import get_data_post, get_user_agent 
from get_proxy_addrs import get_proxy_main
import random


#myproxy = {scheme: username + password + addr + ':' + port}
my_proxies = [{p['scheme']: p['addr'] + ':' + p['port']} for p in get_proxy_main()]

# 不断调用爬取翻译页面的功能，直到result被设置为true，退出整个程序
while True:
    # 假定用户输入 CloseMe 就退出
    key = input('请输入翻译的文字(输入CloseMe退出):\n')
    if key == 'CloseMe':
        break
    # 做真正的查询操作
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 构造 headers
    headers = {'User-Agent': get_user_agent(),
               'X-Requested-With': 'XMLHttpRequest',
               'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }
    # 将form数据规范化,然后post给服务端
    formdata = {
                'i':key,
                'from':'AUTO',
                'to':'AUTO',
                'smartresult':'dict',
                'client':'fanyideskweb',
                'salt':'1523934765921',
                'sign':'7097b5b92fd4d83b5b497028238ffbb1',
                'doctype':'json','version':'2.1',
                'keyfrom':'fanyi.web',
                'action':'FY_BY_REALTIME',
                'typoResult':'false',
            }
    data = bytes(urllib.parse.urlencode(formdata), encoding='utf-8')
    # 给服务器发送post请求
    myproxy = random.choice(my_proxies)
#    print(myproxy)
    info = get_data_post(url, proxy=myproxy, header=headers, formData=data)
    word = json.loads(info)
#{'type': 'EN2ZH_CN', 'errorCode': 0, 'elapsedTime': 0, 'translateResult': [[{'src': 'consist', 'tgt': '由'}]]}
    print(key, '翻译为:')
    out = [x[0]['tgt'] for x in word['translateResult']]
    print(','.join(out))
    
    
    
    
    
    
    
    
    
    
    
