from bs4 import BeautifulSoup
import requests
import re

def save_htm_into_file(url,filename):
	page = requests.get(url,'windows-1251')
	f=open(filename,'w')
	f.write(page.text)
	f.close()
	print('ok')

def kinopoisk_save_pic(url,destination):
	# page = requests.get(url,'utf-8')
	f=open('kinopoisk.html')
	text = f.read()
	f.close()
	soup = BeautifulSoup(text,'lxml')
	table_pic = soup.find('table',{'class':'js-rum-hero fotos'}).findAll('img')
	for img in table_pic:
		url_pic=re.sub('sm_', '', img.get('src'))
		img_name = url_pic.split('/')[-1]
		print(img_name)

def kinopoisk_save_info_film(url,destination):
	f=open('kinopoisk_main.html')
	text = f.read()
	f.close()
	soup = BeautifulSoup(text,'lxml')
	# print(soup.title)
	table_info = soup.find('table',{'class':'info'}).findAll('tr')
	print(table_info[0].contents[1].text)
	print(table_info[0].contents[3].text)

	print(table_info[1].contents[1].text)
	print(table_info[1].contents[3].text)

	print(table_info[2].contents[0].text)
	print(table_info[2].contents[1].text)


	print(table_info[3].contents)


	print(table_info[3].contents[0].text)
	print(table_info[3].contents[1].contents[0].text)

	# print(table_info[3].contents[1].text)
	# print(table_info[3].contents[3].text)		
	# for info in table_info:
	# 	print(info.contents[0])
	



if __name__ == "__main__":
	# kinopoisk_save_pic('https://www.kinopoisk.ru/film/843859/stills/','')
	# save_htm_into_file('https://www.kinopoisk.ru/film/843859/','kinopoisk_main.html')
	kinopoisk_save_info_film('https://www.kinopoisk.ru/film/843859/','')