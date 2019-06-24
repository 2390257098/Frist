import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
import xlrd
import json
import requests
from datetime import datetime



# 读取本地txt文件，转列表
txt1 = open('shop_urls.txt', 'r')
shop_urls = txt1.readlines()
shops = []
for shop in shop_urls:
    shop = shop.replace('\n', '')
    shops.append(shop)
# 创建表格
workbook = xlsxwriter.Workbook(datetime.now().date().isoformat()+'.xlsx')
sheet1 = workbook.add_worksheet('sheet1')
sheet1.write(0, 0, '产品id')
sheet1.write(0, 1, '标题')
sheet1.write(0, 2, '销量')
sheet1.write(0, 3, '评价数量')
sheet1.write(0, 4, '评价星级')
sheet1.write(0, 5, '收藏数')
sheet1.write(0, 6, '原价(美元)')
sheet1.write(0, 7, '促销价(美元)')
# 新建一个产品的列表
product_urls = []
# 读取账号和密码
txt2 = open('email_pwd.txt', 'r')
pwd = txt2.readlines()
email_pwd = []
for w in pwd:
    w = w.replace('\n', '')
    email_pwd.append(w)
# 打开浏览器
option = ChromeOptions()
# option.add_experimental_option('excludeSwitches', ['enable-automation'])
# option.add_argument("--proxy-server=http://115.153.14.157:4549")
# option.add_argument("--headless")
browser = webdriver.Chrome('google\chromedriver.exe', options=option)
wait = WebDriverWait(browser, 60)
browser.set_window_size(1400, 39000)

loginUrl = 'https://login.aliexpress.com/buyer.htm'
browser.get(loginUrl)
time.sleep(5)
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login')))
frame1 = browser.find_element_by_css_selector("#alibaba-login-box")
browser.switch_to_frame(frame1)
# 模拟输入登录的账号
browser.find_element_by_css_selector('#fm-login-id').send_keys(email_pwd[0])
# 模拟输入登录的密码
browser.find_element_by_css_selector('#fm-login-password').send_keys(email_pwd[1])
# 模拟点击登录按钮
# time.sleep(3)
# browser.find_element_by_xpath('//*[@id="login-form"]/div[5]/button').click()
# browser.find_element_by_css_selector('#login-form > div.fm-btn > button').send_keys(Keys.ENTER)
browser.find_element_by_css_selector('#login-form > div.fm-btn').click()
# browser.find_element_by_class_name('fm-button fm-submit password-login').send_keys(Keys.ENTER)
# js = 'document.getElementBySelector("#login-form > div.fm-btn > button").click();'

# browser.execute_script(js)

dict_cookies = browser.get_cookies()
jsonCookies = json.dumps(dict_cookies)
# print(jsonCookies)
# time.sleep(120)
# 保存到本地
with open('cookies.json', 'w') as f:
    f.write(jsonCookies)
time.sleep(3)
# 添加cookies
# browser.add_cookie(browser.get_cookies())
# shops = ['https://www.aliexpress.com/store/all-wholesale-products/2160049.html?spm=a2g1y.12024536.pcShopHead_7975255.1']
# 读取目标文件中的数据，转存进列表

