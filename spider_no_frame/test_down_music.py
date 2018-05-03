# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 19:11:21 2018

@author: tarena
"""
import urllib

#url = 'https://img.alicdn.com/imgextra/i2/20915375/TB1.KhYKpXXXXXMXXXXXXXXXXXX_!!20915375-0-tstar.jpg'
url = 'http://fs.w.kugou.com/201805031620/7bce0af934c7e4d49e9e1312e88fa43f/G126/M08/11/05/HocBAFrlt6WAG9i3ADQZ3BiM8GY606.mp3'
ua_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
req = urllib.request.Request(url, headers=ua_header)
response = urllib.request.urlopen(req)
with open('music.mp3', 'wb') as f:
    f.write(response.read())
print('success')




#from bs4 import BeautifulSoup
#        bsImg = BeautifulSoup(driverImgs.page_source, 'html5lib')
#        imgs = bsImg.find_all('img', {'src': re.compile('.*\.jpg')})
#        with open('xxx.html', 'wb') as f:
#            f.write(driver.page_source.encode('utf-8'))