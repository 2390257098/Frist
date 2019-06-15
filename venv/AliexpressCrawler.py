import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pandas as pd
import xlsxwriter
import xlrd

date = time.strftime("%Y%m%d", time.localtime())
workbook = xlsxwriter.Workbook(r'.xlsx')
sheet1 = workbook.add_worksheet('sheet1')
sheet1.write(0,0,'id')
sheet1.write(0,1,'标题')
sheet1.write(0,2,'销量')
sheet1.write(0,3,'评价数量')
sheet1.write(0,4,'评价星级')
sheet1.write(0,5,'收藏数')
sheet1.write(0,6,'原价')
sheet1.write(0,7,'促销价')
workbook.close()
# 打开浏览器
option = ChromeOptions()
# option.add_argument("--headless")
browser = webdriver.Chrome(r'D:\dev\tool\google\chromedriver.exe', options=option)
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 39000)

loginUrl = 'https://login.aliexpress.com/buyer.htm'
shopUrlList = ['https://www.aliexpress.com/store/all-wholesale-products/2160049.html?spm=a2g1y.12024536.pcShopHead_7975255.1']
# 登录，拿cookie
browser.get(loginUrl)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#fm-login-id')))
html = browser.page_source
doc = pq(html)
# 模拟输入登录的账号
browser.find_element_by_css_selector('#fm-login-id').send_keys('2390257098@qq.com')
# 模拟输入登录的密码
browser.find_element_by_css_selector('#fm-login-password').send_keys('986946Lhb')
# 模拟点击登录按钮
browser.find_element_by_css_selector('#login-form > div.fm-btn > button').submit()
print(browser.get_cookies())
# 添加cookies
browser.add_cookie(browser.get_cookies())
# 新建一个产品的列表
productUrls = []
# 从店铺url列表里一条一条的拿出来，访问店铺
for shopUrl in shopUrlList:
    browser.get(shopUrl)
    time.sleep(2)  # 这里的时间以秒为单位
    html = browser.page_source
    doc = pq(html)
    # 拿到店内商品总页数
    if doc.__contains__('ui-pagination ui-pagination-body util-clearfix'):
        # 获取
        pages = doc('#pagination-bottom > div.ui-pagination-navi.util-left > a').items()
        page = len(pages)
        for i in range(1, page):
            shop_page_url = shopUrl[0:shopUrl.rfind('all-wholesale-products')]+id+search/+i+'.html'
            browser.get(shop_page_url)
            #  拿到商品列表
            items = doc('#list-container > li').items()
            for item in items:
                #  进入列表拿到每个商品的url
                product_url = item.find('div.detail > h3 > a').attr('href')
                #  加进集合中
                productUrls.append(product_url)
                get_details(product_url)
# 截取store后的那部分，截取出店铺id，然后拼接一个新的url:https://www.aliexpress.com/store/+店铺id+search/i.html
# https://www.aliexpress.com/store/all-wholesale-products/2160049.html?spm=a2g1y.12024536.pcShopHead_7975255.1        这是商家第1页展示商品
# https://www.aliexpress.com/store/2160049/search/2.html?spm=2114.12010615.8148361.1.2a0728cbH5rLbG&origin=n&SortType=bestmatch_sort        这是商家第2页展示商品
# https://70mai.aliexpress.com/store/all-wholesale-products/4257014.html?spm=a2g1y.12024536.pcShopHead_6686460.1        改动之后的店址
# https://70mai.aliexpress.com/store/4257014?spm=2114.12010609.pcShopHead_6686460.0&spm=a2g1y.12024536.hotSpots_148342012.0         原版店址

    #  拿到商品列表
    else:
        items = doc('#list-container > li').items()
        for item in items:
            #  进入列表拿到每个商品的url
            product_url = item.find('div.detail > h3 > a').attr('href')
            #  加进集合中
            productUrls.append(product_url)
            get_details(product_url)





# 获取商品详情信息
def get_details(product_url):
    browser.get(product_url)
    time.sleep(2)
    page_source = browser.page_source
    doc = pq(page_source)
    product_id = productUrl[9:20]  # 此处随意写的，数字需要换
    title = doc.find('#j-product-detail-bd > div.store-detail-main > div > h1').text()
    order = doc.find('#j-order-num').text()
    comment_num = doc.find('#j-product-tabbed-pane > ul > li:nth-child(2) > a').text()
    grade = doc.find('#j-customer-reviews-trigger > span.percent-num').text()
    like = doc.find('#j-product-action-block > span.product-action-main > div').text()
    Price = doc.find('#j-sku-price').text()
    Discount_Price = doc.find('#j-sku-discount-price').text()
    sheet1.write(i, 0, product_id)
    sheet1.write(i, 1, title)
    sheet1.write(i, 2, order)
    sheet1.write(i, 3, comment_num)
    sheet1.write(i, 4, grade)
    sheet1.write(i, 5, like)
    sheet1.write(i, 6, Price)
    sheet1.write(i, 7, Discount_Price)






