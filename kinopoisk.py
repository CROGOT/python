from bs4 import BeautifulSoup
import requests
import re
import os
import configparser
from datetime import datetime

#######################################################

SITE_URL="https://www.kinopoisk.ru/film/279095/"

CATALOG="C:\\Users\\Егор\\Desktop\\foto\\"

# STEP=[1,2,3,4] 
STEP=[2,3]
	   # 1 - спарсить сайт в файлы, 
	   # 2 - спарсить инфу по фильму, 
	   # 3 - парс урл картинок,
	   # 4 - сохранить картинки в каталог

#######################################################

config = configparser.ConfigParser()
inf = configparser.ConfigParser()
INFO='INFO'
SETTING='SETTING'
PICS='PICS'
FILEINI='example.ini'
INFOINI='info.ini'
PICS_URL=SITE_URL+"stills/"
# FILE_NAME="КиноПоиск.html"
film = {}

def init():
		config.read(FILEINI)
		if config.sections()==[]:
			print ("Прочитать настройки из %s не удалось" % FILEINI)
			config[SETTING]={}
			config[PICS]={}
			config[INFO]={}
			config[SETTING]['site_url']=SITE_URL
			config[SETTING]['pics_url']=PICS_URL
			config[SETTING]['step']=str(STEP)
		else: 
			print ("Настройки из %s прочитаны" % FILEINI)
			path=config[SETTING]['name_catalog']+'\\'+INFOINI
			inf.read(path)

def save_htm_into_file(page,name_catalog='',filename=''):
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

def save_main_html():
	if (1 not in STEP): return False
	page = requests.get(SITE_URL,'windows-1251')
	soup = BeautifulSoup(page.text,'lxml')
	prefix=re.sub(':', '',soup.title.text)
	name_catalog = CATALOG+prefix
	filename=prefix+'.html'
	config[SETTING]['name_catalog']=name_catalog
	config[SETTING]['filename']=filename
	write_ini()
	save_htm_into_file(page,name_catalog,filename)

def save_pics_html():
	if (1 not in STEP): return False
	page = requests.get(PICS_URL,'windows-1251')
	soup = BeautifulSoup(page.text,'lxml')
	prefix=re.sub(':', '',soup.title.text)
	filename=prefix+'.html'
	name_catalog = config[SETTING]['name_catalog']
	config[SETTING]['filenamepis']=filename
	save_htm_into_file(page,name_catalog,filename)

def clr_text(text):
	specsimbols={' ':'&nbsp;','-':chr(0x97), '...':chr(0x85)}
	for key in specsimbols:
		# print(key)
		# print(specsimbols[key])
		text=re.sub(specsimbols[key], key,text)
	return text
def showsymbols():
	print("…–—·{«^»}{‹^›}{„^“}{‘^’}́…•¶§|±≈≠≥≤×∙÷√∆∞|′″¹²³ⁿ●°µ‰Ω|½¼¾|€¢¥|©®™")
	
