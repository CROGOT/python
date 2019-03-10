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
	# page = requests.get(url)
	# page.encoding = 'utf-8'
	f=open('kinopoisk_main.html')
	text = f.read()
	f.close()
	soup = BeautifulSoup(text,'lxml')
	table_info = soup.find('table',class_='info').findAll("tr")
	# print(table_info)
	# print(table_info[0].contents[1].text)
	god=re.sub('\n', '',table_info[0].contents[3].text)
	print("Год: "+god)

	# print(table_info[1].contents[1].text)
	strana=re.sub('\n', '',table_info[1].contents[3].text)
	print("Страна: "+strana)

	# print(table_info[2].contents[0].text)
	slogan=re.sub('\n', '',table_info[2].contents[1].text)
	print("Слоган: "+slogan)


	# print(table_info[3].contents)
	regiser="Режиссёр:"
	for regisers in table_info[3].contents[1].findAll('a'):
		regiser+=' '+regisers.text+','
	regiser=regiser[:-1]
	print(regiser)

	vozrast=str(table_info[14].contents[3].contents[1])[24:26]
	print("Возраст: "+vozrast+" +")


	aktery = soup.findAll('li',{'itemprop':'actors'})
	# print(aktery)
	akters="Актёры:"
	for akter in aktery:
		akters+=" "+akter.contents[0].text+","
	akters=akters[:-1]
	print(akters)


	td=soup.find('tr',text = re.compile('год')).parent
	print(td)

	# print(table_info[3].contents[1].findAll('a'))

	# print(table_info[3].contents[1].text)[24:26][24:26]
	# print(table_info[3].contents[3].text)		
	# for info in table_info:
	# 	print(info.contents[0])
	



if __name__ == "__main__":
	# kinopoisk_save_pic('https://www.kinopoisk.ru/film/843859/stills/','')
	# save_htm_into_file('https://www.kinopoisk.ru/film/843859/','kinopoisk_main.html')
	kinopoisk_save_info_film('https://www.kinopoisk.ru/film/843859/','')