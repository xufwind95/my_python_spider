# -*- coding: utf-8 -*-
"""
百度音乐数据获取
"""
from selenium import webdriver
import os
import time
import re
import urllib
import hashlib


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, '已创建')


def hashStr(strInfo):
    """对字符串做hash"""
    h = hashlib.sha256()
    h.update(strInfo.encode('utf-8'))
    return h.hexdigest()

# 滚屏操作
def scroll_to_bottom(driver):
    while True:
        try:
            # 让浏览器执行一段js代码
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        except:
            break


def saveImg(url, Localpath):
    '''把图片下载到本地'''
    print(url, '=======', Localpath)
    ua_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    try:
        req = urllib.request.Request(url, headers=ua_header)
        data = urllib.request.urlopen(req).read()
        with open(Localpath + '\\' +  hashStr(time.ctime()) + '.jpg', 'wb') as f:
            f.write(data)
        print('save %s success' % url)        
    except:
        print('failed:', url, Localpath)
        return    

# 获取图片信息
def getImgs(url, name, city):
    # 创建文件夹
    path = 'mPhotos/' + name + city
    mkdir(path)
    driverImgs = webdriver.Chrome()
    driverImgs.get(url)
    try:
        driverImgs.get('https:' + url)
        # 匹配真正的图片的url
        pattern = re.compile('<img[\s\S]*?src="([\s\S]*?\.jpg)"')
        imgs = re.findall(pattern, driverImgs.page_source)
        for img in imgs:
            img = img.replace('&#9;&#9;&#9;', '')
            saveImg('https:' + img, path)
    except:
        return
    finally:
        driverImgs.close()


def parse_page(driver):
    try:
        pattern = re.compile(r'<li class="item">[\s\S]*?<a href="([\s\S]*?)"[\s\S]*?class="name">([\s\S]*?)</span>[\s\S]*?class="city">([\s\S]*?)</span>')
        girlsItem = re.findall(pattern, driver.page_source)
        for it in girlsItem:
            print(it[0], it[1], it[2])
            getImgs(it[0], it[1], it[2])
#            break
    except:
        print('没有获取到首页信息')
        time.sleep(1)    


def test(element, url):
    driver = webdriver.Chrome()
    driver.get(url)
    element.click()
    print('success')
    driver.close()



if __name__ == '__main__':
     # 准备工作
     
#     /html/body/div[3]/div[1]/div/div[1]/div/div[1]/div[1]/a
#    url = 'http://music.baidu.com/song/567299854'
#    url = 'http://www.kugou.com/song/#hash=D3F8E36FE267CD2F44815A4A8AF43727&album_id=8500845'
    url = 'http://www.kugou.com/yy/rank/home/1-8888.html?from=rank'
    outputPath = 'kugoumusic/'
    driver = webdriver.Chrome()
    # 创建本地路径
    mkdir(outputPath)
    # 打开主页
    driver.get(url)
    time.sleep(3)
    
    data = driver.page_source
    atags = driver.find_elements_by_class_name('pc_temp_songname')
    
#    urls = driver.find_elements_by_class_name('pc_temp_btn_listen')
    for a in atags[:3]:
        print(a.get_attribute('href'), a.text)
#        test(a, url)
        a.click()
        print(driver.window_handles)
#        driver.switch_to_window(driver.window_handles[1])
#        target = driver.find_element_by_class_name('music').get_attribute('src')
#        print(target)
#        driver.close()
        driver.switch_to_window(driver.window_handles[0])







