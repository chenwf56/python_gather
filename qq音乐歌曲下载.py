import time
import requests
import json
from lxml import etree
import re
import os

class QQYY:
    def __init__(self,search):
        self.search = search
        self.rank_temp = {}
        self.music_temp = list()
        self.music_list = list()

    #qq音乐请求
    def parse_url(self,url):
        headers = {
            "cookie": "pgv_pvi=5625868288; pgv_pvid=6141645905; RK=RBSUK+6JOW; ptcz=cdef6cff9af21525e9427133524fc8eea69a8e3f59ffd391c6821504675471a9; tvfe_boss_uuid=8a90d517dcf4716d; yqq_stat=0; pgv_si=s5905078272; pgv_info=ssid=s723007990; ts_refer=www.google.com/; ts_uid=7650158627; _qpsvr_localtk=0.1781074620039933; wxuin=o1152921504690979851; qm_keyst=263CB9102E15019B1FC66985EDC3D87CE5B606EB7E0CF200D460715984CC56EA; qqmusic_key=263CB9102E15019B1FC66985EDC3D87CE5B606EB7E0CF200D460715984CC56EA; p_lskey=263CB9102E15019B1FC66985EDC3D87CE5B606EB7E0CF200D460715984CC56EA; wxopenid=opCFJwx-x_goXRhXCAD6RHJTpB_k; wxrefresh_token=30_EGdmjbW_WF_i-9ajYRtvmJZwQLv4nbd0gbJno0u_xVTHJDL9046DKFdixfuibjPrvnI9X99TgOp3rj4vSb7VVgQj9dfZhvjvIdzJN92cVyw; wxunionid=oqFLxsuup64zcR4h_ZXnbd-DfJCI; login_type=2; player_exist=1; qqmusic_fromtag=66; userAction=1; ts_last=y.qq.com/portal/player.html; yplayer_open=1; yq_index=0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
            "origin": "https://y.qq.com",
            "referer": "https://y.qq.com/portal/player.html"
        }
        return requests.get(url,headers=headers).text

    #下载歌曲
    def download(self,url,path,name,types):
        start = time.time() #下载时间
        size = 0
        header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        }
        response = requests.get(url,stream=True,headers=header)
        chunk_size = 1024 #每次下载时间
        content_size = response.headers['Content-Length']   #下载文件总大小
        if response.status_code == 200:
            print(name+' [文件大小]:%0.2f MB' % (int(content_size) / int(chunk_size) / 1024)) #转为MB
            name = name.replace("?",'').replace(" ",'').replace('/','--')
            with open(path+'/'+name+types,"wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data) #已下载文件大小
                    print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size * 50 / int(content_size)),float(size / int(content_size) * 100)),end='')
            end = time.time()
            print('\n',"全部下载完成！用时%.2f秒"%(end - start))

    #搜素歌曲
    def search_music(self,search,types):
        #types 参数 {"song":"单曲","playlist","歌单","user":"用户","lyric","歌词","mv","视频"}
        if(types == "song"):
            url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=68000383296028367&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w={}&g_tk=2071065558&loginUin=1152921504690979851&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0".format(search)
        elif(types == "playlist"):
            url = "https://c.y.qq.com/soso/fcgi-bin/client_music_search_songlist?remoteplace=txt.yqq.playlist&searchid=113992946117054896&flag_qc=0&page_no=0&num_per_page=5&query={}&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0".format(search)
        elif(types == "user"):
            url = "https://c.y.qq.com/soso/fcgi-bin/client_search_user?ct=24&qqmusic_ver=1298&p=1&n=10&searchid=239454069024609106&remoteplace=txt.yqq.user&w={}&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0".format(search)
        elif(types == "mv"):
            url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&remoteplace=txt.yqq.mv&searchid=143260592734291418&aggr=0&catZhida=1&lossless=0&sem=1&t=12&p=1&n=12&w={}&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0".format(search)
        elif(types == "lyric"):
            url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&remoteplace=txt.yqq.lyric&searchid=143260592734291418&aggr=0&catZhida=1&lossless=0&sem=1&t=12&p=1&n=12&w={}&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0".format(search)
        param = json.loads(self.parse_url(url))
        return param

    #下载MV
    def down_music_mv(self,param):
        for li in param['data']['mv']['list']:
            data = {"getMvUrl":{"module":"gosrf.Stream.MvUrlProxy","method":"GetMvUrls","param":{"vids":["z0033q8n2d0"],"request_typet":10001}}}
            data['getMvUrl']['param']['vids'][0] = li['v_id']
            url = "https://u.y.qq.com/cgi-bin/musicu.fcg?data={}&g_tk=5381&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=GB2312&notice=0&platform=yqq&needNewCode=0".format(data)
            url = url.replace("\'",'\"')
            mv_param = json.loads(self.parse_url(url))
            down_url = mv_param['getMvUrl']['data'][li['v_id']]['mp4'][4]['freeflow_url'][0]
            path = 'mv'
            if not os.path.exists(path):
                os.makedirs(path)
            self.download(down_url,path,li['mv_name']+"----"+li['singerName_hilight'],'.mp4')

    #获取下载歌曲地址
    def music_url(self,mid):
        data = {"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"6141645905","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"6141645905","songmid":["0001z7wz1MFXRj"],"songtype":[0],"uin":"1152921504690979851","loginflag":1,"platform":"20"}},"comm":{"uin":"1152921504690979851","format":"json","ct":24,"cv":0}}
        data['req_0']['param']['songmid'][0] = mid
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey765670550297842&g_tk=2071065558&loginUin=1152921504690979851&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={}".format(data)
        url = url.replace("\'",'\"')
        param = json.loads(self.parse_url(url))
        return "http://157.255.154.160/amobile.music.tc.qq.com/"+param['req_0']['data']['midurlinfo'][0]['purl']

    #获取排行榜歌曲
    def get_ranking(self):
        url = "https://y.qq.com/n/yqq/toplist/4.html"
        param = etree.HTML(self.parse_url(url))
        return param.xpath('//div[@class="toplist_nav"]//dd/a/@href'),param.xpath('//div[@class="toplist_nav"]//dd/a/text()')  #TopId

    #下载排行榜歌曲
    def down_ranking(self,top_id):
        data = {"detail":{"module":"musicToplist.ToplistInfoServer","method":"GetDetail","param":{"topId":0,"offset":0,"num":100,"period":"2020-02-13"}},"comm":{"ct":24,"cv":0}}
        data['detail']['param']['topId'] = int(top_id)
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI058852664908423113&g_tk=2071065558&loginUin=1152921504690979851&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={}".format(data)
        url = url.replace("\'",'\"')
        param = json.loads(self.parse_url(url))
        if(len(param['detail']['data']['songInfoList']) < 1):
            url = url.replace("2020-02-13","2020_7")
            param = json.loads(self.parse_url(url))
        if(len(param['detail']['data']['songInfoList']) < 1):
            url = url.replace("2020_7","2020_6")
            param = json.loads(self.parse_url(url))
        for pa in param['detail']['data']['songInfoList']:
            print(pa['mid'])
            down_url = self.music_url(pa['mid'])
            path = 'music/{}/'.format(param['detail']['data']['data']['title'])
            if not os.path.exists(path):
                os.makedirs(path)
            self.download(down_url,path,pa['singer'][0]['name']+"----"+pa['name'],'.mp3')

    #搜索下载歌曲
    def music_run(self):
        param = self.search_music(self.search,'song')
        for info in param['data']['song']['list']:
            down_url = self.music_url(info['mid'])
            self.download(down_url,'music/',info['singer'][0]['name']+"----"+info['name'],'.mp3')

    #下载所有排行榜
    def down_rank_run(self):
        data,name = self.get_ranking()
        for da in data:
            top_id = re.findall('(\d+)+',da)
            if(len(top_id)<1):
                continue
            self.down_ranking(top_id[0])

    def run(self):
        search = input(
'''
选择操作
1:下载排行榜数据
2:搜索
3:退出
''')
        try:
            int(search)
            if(int(search) == ""):
                print('你输入有误')
        except:
            print('！！！！请输入数字')
        if(int(search) == 1):   #下载指定排行榜
            top_id,name = self.get_ranking()
            i = 1
            rank_temp = ''
            temps = list()
            for na,top in zip(name,top_id):
                topid = re.findall('(\d+)+',top)
                if(len(topid)<1):
                    continue
                self.rank_temp[na] = topid[0]
                rank_temp += str(i)+":"+na+"\n"
                temps.append(na)
                i += 1
            ranks = int(input(rank_temp))
            self.down_ranking(self.rank_temp[temps[ranks-1]])
        elif(int(search) == 2):
            music_temp = ''
            temp = {}
            self.music_temp = ['song','playlist','user','lyric','mv']
            keyword = input('请输入搜索关键字:')
            search_music = int(input(
'''
1:单曲
2:歌单
3:用户
4:歌词
5:MV
'''          ))
            param = self.search_music(keyword,self.music_temp[search_music-1])
            if(self.music_temp[search_music-1] == "song"):
                i = 1
                for info in param['data']['song']['list']:
                    music_temp += str(i)+":"+info['singer'][0]['name']+"---"+info['name']+"\n"
                    i += 1
                    temp['mid'] = info['mid']
                    temp['name'] = info['name']
                    temp['author'] = info['singer'][0]['name']
                    self.music_list.append(json.dumps(temp))
                mid_number = int(input(music_temp))
                music_list_temp = json.loads(self.music_list[mid_number-1])
                print(music_list_temp['mid'])
                down_url = self.music_url(music_list_temp['mid'])
                print(down_url)
                self.download(down_url,'music/',music_list_temp['author']+"----"+music_list_temp['name'],'.mp3')
            elif(self.music_temp[search_music-1] == "mv"):
                self.down_music_mv(param)
            self.run()
        elif(search == 3):
            os._exit()


if __name__ == "__main__":
    search  = '麻雀'
    qq = QQYY(search)
    qq.run()