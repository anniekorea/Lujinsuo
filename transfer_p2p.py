# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 13:21:00 2018

@author: Administrator
"""

import requests
import time
import datetime
import random
from lxml import etree
#import webbrowser
import pandas as pd

interest_limit=8.4
amount_min=10000
amount_max=31000

try_again=1
try_time=0
product_list=pd.DataFrame(columns = ['time','name','interest','amount'])

while try_again==1:
    try_time = try_time + 1
    print('第%s次尝试...'%try_time)#,end='')
    url='https://www.lup2p.com/secmkt/p2p/transfer/list?from=lup2p'
    headers={'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    r=requests.get(url,headers=headers,timeout=120)
    html=r.content
    link=etree.HTML(html,parser=etree.HTMLParser(encoding='utf-8'))
    main_list=link.xpath('//ul[@class="main-list"]')
    product_name=main_list[0].xpath('//dt[@class="product-name"]/a/text()')
    interest_rate=main_list[0].xpath('//li[@class="interest-rate"]/p[@class="num-style"]/text()')
    product_amount=main_list[0].xpath('//div[@class="product-amount"]/p/em[@class="num-style"]/text()')
    
    if len(product_name)>=1:
        print('有新项目，快查看！')
        appear_time=[]
        name=[]
        interest=[]
        amount=[]
        for i in range(0,len(product_name)):
            appear_time.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            name.append(product_name[i].strip())
            interest.append(float(interest_rate[i].replace('%','')))
            amount.append(float(product_amount[i].replace(',','')))
        
        product=pd.DataFrame({'time':appear_time,'name':name,'interest':interest,'amount':amount})
        product_list=product_list.append(product,ignore_index=True)#,sort=False)
        
        #判断是否有利率和金额都满足要求的项目
        if any((product['interest']>=interest_limit) &
               (product['amount']>=amount_min) &
               (product['amount']<=amount_max)):  
            print(product)
            print('\a') #声音提醒
            #webbrowser.open_new(url)
            #try_again=0
    
    time_interval = random.uniform(5,10) 
    time.sleep(time_interval)

