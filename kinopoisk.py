from bs4 import BeautifulSoup
import requests

def kinopoisk_save_pic(url,destination):
	page = requests.get(url,'utf-8')
	# f=open('kinopoisk.html')
	# text = f.read()
	# f.close()
	soup = BeautifulSoup(page.text,'lxml')
	table_pic = soup.find('table',{'class':'js-rum-hero fotos'}).findAll('img')
	for img in table_pic:
		url_pic=img.get('src')
		# links=li.findAll('li')
		print(url_pic)








if __name__ == "__main__":
	kinopoisk_save_pic('https://www.kinopoisk.ru/film/843859/stills/','')