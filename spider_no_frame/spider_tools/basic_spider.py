# -*- coding: utf-8 -*-
"""
爬虫基础功能模块
"""
from urllib import request
from urllib import error
import random
import time

# 未获取到页面后再次发起请求的时间间隔:开始时间 
INTERVAL_BEGIN = 1
# 未获取到页面后再次发起请求的时间间隔:结束时间 
INTERVAL_END = 5


def get_user_agent():
    '''动态获取user_agent'''
    user_agents = [
	    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
	    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
	    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
	    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
	    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
	    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
	    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
	    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
	    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
	    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
	    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
	    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",        
    ]
    return random.choice(user_agents)


def get_data_common(url, proxy=None, do_chose=0, header=[], decodeInfo='utf-8', timeout=None, num_retries=5):
    '''通用方式获取html页面
    参数说明:
        url : 爬取地址
        proxy : 代理信息(字典 {'protocol_type': '[username:password@]address:port'} )
        chose : 是否一定选择代理 1: 一定 0: 根据概率随机选择
        header : 设置请求头(列表，每个元素为元组)
        decodeInfo : 编码方式
        timeout : 响应的超时时间
        num_retries : 爬取失败后，需要重试的重试次数
    '''
    if not do_chose and proxy:
        if random.randint(1, 10) >= 7:
            proxy = False

    # 处理代理
    proxy_support = request.ProxyHandler(proxy)
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)
    opener.addheaders = header
    data = None
    # 根据url获取数据
    try:
        req = request.urlopen(url, timeout=timeout)
        data = req.read().decode(decodeInfo)
    except UnicodeDecodeError:
        print('编码解析出错')
    except error.URLError:
        print('url错误') 
    except error.HTTPError as e:
        print('获取http响应出错')
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code <= 600:
                time.sleep(random.randint(INTERVAL_BEGIN, INTERVAL_END))
                data = get_data_common(url, proxy, do_chose, header, decodeInfo, timeout, num_retries - 1)
    return data
    

def get_html_inner_brower():
    '''通过内置浏览器的方式获取html页面,动态页面很难实现规律化的处理，这里不对该方式进行封装'''
    
    
    

