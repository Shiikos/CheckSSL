# -*- coding: utf-8 -*-  
# python3

from typing import Counter, ValuesView
import requests
import json
import time
import os
import hashlib
import sys

sslurl = 'www.baidu.com'
ftqq = ''

webhook = ''

# 获取SSL证书状态
def getSSLstatus():
    global forcast
    forcast = ""
    # 读取json文件
    with open("output/ct.json",'r') as load_sslststus:
        load = json.load(load_sslststus)
        print(load)
    print("---------------------")
    #reponse = json.dumps(load)
    #reponse = json_data.json()
    reponse = load
    print(len(reponse))
    
    counter = 0
    # 组装结果
    while(counter < len(reponse)):
        forcast = '网站' + '：'  + reponse[counter]['domain'] + '\n' + '状态' + '：'  + reponse[counter]['statuscolor'] + "\n —————————— \n" + forcast + "  \n  "
        counter += 1
    
    return forcast + "  \n  "
    

# 发送结果
def sendKim(content):
    print(" 开始发送 Kim 信息 \n")
    webhook_url = webhook
    KimHeader = {"Content-Type": "application/json", "Charset": "UTF-8"}
    KimMessage = {
        "msgtype": "markdown",
        "markdown": {
            "content":f'【SSL即将到期】\n{content}'
        }
    }
    r = requests.post(url=webhook_url,
                      headers=KimHeader,
                      data=json.dumps(KimMessage))
    
    
    if r is None:
        print("kim 返回结果 ", r)
        return False
    
    print("kim 发送消息回来的全部结果 ", r.json())

    if r.status_code == 200:
        print("[+]KIM消息推送成功，请查收  ", r.json())
        return True
    else :
        print("[+]KIM消息推送失败，请查收  ", r.json())
        return False
   
def process():
    print("start process")

    #执行checker.sh
    print(os.system("bash checker.sh " + sslurl))

    time.sleep(10)
    
    #获取ssl证书状态
    content = getSSLstatus()
    
    #发送结果
    return sendKim(content)
        

def sendCheckmassage():
    counter = 0
    
    # 重试发送
    while(counter < 3):
        res = process()
        
        # 成功就返回
        if res:
            return
        
        counter += 1
       
    # 处理失败
    # 失败三次发送报警
    requests.get(ftqq).json
    
def main():
    while(True) :
        now = time.localtime(time.time())
        hour = now.tm_hour
        min = now.tm_min
        
        #判断时间是否开始处理
        if hour >= 7 and hour <= 9:
            #判断时间是8点，否则睡 30s
            if hour == 8 and min >= 00:
                counter = 0
                
                sendCheckmassage()    
                #无论是否处理成功，都睡 20 小时    
                time.sleep(60*60*20)
            else:
                print("sleep 30s", now)
                time.sleep(30)
        else:
            time.sleep(60*60)   
 
def main_handler(event, context):
    return main()

 
if __name__ == '__main__':
    main()
