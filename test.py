import json
import requests


headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
url='https://rate.taobao.com/feedRateList.htm?auctionNumId=539964349896&userNumId=436848847&currentPageNum=2&pageSize=20'
res=requests.get(url,headers=headers)
strJson=res.text
strJson=strJson[:-2]
strJson=strJson[3:]
json_data=json.loads(strJson)
for comment in json_data["comments"]:
    print(comment["content"])
    print(comment["date"])
    print(comment["auction"]["sku"])
