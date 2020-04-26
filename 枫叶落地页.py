from requests_html import HTMLSession
import requests
import random
import json

session = HTMLSession()
#请求发送
def getCitoken():
    headers = {
        "Accept":"application/json, text/plain, */*",
        "Host":"ec.fy.qq.com",
        "Referer":"https://ec.fy.qq.com/editor/message/index?code=132000&platform=fyec&f_id=gdt_15102326",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Referer":"https://ec.fy.qq.com/editor/message/index?code=132000&platform=fyec&f_id=gdt_15102326",
        "Sec-Fetch-Site":"same-origin",
        "cookie":"pac_uid=0_f7b4ca2a407dc; XWINDEXGREY=0; pgv_pvid=4493696816; pgv_pvi=4617995264; ptui_loginuin=1162850810; RK=W05hGfazdf; ptcz=7bba34f76698bbd37133b7d6f68eb6d6a8218aa7982c27776f6183a7d255a2df; Hm_lvt_f60b4fa70e7d559cd06dc45d240b8b96=1585905074,1586237804,1586316721; Hm_lpvt_f60b4fa70e7d559cd06dc45d240b8b96=1586317892; pgv_si=s839470080; _qpsvr_localtk=0.7762047435395496; fyec_platform=fyec; fyec_utype=11; fyec_sign=fyec_TGT-22757-W3n0siu9XbFnYH7Eup6Y6gXhgSeMSi2hFujOY8WMTMXeIEsZaEp2IamWm7oxaJB5; fyec_login_id=D4D806ED0855A2154269A3A7D0331F06"
    }
    url = 'https://ec.fy.qq.com/misc/token/getcitoken?f_id=gdt_15102326'
    session.get('https://ec.fy.qq.com/editor/message/index?code=132000&platform=fyec&f_id=gdt_15102326',headers=headers)
    data = session.get(url,headers=headers).text
    jsonData = json.loads(data)
    return jsonData['data']['citoken']

# 获取用户信息
def choosePost(citoken):
    url = "https://ec.fy.qq.com/editor/fyuser/choose?f_id=gdt_15102326"
    headers = {
        "Accept":"application/json, text/plain, */*",
        "Host":"ec.fy.qq.com",
        "Referer":"https://ec.fy.qq.com/editor/message/index?code=132000&platform=fyec&f_id=gdt_15102326",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Origin":"https://ec.fy.qq.com",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "cookie":"fyec_platform=fyec; fyec_utype=11; fyec_login_id=D4D806ED0855A2154269A3A7D0331F06;fyec_sign=fyec_TGT-17798-iiZJKhVqUrS8R2M_CRE30fxKf2xQw7XBozBhzeQua_xNxpNKGTQMOeuXPropVySR"
    }
    data = {
        "citoken":citoken
    }
    data = session.post(url,headers=headers,data=data).text
    return data

# 获取订单信息
def getOrder(citoken):
    url = "https://ec.fy.qq.com/editor/order/orderlist?f_id=gdt_15102326"
    headers = {
        "Accept":"application/json, text/plain, */*",
        "Host":"ec.fy.qq.com",
        "Referer":"https://ec.fy.qq.com/editor/message/index?code=132000&platform=fyec&f_id=gdt_15102326",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Referer":"https://ec.fy.qq.com/editor/message/index?code=132000&platform=fyec&f_id=gdt_15102326",
        "Sec-Fetch-Site":"same-origin",
        # "cookie":"pac_uid=0_f7b4ca2a407dc; XWINDEXGREY=0; pgv_pvid=4493696816; pgv_pvi=4617995264; ptui_loginuin=1162850810; RK=W05hGfazdf; ptcz=7bba34f76698bbd37133b7d6f68eb6d6a8218aa7982c27776f6183a7d255a2df; Hm_lvt_f60b4fa70e7d559cd06dc45d240b8b96=1585905074,1586237804,1586316721; Hm_lpvt_f60b4fa70e7d559cd06dc45d240b8b96=1586317892; pgv_si=s839470080; _qpsvr_localtk=0.7762047435395496; fyec_platform=fyec; fyec_utype=11; fyec_sign=fyec_TGT-22757-W3n0siu9XbFnYH7Eup6Y6gXhgSeMSi2hFujOY8WMTMXeIEsZaEp2IamWm7oxaJB5; fyec_login_id=D4D806ED0855A2154269A3A7D0331F06"
    }
    data = {
        "page":1,
        "order_status":-1,
        "express_type":-1,
        "delete":0,
        "startTime":"2019-10-11",
        "endTime":"2020-04-08",
        "citoken":citoken
    }
    data = requests.post(url,headers=headers,data=data).text
    return data

def getGoodTypeList(citoken):
    url = "https://ec.fy.qq.com/editor/goodstype/getgoodstypelist?f_id=gdt_15102326"
    headers = {
        "Accept":"application/json, text/plain, */*",
        "Host":"ec.fy.qq.com",
        "Referer":"https://ec.fy.qq.com/editor/goods/index?f_id=gdt_15102326",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Sec-Fetch-Site":"same-origin",
        "Origin":"https://ec.fy.qq.com",
        "cookie":"pac_uid=0_f7b4ca2a407dc; XWINDEXGREY=0; pgv_pvid=4493696816; pgv_pvi=4617995264; ptui_loginuin=1162850810; RK=W05hGfazdf; ptcz=7bba34f76698bbd37133b7d6f68eb6d6a8218aa7982c27776f6183a7d255a2df; Hm_lvt_f60b4fa70e7d559cd06dc45d240b8b96=1585905074,1586237804,1586316721; Hm_lpvt_f60b4fa70e7d559cd06dc45d240b8b96=1586317892; pgv_si=s839470080; _qpsvr_localtk=0.7762047435395496; fyec_platform=fyec; fyec_utype=11; fyec_sign=fyec_TGT-22757-W3n0siu9XbFnYH7Eup6Y6gXhgSeMSi2hFujOY8WMTMXeIEsZaEp2IamWm7oxaJB5; fyec_login_id=D4D806ED0855A2154269A3A7D0331F06"
    }
    data = {
        "page":1,
        "pageSize":200,
        "citoken":citoken,
    }
    data = requests.post(url,headers=headers,data=data).text
    return data

citoken = getCitoken()
print(citoken)
# param = getOrder(citoken)
# param = getGoodTypeList(citoken)
param = choosePost(citoken)
print(param)