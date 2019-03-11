from bs4 import BeautifulSoup
import requests
import re
import os

SITE_URL="https://www.kinopoisk.ru/film/706655/"
PICS_URL=SITE_URL+"stills/"
CATALOG="C:\\Users\\Егор\\Desktop\\foto\\"
FILE_NAME="Капитан_Марвел.html"
STEP=1 # 1-спарсить сайт в файл, 2 - спарсить инфу по фильму, 3 - сохранить картинки в каталог

film={}

def save_htm_into_file(url='',name_catalog='',filename=''):
	if STEP != 1: return false
	page = requests.get(url,'windows-1251')
	soup = BeautifulSoup(page.text,'lxml')
	prefix=re.sub(':', '',soup.title.text)
	if name_catalog=='': name_catalog=os.getcwd()+"\\"+prefix
	else: name_catalog+="\\"+prefix
	if filename=='': filename=prefix+'.html'
	if (filename=='') and (name_catalog==PICS_URL): filename=prefix+'_pics.html'
	# print(name_catalog)

	try:
		os.mkdir(name_catalog)
	except OSError: 
		print ("Создать директорию %s не удалось" % name_catalog)
	else: 
		print ("Успешно создана директория %s " % name_catalog)
	
	path=name_catalog+'\\'+filename

	try:
		f=open(path,'w')
	except OSError:
		print ("Создать файл %s не удалось" % path)
	else:
		print ("Успешно создан файл %s " % path)
	f.write(page.text)
	f.close()

def kinopoisk_save_pic(url,destination):
	if STEP != 3: return false
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
	if STEP != 2: return false
	# page = requests.get(url)
	# page.encoding = 'utf-8'
	f=open('kinopoisk_main.html')
	text = f.read()
	f.close()
	soup = BeautifulSoup(text,'lxml')
	film['имя']=soup.find('h1',{'class':'moviename-big'}).text
	table_info = soup.find('table',class_='info')
	# print(table_info)
	# print(table_info[0].contents[1].text)
	# god=re.sub('\n', '',table_info[0].contents[3].text)
	film['год']=table_info.find('td',text = re.compile('год')).findNext('td').a.text
	# print("Год: "+film['год'])

	# print(table_info[1].contents[1].text)
	# strana=re.sub('\n', '',table_info[1].contents[3].text)
	film['страна']=table_info.find('td',text = re.compile('страна')).findNext('td').a.text
	# print("Страна: "+film['страна'])

	# print(table_info[2].contents[0].text)
	# slogan=re.sub('\n', '',table_info[2].contents[1].text)
	film['слоган']=table_info.find('td',text = re.compile('слоган')).findNext('td').text
	# print("Слоган: "+film['слоган'])

	# print(table_info[3].contents)
	film['режиссер']=[]
	for regiser in table_info.find('td',text = re.compile('режиссер')).findNext('td').findAll('a'):
		film['режиссер'].append(regiser.text)
	# film['режиссер']=film['режиссер'][:-1]
	# print("Режиссёр:" + film['режиссер'])

	film['возраст']=re.sub('"', '',str(table_info.find('td',text = re.compile('возраст')).findNext('td').contents[1])[24:26])
	# print("Возраст: "+film['возраст']+" +")


	aktery = soup.findAll('li',{'itemprop':'actors'})
	film['актер']=[]
	for akter in aktery:
		film['актер'].append(akter.contents[0].text)
	# print("Актёры: "+film['актер'])
	film['preview_url']=soup.find('a',{'class':'popupBigImage'}).img.get('src')

	print(film)
	print(soup.title.text)
	path = os.getcwd()
	print ("Текущая рабочая директория %s" % path)
	# print(soup.find('a',{'class':'popupBigImage'}).img.get('src'))
	# td=soup.find('td',text = re.compile('год')).next.next.next.a.text
	# print(table_info[3].contents[1].findAll('a'))
	# print(table_info[3].contents[1].text)[24:26][24:26]
	# print(table_info[3].contents[3].text)		
	# for info in table_info:
	# print(info.contents[0])
	


if __name__ == "__main__":
	save_htm_into_file(SITE_URL,CATALOG)
	save_htm_into_file(PICS_URL,CATALOG)	
	# kinopoisk_save_pic('https://www.kinopoisk.ru/film/843859/stills/',CATALOG)
	# kinopoisk_save_info_film(SITE_URL,'')