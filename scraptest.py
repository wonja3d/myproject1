from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

client = MongoClient('localhost', 27017)
db = client.totalad

url = 'https://play.tvcf.co.kr/798307'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
print(soup)

image = soup.select_one('meta[property="og:image"]')
title = soup.select_one(
    'body > div > div.player-area > div > div.controlbox > div > div.left > div.row1 > div:nth-child(1)')
date = soup.select_one(
    'body > div > div.player-area > div > div.controlbox > div > div.left > div.row1 > div:nth-child(3)')

print(image)
print(title)
print(date)

# article = {'title': title, 'image': image, 'date': date}
# print(article)
# db.articles.insert_one(article)
