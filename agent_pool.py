__author__ = 'Administrator'
import requests
import eye_connect
import random
from pyquery import PyQuery as pq
def get_proxiex():
    for i in range(1,6):
        url='https://www.kuaidaili.com/free/inha/%s/'%i

        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        resp=requests.get(url,headers=headers)
        doc=pq(resp.text)
        h=doc('#list .table tbody tr ')
        for i in h:
            proxies=[]
            ip=i.find('td[1]').text
            port=i.find('td[2]').text
            type=i.find('td[4]').text
            speed=i.find('td[5]').text
            proxies.append(type)
            proxies.append(ip)
            proxies.append(port)
            yield proxies
def insert():
    test_url='https://www.baidu.com/'
    proxies={}
    conn=eye_connect.conn
    cursor=eye_connect.cursor
    for i in get_proxiex():
        proxies[i[0]]=i[1]+':'+i[2]
        #print(i)
        #print(i[1])
        #print(eye_connect.ip_tuple)
        sql='insert proxies (type,ip,port) values(%s,%s,%s)'
        if eye_connect.ip_tuple==()  :

            cursor.execute(sql,i)
            conn.commit()
        elif i[1] not in eye_connect.ip_tuple:
                    cursor.execute(sql,i)
                    conn.commit()
def test():
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url='https://www.baidu.com/'
    resp=requests.get(url,headers=headers)
    status=resp.status_code
    conn=eye_connect.conn
    cursor=eye_connect.cursor
    sql='select * from proxies'
    cursor.execute(sql)
    h=cursor.fetchall()
    #print(h)
    #print(len(h))
    dict=[]
    for i in h:
        if status==200:
            #print(i)
            dict.append(i[1]+':'+i[2])
    return dict
if __name__=='__main__':
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    insert()
