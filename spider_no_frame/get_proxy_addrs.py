# -*- coding: utf-8 -*-
"""
在网上爬取代理地址，并做对地址做验证
"""
from spider_tools.basic_spider import *
import re
import random
import time


def valide_address(scheme, addr, port, username='', password=''):
    '''验证代理地址'''
    url = 'http://www.baidu.com'
    user_agent = [('User-Agent', get_user_agent())]
    if password and password:
        username = username + ':'
        password = password + '@'
    myproxy = {scheme: username + password + addr + ':' + port}
    
    data = get_data_get(url, proxy=myproxy, header=user_agent, do_chose=1, timeout=3)
    if data:
        pattern = re.compile('<title>百度一下，你就知道</title>')
        title = pattern.findall(data)
        if title:
            print(myproxy, '=== success')
    else:
        print(myproxy, '=== failed')

  
def get_66ip():
    '''66ip
    使用https更容易成功!
    '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?(\d{1,5})'
    '''
    for i in range(1, 6):
        if i == 1:
            url = url = 'http://www.66ip.cn/index.html'
        else:
            url = 'http://www.66ip.cn/%s.html' % str(i)
        user_agent = [('User-Agent', get_user_agent())]
        data = get_data_get(url, header=user_agent, decodeInfo='gb2312')
        print(data)
        time.sleep(random.randint(1, 3))      


def get_kuaidaili():
    ''''快代理
    用http跑不通的，用https可能能跑通！
    (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?(\d{1,5})[\s\S]*?HTTP
    '''
    for i in range(1, 6):
        if i == 1:
            url = 'https://www.kuaidaili.com/free/inha/'
        else:
            url = 'https://www.kuaidaili.com/free/inha/%s/' % str(i)
        user_agent = [('User-Agent', get_user_agent())]
        data = get_data_get(url, header=user_agent)
        print(data)
        time.sleep(random.randint(1, 6))
    
    for i in range(1, 6):
        if i == 1:
            url = 'https://www.kuaidaili.com/free/intr/'
        else:
            url = 'https://www.kuaidaili.com/free/intr/%s/' % str(i)
        user_agent = [('User-Agent', get_user_agent())]
        data = get_data_get(url, header=user_agent)
        print(data)
        time.sleep(random.randint(1, 6))
 

def get_yqie():
    '''http://ip.yqie.com/ipproxy.htm
    默认类型为 https(就算写的是http，还是要https才能测试通过)!
    (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?(\d{1,5})
    '''
    url = 'http://ip.yqie.com/ipproxy.htm'
    user_agent = [('User-Agent', get_user_agent())]
    data = get_data_get(url, header=user_agent)
    print(data)
    

def get_mayidaili():
    '''http://www.mayidaili.com/free/%s
    需要对端口号进行图形识别,协议类型默认为 https!
    '''
    for i in range(1, 6):       
        url = 'http://www.mayidaili.com/free/%s' % str(i)
        user_agent = [('User-Agent', get_user_agent())]
        data = get_data_get(url, header=user_agent)
        print(data)
        time.sleep(random.randint(1, 3))


def get_youdaili():
    '''http://youdaili.steel-spot.com
    (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})@HTTP
    协议类型默认为https
    '''
    for i in range(1, 6):
        if i == 1: 
            url = 'http://youdaili.steel-spot.com/xw/?id=3'
        else:
            url = 'http://youdaili.steel-spot.com/xw/index.asp?id=3&page=%s' % str(i)
        user_agent = [('User-Agent', get_user_agent())]
        data = get_data_get(url, header=user_agent, decodeInfo='gb2312')
        print(data)
        time.sleep(random.randint(1, 3))


def get_proxy_address():
    '''获取代理服务器的代理信息'''
    get_66ip()
#    get_kuaidaili()
#    get_yqie()
#    get_mayidaili()
#    get_youdaili()
    
    


if __name__ == '__main__':
    get_proxy_address()
#    valide_address('http', '219.135.99.185', '8088')
    


#    myproxy = {'http': '219.135.99.185:8088'}
#    myproxy = {'https': '140.143.134.248:3128'}