for shop in shops:
    print(shop)
    browser.get(shop)
    time.sleep(3)
    # while True:
        # try:
            # 获取滑块
            # sour = browser.find_element_by_css_selector('#nc_1_n1z')
            # ActionChains(browser).drag_and_drop_by_offset(sour, 400, 0).perform()
            # time.sleep(2)
            # break
        # except Exception as e:
            # print(e)


    # print(browser.get_cookies())
    # 从商家url中获取出店铺id
    shop_id = shop[shop.rfind('all-wholesale-products'):shop.find('.html')][23:]
    html = browser.page_source
    doc = pq(html)
    # 获取该店商品总数，以得到最大页数
    shop_product_num = doc.find('#your-choice > div.result-info').text()[0:-12]
    # 1000以上商品数会表示为 1,000 所以这里需要进行下判断
    if len(shop_product_num) == 5:
        shop_product_num = shop_product_num[:1]+shop_product_num[2:]
    if len(shop_product_num) == 6:
        shop_product_num = shop_product_num[:2]+shop_product_num[3:]
    print('本店商品数为：'+shop_product_num)
    if shop_product_num == '':
        break
    else:
        # 如果余数为0，再判断
        if int(int(shop_product_num)%36) == 0:
            page = int(int(shop_product_num)/36)
            # print('本店商品页数为：'+page)
            # print('本店商品有多页哦！')
            for i in range(1, page + 1):
                # id为店铺id  从店铺的url中可以获取到
                shop_page_url = shop[0:shop.rfind('all-wholesale-products')] + shop_id + '/search/' + str(i) + '.html'
                browser.get(shop_page_url)
                time.sleep(3)
                html = browser.page_source
                doc = pq(html)
                items = doc('#node-gallery > div.module.m-o.m-o-large-all-detail > div > div > ul > li').items()
                for item in items:
                    #  进入列表拿到每个商品的url
                    product_url = 'https:'+item.find('div.detail > h3 > a').attr('href')
                    # print(product_url)
                    #  加进集合中
                    product_urls.append(product_url[0:product_url.rfind('.html')] + '.html')

        else:
            page = int(int(shop_product_num)/36+1)
            # print('本店商品页数为：' + page)
            for i in range(1, page + 1):
                # id为店铺id  从店铺的url中可以获取到

                shop_page_url = shop[0:shop.rfind('all-wholesale-products')] + shop_id + '/search/' + str(i) + '.html'
                browser.get(shop_page_url)
                time.sleep(3)
                html = browser.page_source
                doc = pq(html)
                items = doc('#node-gallery > div.module.m-o.m-o-large-all-detail > div > div > ul > li').items()
                for item in items:
                    #  进入列表拿到每个商品的url
                    product_url = 'https:'+item.find('div.detail > h3 > a').attr('href')
                    # print(product_url)
                    #  加进集合中
                    product_urls.append(product_url[0:product_url.rfind('.html')] + '.html')

    # wait.until(EC.presence_of_element_located(
       #(By.CSS_SELECTOR, '#node-gallery > div.module.m-o.m-o-large-all-detail > div > div > ul')))
# 退出，清除浏览器缓存
# 读取cookies
cookie = open(r'cookies.json','r')#打开所保存的cookies内容文件
cookies = {}#初始化cookies字典变量
for line in cookie.read().split(';'):  #按照字符：进行划分读取
  #其设置为1就会把字符串拆分成2份

  name, value = line.strip().split('=', 1)
  cookies[name] = value
product_num = len(product_urls)
print('今日爬取产品总数是：'+str(product_num))
for i in range(1, product_num+1):
    # document = requests.get(product_urls[i-1])
    browser.get(product_urls[i - 1])
    time.sleep(3)
    html = browser.page_source
    doc = pq(html)
    title = doc.find('#j-product-detail-bd > div.store-detail-main > div > h1').text()
    order = doc.find('#j-order-num').text()[0:-6]
    comment_num = doc.find('#j-product-tabbed-pane > ul > li:nth-child(2) > a').text()[10:-1]
    if comment_num == '0':
        comment_num = ' '
    grade = doc.find('#j-customer-reviews-trigger > span.percent-num').text()
    like = doc.find('#j-product-action-block > span.product-action-main > div').text()
    Price = doc.find('#j-sku-price').text()
    Discount_Price = doc.find('#j-sku-discount-price').text()
    sheet1.write(i, 0, product_urls[i - 1][-16:-5])
    sheet1.write(i, 1, title)
    sheet1.write(i, 2, order)
    sheet1.write(i, 3, comment_num)
    sheet1.write(i, 4, grade)
    sheet1.write(i, 5, like)
    sheet1.write(i, 6, Price)
    sheet1.write(i, 7, Discount_Price)
    print(like)
    # doc = BeautifulSoup(soup, 'html.parser')







    # time.sleep(3)
    # 等待页面加载
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#bd')))


browser.quit()
product_urls.clear()
workbook.close()




