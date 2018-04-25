# -*- coding: utf-8 -*-
"""
在网上爬取代理地址，并对地址做验证
"""
from spider_tools.basic_spider import get_user_agent, get_data_get
from concurrent.futures import ThreadPoolExecutor
import re
import random
import time
import queue
import json
import os


def valide_address(scheme, addr, port, username='', password=''):
    '''验证代理地址'''
    url = 'http://www.baidu.com'
    user_agent = [('User-Agent', get_user_agent())]
    if username and password:
        username = username + ':'
        password = password + '@'
    myproxy = {scheme: username + password + addr + ':' + port}
    data = get_data_get(url, proxy=myproxy, header=user_agent, do_chose=1, timeout=3)
    if data:
        pattern = re.compile('<title>百度一下，你就知道</title>')
        title = pattern.findall(data)
        if title:
            print(myproxy, '=== success')
            return True
    print(myproxy, '=== failed')
    return False
    

def get_match_data(url, pattern, decodeInfo='utf-8'):
    '''获取匹配的数据'''
    user_agent = [('User-Agent', get_user_agent())]
    data = get_data_get(url, header=user_agent, decodeInfo=decodeInfo)
    matches = []
    if data:
        matches = pattern.findall(data)
    else:
        print(url + ' 没有获取到数据！')
    return matches


def check_proxy_addr(q_res, item):
    flag = True
    for i in range(3):
       if not valide_address(item['scheme'], item['addr'], item['port']):
           flag = False
           break
    if flag:
        q_res.put(item)


def get_66ip(q):
    '''66ip
    使用https更容易成功!
    '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?(\d{1,5})'
    '''
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?(\d{1,5})')
    for i in range(1, 6):
        if i == 1:
            url = url = 'http://www.66ip.cn/index.html'
        else:
            url = 'http://www.66ip.cn/%s.html' % str(i)
        matches = get_match_data(url, pattern, 'gb2312')
        for it in matches: 
            q.put({'scheme': 'https', 'addr': it[0], 'port': it[1], 'net': '66ip'})
        time.sleep(random.randint(1, 3))
    q.put({})


def get_kuaidaili(q):
    ''''快代理
    用http跑不通的，用https可能能跑通！
    (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?(\d{1,5})[\s\S]*?HTTP
    '''
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?(\d{1,5})[\s\S]*?HTTP')
    for i in range(1, 6):
        if i == 1:
            url = 'https://www.kuaidaili.com/free/inha/'
        else:
            url = 'https://www.kuaidaili.com/free/inha/%s/' % str(i)
        matches = get_match_data(url, pattern)
        for it in matches:
            q.put({'scheme': 'http', 'addr': it[0], 'port': it[1], 'net': 'kuaidaili'})
        time.sleep(random.randint(1, 6))
    
    for i in range(1, 6):
        if i == 1:
            url = 'https://www.kuaidaili.com/free/intr/'
        else:
            url = 'https://www.kuaidaili.com/free/intr/%s/' % str(i)
        matches = get_match_data(url, pattern)
        for it in matches:
            q.put({'scheme': 'http', 'addr': it[0], 'port': it[1], 'net': 'kuaidaili'})        
        time.sleep(random.randint(1, 6))
    q.put({})


def get_yqie(q):
    '''http://ip.yqie.com/ipproxy.htm
    默认类型为 https(就算写的是http，还是要https才能测试通过)!
    (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?(\d{1,5})
    '''
    url = 'http://ip.yqie.com/ipproxy.htm'
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?(\d{1,5})')
    matches = get_match_data(url, pattern)
    for it in matches:
        q.put({'scheme': 'https', 'addr': it[0], 'port': it[1], 'net': 'yqie'})
    q.put({})


def get_mayidaili(q):
    '''http://www.mayidaili.com/free/%s
    需要对端口号进行图形识别,协议类型默认为 https!
    '''
    for i in range(1, 6):       
        url = 'http://www.mayidaili.com/free/%s' % str(i)
        user_agent = [('User-Agent', get_user_agent())]
        data = get_data_get(url, header=user_agent)
        print(data)
        time.sleep(random.randint(1, 3))


def get_youdaili(q):
    '''http://youdaili.steel-spot.com
    (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})@HTTP
    协议类型默认为https
    '''
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})@HTTP')
    for i in range(1, 6):
        if i == 1: 
            url = 'http://youdaili.steel-spot.com/xw/?id=3'
        else:
            url = 'http://youdaili.steel-spot.com/xw/index.asp?id=3&page=%s' % str(i)
        matches = get_match_data(url, pattern, 'gb2312')
        for it in matches:
            q.put({'scheme': 'https', 'addr': it[0], 'port': it[1], 'net': 'youdaili'})
        time.sleep(random.randint(1, 3))
    q.put({})


def get_proxy_address(filepath):
    '''获取代理服务器的代理信息'''
#    get_mayidaili()
    # 将要获取代理信息的各个方法添加进任务(蚂蚁的需要破解验证码，暂时未处理)
    tasks = [get_66ip, get_kuaidaili, get_yqie, get_youdaili]
    res = []
    q_addrs = queue.Queue()
    q_res = queue.Queue()
    length = len(tasks)
    with ThreadPoolExecutor(length * 5) as executor:
        # 将网上的所有代理信息先拿下来
        for task in tasks:
            executor.submit(task, q_addrs)
        # 验证代理信息是否正确
        num = 0
        while num < length:
            item = q_addrs.get()
            if not item:
                num += 1
                continue
            executor.submit(check_proxy_addr, q_res, item)

    if q_res: 
        while not q_res.empty():
            res.append(q_res.get())

    with open(filepath, 'w') as f:
        for item in res:
            f.write(json.dumps(item) + '\n')

    return res        


def get_proxy_from_file(filepath):
    '''从文件获取代理服务器的信息'''
    if not os.path.exists(filepath):
        return None
    proxy_addrs, res = [], []
    q_res = queue.Queue()
    with open(filepath) as f:
        for line in f:
            proxy_addrs.append(json.loads(line))
    with ThreadPoolExecutor(5) as executor:
        for d_proxy in proxy_addrs:
            executor.submit(check_proxy_addr, q_res, d_proxy)
    while not q_res.empty():
        res.append(q_res.get())
    if res:
        with open(filepath, 'w') as f:
            for item in res:
                f.write(json.dumps(item) + '\n')
    return res


def get_proxy_main():
    '''入口方法'''
    fileapth = 'proxy_addrs.txt'
    res = get_proxy_from_file(fileapth)
    if res:
        print('file has useable proxy addr')
        return res
    res = get_proxy_address(fileapth)
    if res:
        print('get proxy addr from net')
    return res


if __name__ == '__main__':
    proxy_addrs = get_proxy_main()
    if proxy_addrs:
        print('the following can be use as proxy server')
        print('============================================') 
    else:
        print('sorry, there is no useable proxy address...')
    for it in proxy_addrs:
        print(it)

#    myproxy = {'http': '219.135.99.185:8088'}
