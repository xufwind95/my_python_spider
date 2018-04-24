# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 11:15:49 2018

@author: tarena
"""
# 使用 cookirjar 来登录人人
from http import cookiejar
from urllib import request
from urllib import parse

# 创建一个cookirjar
cookie = cookiejar.CookieJar()

# 通过httpcookieprocess 处理 cookie
cookie_handler = request.HTTPCookieProcessor(cookie)

# 构建一个opener
opener = request.build_opener(cookie_handler)
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')]

# 找到登录的入口
urlLogin = 'http://www.renren.com/PLogin.do'

# 登录用户名和密码
data = {'email': "xuf95@163.com", "password": "11xf123456"}

# 通过urlencode
data = bytes(parse.urlencode(data), encoding='utf-8')
# 发送一个post请求，生成登录成功之后的cookie
request = request.Request(urlLogin, data=data, method='POST')
response = opener.open(request)
# 获取到cookie后打开自己的个人主页
responseRenRen = opener.open('http://www.renren.com/222775423/profile')

with open('myRenrenFromCookieJar.html', 'wb') as f:
    f.write(responseRenRen.read())





