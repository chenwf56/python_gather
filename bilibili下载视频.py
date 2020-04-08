import requests
import time
import json
import os

def parse_url(url):
    header = {
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Host":"api.bilibili.com",
        "Referer":"https://www.bilibili.com/video/BV18J411W7cE?from=search&seid=5890807082354848965",
        "Origin":"https://www.bilibili.com",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    response = requests.get(url,headers=header).text
    return response

def download(url,path):
    header = {
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    start = time.time() #下载时间
    size =0
    response = requests.get(url,headers=header,stream=True)
    chunk_size =1024    #每次下载时间
    content_size = response.headers['Content-Length']   #下载文件总大小
    if response.status_code == 200:
        print('[文件大小]:%0.2f MB'% (int(content_size) / int(chunk_size) /1024)) #转为MB
        with open(path,"wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                size +=len(data) #已下载文件大小
                print('\r'+'[下载进度]:%s%.2f%%'% ('>'*int(size *50 / int(content_size)),float(size /int(content_size)  * 100)),end='')
        end = time.time()
        print('\n',"全部下载完成！用时%.2f秒"%(end - start))


if __name__ == "__main__":
    url = "https://api.bilibili.com/x/web-interface/view?cid=137902788&bvid=BV18J411W7cE"
    avid_param = json.loads(parse_url(url))
    avid = avid_param['data']['aid']
    title = avid_param['data']['title']
    for param in avid_param['data']['pages']:
        url = "https://api.bilibili.com/x/player/playurl?avid={}&cid={}&pn=112".format(avid,param['cid'])
        urlData = json.loads(parse_url(url))
        video_url = urlData['data']['durl'][0]['url']
        path = param['part']+'.mp4'
        if(os.path.exists(title) == False):
            os.mkdir(title)
        path = "{}/{}".format(title,path)
        download(video_url,path)