def kinopoisk_save_info_film():
	if (2 not in STEP): return False
	# page = requests.get(url)
	# page.encoding = 'utf-8'
	path=config[SETTING]['name_catalog']+'\\'+config[SETTING]['filename']
	f=open(path)
	text = f.read()
	f.close()
	soup = BeautifulSoup(text,'lxml')
	film['имя']=soup.find('h1',{'class':'moviename-big'}).text
	film['описание']=clr_text(soup.find('div',{'class':'film-synopsys'}).text)
	# film['описание']=re.sub(chr(0x97), '-',film['описание'])
	table_info = soup.find('table',class_='info')

	film['год']=table_info.find('td',text = re.compile('год')).findNext('td').a.text

	aktery = soup.find('div',{'id':'actorList'}).ul
	film['актер']=[]
	for akter in aktery.findAll('li'):
		film['актер'].append(akter.contents[0].text)
	film['актер'].pop(-1)

	try: film['бюджет']=table_info.find('td',text = re.compile('бюджет')).findNext('td').a.text
	except AttributeError:
		try: film['бюджет']=table_info.find('td',text = re.compile('бюджет')).findNext('td').div.text.replace("\n", "").replace(" ", "")
		except AttributeError: film['бюджет']='-'

	film['возраст']=re.sub('"', '',str(table_info.find('td',text = re.compile('возраст')).findNext('td').contents[1])[24:26])

	try: film['дата']=soup.find('td',{'id':'div_rus_prem_td2'}).find('div',{'class':'prem_ical'}).get('data-ical-date')
	except AttributeError: film['дата']='-'
	else: film['дата']=format_date(film['дата'])

	film['время']=table_info.find('td',text = re.compile('время')).findNext('td').text

	film['режиссер']=[]
	for regiser in table_info.find('td',text = re.compile('режиссер')).findNext('td').findAll('a'):
		film['режиссер'].append(regiser.text)

	film['слоган']=table_info.find('td',text = re.compile('слоган')).findNext('td').text

	film['страна']=[]
	for strana in table_info.find('td',text = re.compile('страна')).findNext('td').findAll('a'):
		film['страна'].append(strana.text)
	# film['страна']=table_info.find('td',text = re.compile('страна')).findNext('td').a.text

	film['preview_url']=soup.find('a',{'class':'popupBigImage'}).img.get('src')

	config[INFO]={}
	for item in film:
		if type(film[item])==list:
			config[INFO][item]=','.join(film[item])
		else:
			config[INFO][item]=str(film[item])
	for key in config['INFO']:
		print(key+': '+config['INFO'][key])
	inf[INFO]=config[INFO]
	# path = os.getcwd()
	# print ("Текущая рабочая директория %s" % path)
	# print(info.contents[0])

def write_ini():
	with open(FILEINI, 'w') as configfile:
		config.write(configfile)
def write_info_ini():
	path=config[SETTING]['name_catalog']+'\\'+INFOINI
	with open(path, 'w') as infofile:
		inf.write(infofile)

def get_ini(key):
	config.read(FILEINI)
	return config[SETTING][key]

def format_date(date_str):
	RU_MONTH_VALUES = {'января': 1,'февраля': 2,'марта': 3,'апреля': 4,'мая': 5,'июня': 6,'июля': 7,'августа': 8,'сентября': 9,'октября': 10,'ноября': 10,'декабря': 12,}
	for k, v in RU_MONTH_VALUES.items():
		date_str = date_str.replace(k, str(v))
	d = datetime.strptime(date_str+', 00:00', '%d %m %Y, %H:%M')
	strg = f'{d:%d.%m.%Y}'
	return strg

def kinopoisk_save_urlpic():
	if (3 not in STEP): return False
	# page = requests.get(url,'utf-8')
	path=config[SETTING]['name_catalog']+'\\'+config[SETTING]['filenamepis']
	f=open(path)
	text = f.read()
	f.close()
	soup = BeautifulSoup(text,'lxml')
	table_pic = soup.find('table',{'class':'js-rum-hero fotos'}).findAll('img')
	config[PICS]={}
	config[PICS]['preview_url'+'.jpg']=config['INFO']['preview_url']
	for img in table_pic:
		url_pic=re.sub('sm_', '', img.get('src'))
		img_name = url_pic.split('/')[-1]
		config[PICS][img_name]=url_pic
		print(img_name)
	inf[PICS]=config[PICS]

def kinopoisk_save_pics():
	if (4 not in STEP): return False
	for key in config[PICS]:
		path=config[SETTING]['name_catalog']+'\\'+key
		# print(key,config[PICS][key] )
		p = requests.get(config[PICS][key])
		out = open(path, "wb")
		out.write(p.content)
		out.close()
		print(path)

if __name__ == "__main__":
	init()
	save_main_html()
	save_pics_html()
	kinopoisk_save_info_film()
	kinopoisk_save_urlpic()
	kinopoisk_save_pics()
	write_ini()
	write_info_ini()
	# showsymbols()
