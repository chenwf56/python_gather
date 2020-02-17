import requests
import queue
from lxml import etree
import execjs
import re
import json
import warnings
import time
warnings.filterwarnings('ignore')

#链接队列
video_url = queue.Queue()
video_title = queue.Queue()
video_data = queue.Queue()

def download(url,path,name):
    start = time.time() #下载时间
    size = 0
    response = requests.get(url,stream=True)
    chunk_size = 1024 #每次下载时间
    content_size = response.headers['Content-Length']   #下载文件总大小
    if response.status_code == 200:
        print(name+' [文件大小]:%0.2f MB' % (int(content_size) / int(chunk_size) / 1024)) #转为MB
        with open(path,"wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                size += len(data) #已下载文件大小
                print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size * 50 / int(content_size)),float(size / int(content_size) * 100)),end='')
        end = time.time()
        print('\n',"全部下载完成！用时%.2f秒"%(end - start))

def parse_url_xpath(url):
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "upgrade-insecure-requests": "1",
    }
    response = requests.get(url, headers=header, verify=False, timeout=5)  # 发送请求
    return etree.HTML(response.content)  # 获取element 类型的html

number = int(input("请输入采集页数:"))
for i in range(1,number):
    url = "https://52op.net/video/"
    if(i > 1):
        url = "https://52op.net/video/index_{}.html".format(i)
    gcw_param = parse_url_xpath(url)
    url = gcw_param.xpath('//div[@class="contentBox"]//div[@class="a_imgBox"]//a/@href')
    for u in url:
        url_s = re.findall('https://52op.net/video/(.*).html',u)
        video_url.put(url_s[0])

for num in range(video_url.qsize()):
    url_list = "https://52op.net/flvData/d.aspx?id={}".format(video_url.get())
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "upgrade-insecure-requests": "1"
    }
    param = requests.get(url_list,headers=header).text
    data = json.loads(param)
    video_param = requests.get(data['Data']['MP4']).content
    path = 'video/{}{}'.format(data['Name'],'.mp4')
    download(data['Data']['MP4'],path,data['Name'])
