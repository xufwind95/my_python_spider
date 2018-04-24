# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 11:04:28 2018

@author: tarena
"""
import urllib.request
import json
import urllib.parse
from spider_tools.basic_spider import *


# 不断调用爬取翻译页面的功能，直到result被设置为true，退出整个程序
while True:
    # 假定用户输入 CloseMe 就退出
    key = input('请输入翻译的文字(输入CloseMe退出):\n')
    if key == 'CloseMe':
        break
    # 做真正的查询操作
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 构造 headers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
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
#    __init__(self, url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)
    myproxy = {'http': '219.135.99.185:8088'}
#    proxy_support = urllib.request.ProxyHandler(myproxy)
#    opener = urllib.request.build_opener(proxy_support)
#    urllib.request.install_opener(opener)
#    proxy_headers = []
#    for key, value in headers.items():
#        proxy_headers.append((key, value))
#    opener.addheaders = proxy_headers  
  
#    req = urllib.request.Request(url, data=data, method='POST')
#    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
#    response = urllib.request.urlopen(req)
#    info = response.read().decode('utf-8')
    
#    url, proxy=None, do_chose=0, header=None,formData=None, decodeInfo='utf-8', timeout=None, num_retries=5):
    info = get_data_post(url, proxy=myproxy, header=headers, do_chose=1, formData=data)
    word = json.loads(info)
    print(key, '翻译为:')
    out = [x[0]['tgt'] for x in word['translateResult']]
    print(','.join(out))
#    for i in word['translateResult']:
#        print(i[0]['tgt'], end=' ')


#{'type': 'EN2ZH_CN', 'errorCode': 0, 'elapsedTime': 0, 'translateResult': [[{'src': 'consist', 'tgt': '由'}]]}
    
    
    
    
    
    
    
    
    
    
    
