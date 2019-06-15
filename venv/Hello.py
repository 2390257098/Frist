import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

# 思路：打开当前店铺，获取店内产品总页数(部分商店货物种类少，只有一页)，然后替换url中的分页部分，获取店内所有产品的url，放在一个列表里，接着再用浏览器打开产品的链接，从链接里截取出产品的id，此时找到其他需要的数据，统一存入excel表格中

option = ChromeOptions()
# option.add_argument("--headless")
browser = webdriver.Chrome(r'D:\dev\tool\google\chromedriver.exe', options=option)
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 39000)
# 登录页       https://login.aliexpress.com/buyer.htm

loginUrl = 'https://login.aliexpress.com/buyer.htm'
# 店家url
url = 'https://www.aliexpress.com/store/all-wholesale-products/2160049.html?spm=a2g1y.12024536.pcShopHead_7975255.1'
# 产品url https://www.aliexpress.com/store/product/Anfilite-E31-Pro-4G-Car-Camera-GPS-7-8-Android-5-1-Car-DVRs-WIFI-1080P/2160049_32969052433.html?spm=2114.12010615.8148356.2.2a0749b7FWNSW9
productUrl = 'https://www.aliexpress.com/store/product/Anfilite-E31-Pro-4G-Car-Camera-GPS-7-8-Android-5-1-Car-DVRs-WIFI-1080P/2160049_32969052433.html?spm=2114.12010615.8148356.2.2a0749b7FWNSW9'
email = '2390257098@qq.com'
password = '986946Lhb'

browser.get(productUrl)
time.sleep(3)
# //*[@id="fm-login-id"] 账号输入框
# //*[@id="fm-login-password"] 密码输入框
# //*[@id="login-form"]/div[5]/button 提交按钮
# browser.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(email)
# browser.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)
# browser.find_element_by_xpath('//*[@id="login-form"]/div[5]/button').submit()
# cookies = browser.get_cookies()
# print(cookies)
# browser.add_cookie(cookies)
# cookie1 = driver.get_cookies()
# print(cookie1)
# elem = driver.find_element_by_xpath("//*[@id="(login)"]/div/div/div[3]/button");
# elem.send_keys(Keys.ENTER)


# url = 'https://www.aliexpress.com/store/all-wholesale-products/2160049.html?spm=a2g1y.12024536.pcShopHead_7975255.1'
# browser.get(url)
# page = browser.find_element_by_xpath()
time.sleep(3)
html = browser.page_source
doc = pq(html)
title = doc.find('#j-product-detail-bd > div.store-detail-main > div > h1').text()
orders = doc.find('#j-order-num').text()
print(title)
print(orders)

