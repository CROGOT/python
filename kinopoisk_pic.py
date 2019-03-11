from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import pprint
import var_dump
import re

def kinopoisk_save_pics(url_pics,folder):
	page = requests.get(url_pics)
	# f = open('Kinopoisk.html', 'r')
	# page=f.read()
	# f.close()
	# soup = BeautifulSoup(page, 'html.parser')
	soup = BeautifulSoup(page.text, 'lxml')
	table_img=soup.find("table",class_="js-rum-hero").findAll("img")
	for img in table_img:
		link=re.sub('sm_','',img.attrs['src'])
		print (link)
		filename = link.split("/")[-1]
		print (folder+filename)
		p = requests.get(link)
		out = open(folder+filename, "wb")
		out.write(p.content)
		out.close()


kinopoisk_save_pics('https://www.kinopoisk.ru/film/1041723/stills','C:\\Users\\Егор\\Desktop\\foto\\')