#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import asyncio
import random
import time
from pyppeteer import launch
from retrying import retry


async def taobao_login(url):
    """
    淘宝登录主程序
    :param username: 用户名
    :param password: 密码
    :param url: 登录网址
    :return: 登录cookies
    """
    # 'headless': False如果想要浏览器隐藏更改False为True
    browser = await launch({'headless': False,'args': ['--no-sandbox']})
    page = await browser.newPage()
    # await page.setViewport({ # 最大化窗口
    #     "width": 1920,
    #     "height": 1080
    # })
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    await page.goto(url)
    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    # await page.evaluate('''document.querySelector("#main > div > div.rByMBUmP > div:nth-child(4) > div > div.footer-items > div:nth-child(5) > div.footer-item-text").click()''')
    # await asyncio.wait([page.waitForNavigation(),])
    time.sleep(5)
    await page.evaluate('''document.querySelector("#first > div.login-box > div.phone-login > span").click()''')
    # time.sleep(2)
    # await page.evaluate('''document.querySelector("#user-mobile").()''')
    await page.type('#user-mobile','18316845517')
    time.sleep(2)
    await page.evaluate('''document.getElementById("code-button").click()''')
    time.sleep(2)
    await page.type('#input-code',"12345")
    await page.evaluate('''document.getElementById("submit-button").click()''')






if __name__ == '__main__':
    url = 'http://mobile.yangkeduo.com/login.html?from=http%3A%2F%2Fmobile.yangkeduo.com%2Fpersonal.html%3Frefer_page_name%3Dindex%26refer_page_id%3D10002_1581909644057_dfTGO9Kird%26refer_page_sn%3D10002&refer_page_name=personal&refer_page_id=10001_1581910120934_8t2ak3yhvy&refer_page_sn=10001'
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(taobao_login(url))
    loop.run_until_complete(task)
    # cookie = task.result()
    # print(cookie)