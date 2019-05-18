# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:55:44 2019

@author: Administrator

2019年4月后陆金所对网页的访问进行了限制，直接使用requests爬取的网页为验证网页，
爬取不到需要的项目信息，改为selenium模拟浏览器进行爬取，可获得所需项目信息，
但需要控制爬取频率，否则容易被封。
将休眠时间设置为20秒以上，可顺利爬取一段时间，但最后还是被封。
"""

import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import etree

class Lumoney:
    def __init__(self):
        self.username = '*********' #陆金所注册手机号
        self.pwd = '*********'  #密码
        self.driver = webdriver.Chrome()
        self.new_p2p = False
        self.transfer_p2p = False
        self.product_list=pd.DataFrame(columns = ['time','name','interest','amount'])

    def login(self):
        driver = self.driver
        driver.get('https://www.lup2p.com/user/login')
        
        # 登录账号
        input_userName = driver.find_element_by_id('userNameLogin')
        input_userName.send_keys(self.username)
        time.sleep(2)
        
        # 密码
        input_password = driver.find_element_by_id('pwd')
        input_password.send_keys(self.pwd)
        time.sleep(2)
        
        # 手工输入验证码
        vericode = input('input code:')
        input_capcha = driver.find_element_by_id('validNum')
        if not input_capcha.text:
            input_capcha.send_keys(vericode)
        time.sleep(2)
        
        #勾选同意协议
        #driver.find_element_by_id('signLoginAgreement').click()
        
        # 点击“登录”
        login = driver.find_element_by_id('loginBtn')
        login.send_keys(Keys.ENTER)

    def check_new_p2p(self):
        time.sleep(random.uniform(5,10))
        print('检查新标...',end='')
        self.new_p2p = False
        self.driver.get('https://www.lup2p.com/lup2p/p2p')
        new_html=self.driver.page_source
        new_html_str=str(new_html)
        if new_html_str.count('已售完')>0:
            print('新标已售完')
        else:
            self.new_p2p=True
            print('有可投新标！！！\a')
            
        self.new_html=new_html
        return new_html_str
    
    def check_transfer_p2p(self):
        time.sleep(random.uniform(20,25))
        print('检查转让标...',end='')
        self.transfer_p2p = False
        self.driver.get('https://www.lup2p.com/secmkt/p2p/transfer/list?from=lup2p')
        transfer_html=self.driver.page_source
        transfer_html_str=str(transfer_html)
        if transfer_html_str.count('暂无符合条件的项目</div')>0:
            print('暂无符合条件的项目')
        elif transfer_html_str.count('由于您的刷新频率过快')>0:
            print('刷新频率过快')
            time.sleep(20)  #等待20秒，手动在网页上进行验证，否则后续一直都是需验证界面
        else:
            self.transfer_p2p=True
            print('有可投转让标！！！\a')
        
        self.transfer_html=transfer_html
        return transfer_html_str
    
    def select_transfer_p2p(self,interest_limit=0,amount_min=0,amount_max=1000000):
        if self.transfer_p2p:
            link=etree.HTML(self.transfer_html,parser=etree.HTMLParser(encoding='utf-8'))
            main_list=link.xpath('//ul[@class="main-list"]')
            product_name=main_list[0].xpath('//dt[@class="product-name"]/a/text()')
            interest_rate=main_list[0].xpath('//li[@class="interest-rate"]/p[@class="num-style"]/text()')
            product_amount=main_list[0].xpath('//div[@class="product-amount"]/p/em[@class="num-style"]/text()')
            
            if len(product_name)>=1:
                appear_time=[]
                name=[]
                interest=[]
                amount=[]
                for i in range(0,len(product_name)):
                    appear_time.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                    name.append(product_name[i].strip())
                    interest.append(float(interest_rate[i].replace('%','')))
                    amount.append(float(product_amount[i].replace(',','')))
                
                product=pd.DataFrame({'time':appear_time,'name':name,'interest':interest,'amount':amount})
                self.product_list=self.product_list.append(product,ignore_index=True)#,sort=False)
                
                #判断是否有利率和金额都满足要求的项目
                if any((product['interest']>=interest_limit) &
                       (product['amount']>=amount_min) &
                       (product['amount']<=amount_max)):  
                    print(product)
                    print('\a') #声音提醒
                
                product_list=self.product_list
                return product_list
        
if __name__ == '__main__':
    lu = Lumoney()
    lu.login()
    
    try_again=True
    try_time=0    
    while try_again:
        try_time = try_time + 1
        print('%s 第%s次尝试...'%(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(time.time())),try_time))
        new_html_str=lu.check_new_p2p()
        transfer_html_str=lu.check_transfer_p2p()
        product_list = lu.select_transfer_p2p(8.4,0,50000)
        
