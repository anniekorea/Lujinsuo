# -*- coding: utf-8 -*-
"""
Created on Thu May 16 16:57:27 2019

@author: Administrator

不登录，直接抓取新标网页，若全部为“新客专享”，
则提示“有新标！共%s项，其中新客专享%s项”；
若出现“新客专享”的次数<“投资金额”出现的次数，
说明有项目老客户也可投，则提示“有可投新标！！！！！”
"""

import requests
import time
import random
#from lxml import etree
#import webbrowser
#import pandas as pd

try_again=True
try_time=0

while try_again:
    try_time = try_time + 1
    print('%s 第%s次尝试...'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),try_time),end='')
    url='https://www.lup2p.com/lup2p/' #新标的网址
    headers={'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    
    r=requests.get(url,headers=headers,timeout=10)
    html=r.content  
    html_str=str(html,encoding='utf-8')
    print('有新标！共%s项，其中新客专享%s项'%(html_str.count('>投资金额</span>'),html_str.count('>新客专享</span>')))
    if html_str.count('>投资金额</span>')>html_str.count('>新客专享</span>'):
        print('有可投新标！！！！！')
        print('\a')
        #webbrowser.open_new(url)
        #try_again=False
        #break
    
    time_interval = random.uniform(10,20) 
    time.sleep(time_interval)

