from selenium import webdriver
import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.totalad

db.tvcfk.drop()
db.tvcfg.drop()

driver = webdriver.Chrome('/Users/developer/Downloads/chromedriver')
driver.implicitly_wait(5)
driver.get('https://tvcf.co.kr/MovieK/List.asp')

before_day = 2
today = datetime.datetime.now()
day_before_3 = today - datetime.timedelta(days=before_day)

driver.find_element_by_name('Date1').send_keys(day_before_3.strftime("%Y-%m-%d"))
driver.find_element_by_name('Date2').send_keys(today.strftime("%Y-%m-%d"))
driver.find_element_by_css_selector('#date_select > a').click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
lis = soup.select('#creative_list2 > li')
pages = soup.select_one('#pageNavi > ul > li:nth-child(1)').text.split('/')[1].strip()


def read_tvcf():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.select('#creative_list2 > li')

    for li in lis:
        title = li.select_one('label.title').text
        date = li.select_one('label.date').text
        type = li.select_one('label.flag > img')['alt']
        url = li.select_one('div.thumWrapfix > a')['href']
        img_url = li.select_one('div.thumWrapfix > a > div.cut')['data-src']
        tvcf_k = {
            'title': title,
            'date': date,
            'type': type,
            'url': url,
            'img_url': img_url
        }
        db.tvcfk.insert_one(tvcf_k)

def read_tvcfE():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.select('#creative_list > li')

    for li in lis:
        title = li.select_one('label.title').text.strip()
        date = li.select_one('label.date').text.strip()
        type = 'Global'
        url = li.select_one('div.thumWrapfix > a')['href']
        img_url = li.select_one('div.thumWrapfix > a > img')['src']
        tvcf_g = {
            'title': title,
            'date': date,
            'type': type,
            'url': url,
            'img_url': img_url
        }
        db.tvcfe.insert_one(tvcf_g)


if int(pages) == 1:
    read_tvcf()
else:
    for i in range(1, int(pages) + 1):
        read_tvcf()
        if i != int(pages):
            page_num = i + 3
            if i != 1:
                page_num += 1
            driver.find_element_by_css_selector('#pageNavi > ul > li:nth-child({}) > a'.format(page_num)).click()

driver.get('https://tvcf.co.kr/MovieE/List.asp')
driver.find_element_by_name('Date1').send_keys(day_before_3.strftime("%Y-%m-%d"))
driver.find_element_by_name('Date2').send_keys(today.strftime("%Y-%m-%d"))
driver.find_element_by_css_selector('#date_select > a').click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

lis = soup.select('#creative_list > li')
pages = soup.select_one('#pageNavi > ul > li:nth-child(1)').text.split('/')[1].strip()

if int(pages) == 1:
    read_tvcfE()
else:
    for i in range(1, int(pages) + 1):
        read_tvcfE()
        if i != int(pages):
            page_num = i + 3
            if i != 1:
                page_num += 1
            driver.find_element_by_css_selector('#pageNavi > ul > li:nth-child({}) > a'.format(page_num)).click()




driver.quit()

