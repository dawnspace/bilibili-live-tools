import asyncio
import random
from struct import *
import json
import datetime
import time
import hashlib
import requests
import datetime
cookies = ''
headers = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Accept-Language' : 'zh-CN,zh;q=0.9',
    'accept-encoding':'gzip, deflate',
    'authority': 'live.bilibili.com',
    'cookie': cookies,
}
while 1:
	for i in range(31,50):
		params={
			'aid': i,
		}
		url='https://api.live.bilibili.com/lottery/v1/box/getStatus'
		respone = requests.get(url,params=params, headers=headers)
		if respone.json()['code']!=-400:
			respone_start= respone.json()['data']['typeB'][0]['join_start_time']
			respone_end= respone.json()['data']['typeB'][0]['join_end_time']
			current=int(time.mktime(datetime.datetime.now().timetuple()))
			if current>respone_start and current<respone_end:
				for num in range(1,3):
					params_pres={
						'aid': i,
						'number':num
					}
					url_pres='https://api.live.bilibili.com/lottery/v1/box/draw'
					respone_pres = requests.post(url_pres,params=params_pres, headers=headers).json()['msg']
					#print(respone_pres)
					title= respone.json()['data']['title']
					if respone_pres==0:	
						print("活动%s加入成功"%title)
					else:
						print("活动%s加入失败,%s"%(title,respone_pres))
		#time.sleep(3600)
