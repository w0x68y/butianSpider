import json
import requests
import time
from bs4 import BeautifulSoup

def spider():
    '''
    爬取所有公益厂商的ID
    保存为id.txt
    :return:
    '''
    headers = {
        'Host': 'butian.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://butian.net/Reward/pub//Message/send',
        'Connection': 'keep-alive'
    }
    cookies={'btlc_':'未登录前的cookie','PHPSE    SSID':'未登录前的cookie','
            __q__':'未登录前的cookie'}
    for i in range(1,149):
        data={
            'p': i,
            'token': ''
        }
        time.sleep(3)
        res = requests.post('http://butian.net/Reward/pub/Message/send',cookies=cookies, data=data,headers=headers,timeout=(4,20))
        allResult = {}
        allResult = json.loads(res.text)
        currentPage = str(allResult['data']['current'])
        currentNum = str(len(allResult['data']['list']))
        print('正在获取第' + currentPage + '页厂商数据')
        print('本页共有' + currentNum + '条厂商')
        for num in range(int(currentNum)):
            print('厂商名字:'+allResult['data']['list'][int(num)]['company_name']+'\t\t厂商类型:'+allResult\
                  ['data']['list'][int(num)]['company_id']+'\t\t厂商ID:'+allResult['data']['list'][int(num)]['company_id'])
            base='http://butian.net/Loo/submit?cid='
            with open('id.txt','a') as f:
                f.write(base+allResult['data']['list'][int(num)]['company_id']+'\n')
def Url():
    '''
    遍历所有的ID
    取得对应的域名
    保存为target.txt
    :return:
    '''
    headers={
        'Host':'butian.net',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh,zh-CN;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
    }
    cookies={'btlc_ba52447ea424004a7da412b344e5e41a':'登录后的cookie','PHPSESSID':'登录后的cookie','':'登录后的cookie'}
    with open('id.txt','r') as f:
        for target in f.readlines():
            target=target.strip()
            getUrl=requests.get(target,headers=headers,cookies=cookies,timeout=(4,20))
            result=getUrl.text
            info=BeautifulSoup(result,'lxml')
            #print(target)
            #print(info)
            url=info.find(name='input',attrs={"name":"host"})
            name = info.find(name='input', attrs={"name": "company_name"})
            lastUrl=url.attrs['value']
            print('厂商:' + name.attrs['value'] + '\t网址:' + url.attrs['value'])
            with open('target.txt','a') as t:
                t.write(lastUrl+'\n')
            time.sleep(3)
    print('The target is right!')
if __name__=='__main__':

    data = {
            's': '1',
            'p': '1',
            'token': ''
        }
    res = requests.post('http://butian.net/Reward/pub/Message/send', data=data)
    allResult = {}
    allResult = json.loads(res.text)
    allPages = str(allResult['data']['count'])
    print('共' + allPages + '页')
    spider()
    Url()
