# f = open( 'emails.txt', 'w' )
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import pprint
import var_dump
import re
# page=requests.get("https://www.avito.ru/vologodskaya_oblast?q=java")
f = open('avito.html', 'r', encoding='utf-8')
page=f.read()
f.close()
# soup = BeautifulSoup(page, 'html.parser')
soup = BeautifulSoup(page, 'lxml')
# print (soup)
items=soup.findAll("div",class_="item")
urls_tags = soup.findAll(class_="item-description-title-link")
# print(items)
for item in items:
	name = item.find("span",attrs={"itemprop":"name"}).getText()
	images = item.findAll("div",class_="item-slider-image")
	# print(images)
	url_img=''
	for img in images:
		# img_link=img.find('img').attrs['src']
		url_img+='https:'+img.find("img").attrs['src']+';'
		# print (img_link)
	price = item.find("span",class_="price").attrs['content']
	print(name+';'+price+';'+url_img)