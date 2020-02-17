import tkinter
from tkinter import ttk
import tkinter.messagebox
import json
import requests
import queue
import time

class MyFrame5():
    def __init__(self):
        self.temp = list()
        self.name_temp = list()
        self.window = tkinter.Tk()
        self.window.title('音乐下载器')
        self.window.geometry("600x500+200+20")
        self.label1 = tkinter.Label(self.window, text="请输入歌曲名称")
        self.Entry1 = tkinter.Entry(self.window, bd=5,width=50)
        self.Button1 = tkinter.Button(self.window,text="点击按钮",command=self.search_music)
        self.lb = tkinter.Listbox(self.window,width=50,selectmode="browse")
        self.lb.bind("<<ListboxSelect>>",self.show_button)
        self.Button2 = tkinter.Button(self.window,text="下载",command=self.down_load,width=40)

    #发送请求
    def parse_url_text(self,url):
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            }
        response = requests.get(url, headers=header, verify=False, timeout=5)  # 发送请求
        return response.content  # 获取element 类型的html

    #显示下载按钮
    def show_button(self,*args):
        self.Button2.place(x=130,y=250)

    def search_music(self):
        search = self.Entry1.get()
        print(search)
        url = "https://api.imjad.cn/cloudmusic/?type=search&search_type=1&s={}".format(search)
        param = self.parse_url_text(url)
        print(param)
        param = json.loads(param)
        for pa in param['result']['songs']:
            self.lb.insert(1,pa['name']+"---"+pa['ar'][0]['name'])
            self.temp.append(pa['id'])
            self.name_temp.append(pa['name'])
        self.lb.place(x=110,y=50)
    #下载文件
    def download(self,url,path,name):
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
            with open(path,"wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data) #已下载文件大小
                    print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size * 50 / int(content_size)),float(size / int(content_size) * 100)),end='')
            end = time.time()
            # print('\n',"全部下载完成！用时%.2f秒"%(end - start))
            tkinter.messagebox.showinfo('提示','全部下载完成！用时{}秒'.format(float(end-start)))

    def down_load(self,*args):
        data = self.lb.curselection()   #选择的歌曲
        param = self.temp[data[0]]
        url = "http://music.163.com/song/media/outer/url?id={}.mp3".format(param)
        path = "music/{}.mp3".format(self.name_temp[data[0]])
        self.download(url,path,self.name_temp[data[0]])
        return

    def run(self):
        self.label1.place(x=10,y=10)
        self.Entry1.place(x=110,y=10)
        self.Button1.place(x=480,y=10)
        self.window.mainloop()

if __name__ == "__main__":
    data = MyFrame5()
    data.run()
