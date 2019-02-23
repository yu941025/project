__author__ = 'Administrator'
__author__ = 'Administrator'
import time
import requests
from bs4 import BeautifulSoup
import eye_logs
from pyquery import PyQuery as pq
from lxml import etree
import eye_connect
import eye_url
import random
import eye_logs
import threading
import multiprocessing
import agent_pool
logs=eye_logs.logger
def get_cookies():
    a=['cookies.txt','cookies1.txt']
    cookie=random.choice(a)
    a=open(cookie,'r',encoding='utf-8')
    cookies={}
    for i in a.read().split(';'):
        name,value=i.strip().split('=',1)
        cookies[name]=value
    if cookie =='cookies.txt':
        logs.info('13717021587=wzzs0005')
    else :
        logs.info('17199758617=deewis2018')
    return cookies
def get_html(url):
        proxies=agent_pool.test()
        proxies_dict={'http':random.choice(proxies)}

        user_agents=['Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)']
        user_agent=random.choice(user_agents)
        headers={'User-Agent': user_agent,
                 'Connection': 'keep-alive',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 'Upgrade-Insecure-Requests': '1',
                 'Host': 'www.tianyancha.com',
                 'Accept-Encoding': 'gzip, deflate, br'
                 }
        '''resp=requests.get(url,cookies=get_cookies(),headers=headers,proxies=proxies_dict).text
        print(resp)
        return resp
        print(url)'''
        try:
            resp=requests.get(url,cookies=get_cookies(),headers=headers,timeout=5).text
            time.sleep(random.uniform(5,6))
            return resp
        except:
            logs.info('获取response失败')
            return ' '
def html_parse(url):
    html=get_html(url)
    paqu_url=url
    soup=BeautifulSoup(html,'lxml')

    #soup= soup.prettify()
    b=soup.find_all('a',class_='link-nav')
    if not b:
        logs.info('被识别为机器人')
    elif  b[2].text=='登录/注册':
       logs.info('cookies失效，请重新获取登录cookies')
    else:
        save_url(paqu_url)
        try:
            a=soup.find_all('div',class_='result-list')[0].children
            for i in a:
                list=[]
                company=i.find('a',class_='name').text#公司名称
                url=i.find('a',class_='name').get('href')#公司的url
                province=i.find('div',class_='search-result-single').find('span',class_='site').text#公司所在省份
                #print(province)
                faren=i.find('div',class_='content').find('div',class_='info').find('div').find('a').text#公司法人信息
                all_list=i.find('div',class_='search-result-single').find('div',class_='content').find('div',class_='contact').find('div',class_='col')
                #以下为判断有无电话号码或者邮箱，比较复杂，首先判断有无电话和邮箱，然后判断是否有更多的电话以及邮箱
                #print(type(all_list))
                if all_list==None:
                    phone=''
                else:
                    if all_list.find('span',class_='label').text[0:4]=='联系电话':
                        h=all_list.find('script')
                    #print(phone)
                        if h==None:
                            phone=all_list.find_all('span')[1].find('span')
                            if phone==None:
                                phone=''
                            else:
                                phone=phone.text
                        else:
                            phone=h.text
                    else:
                        phone=''
                email_list=i.find('div',class_='search-result-single').find('div',class_='content').find('div',class_='contact').find_all('div',class_='col')
                #print(email_list)
                email=''
                if len(email_list)>1:
                    email_list=email_list[1]
                    h=email_list.find('script')
                    if h:
                        email=h.text
                    else:
                        email=email_list.find_all('span')[1]
                        if email:
                            email=email.text
                        else:
                            email=''
                elif len(email_list)==1:
                    #print(email_list[0])
                    if email_list[0].find('span',class_='lable'):
                        if email_list[0].find('span',class_='lable').text[0:2]=='邮箱':
                            h=email_list.find('script')
                            if h:
                                email=h.text
                            else:
                                email=h.find_all('span')[1]
                else:
                    email=''
                list.append(company)
                list.append(province)
                list.append(city)
                list.append(faren)
                list.append(phone)
                list.append(email)
                list.append(url)
                save_mysql(list)
                print(list)
                print('-------------------------------')
        except:
            print('当前url:%s没有查询到公司'%paqu_url)
def save_mysql(list):
    conn=eye_connect.conn
    cursor=eye_connect.cursor
    save_sql='insert  `{}` (company,province,city,legal_person,phone,email,url) VALUES (%s,%s,%s,%s,%s,%s,%s)'.format(eye_connect.table_name)
    cursor.execute(save_sql,list)
    conn.commit()
def save_url(url):
    conn=eye_connect.conn
    cursor=eye_connect.cursor
    save_url='insert `url` (url) values(%s)'
    try:
        cursor.execute(save_url,url)
        conn.commit()
    except:
        print('当前爬取url保存完成')

if __name__=='__main__':
    city=input('请输入城市：')

    end=''
    for url in eye_url.get_url(city):
        exist_url=eye_connect.ii_list

        if url in exist_url:
            logs.info('%s已爬取'%url)
        else:

            html_parse(url)


