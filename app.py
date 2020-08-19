from flask import Flask, render_template, jsonify, request
from selenium import webdriver
import datetime
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/tvcf', methods=['GET'])
def read_tvcf():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('—disable - gpu')
    chrome_options.add_argument('lang = ko_KR')

    driver = webdriver.Chrome('/Users/developer/Downloads/chromedriver', chrome_options=chrome_options)
    driver.implicitly_wait(3)
    driver.get('https://tvcf.co.kr/MovieK/List.asp')

    before_day = 0
    today = datetime.datetime.now()
    day_before_3 = today - datetime.timedelta(days=before_day)

    driver.find_element_by_name('Date1').send_keys(day_before_3.strftime("%Y-%m-%d"))
    driver.find_element_by_name('Date2').send_keys(today.strftime("%Y-%m-%d"))
    driver.find_element_by_css_selector('#date_select > a').click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.select('#creative_list2 > li')


    tvcf_k_list = []


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
        tvcf_k_list.append(tvcf_k)

    driver.get('https://tvcf.co.kr/MovieE/List.asp')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.select('#creative_list > li')
    tvcf_g_list = []

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
        tvcf_g_list.append(tvcf_g)

    driver.quit()
    return jsonify({'result': 'success', 'tvcf_korea_infos': tvcf_k_list, 'tvcf_global_infos' : tvcf_g_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
