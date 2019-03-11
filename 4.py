import requests
from bs4 import BeautifulSoup
# Collect and parse first page
page = requests.get('https://www.kinopoisk.ru/film/1114960/stills/')
soup = BeautifulSoup(page.text, 'html.parser')
# Pull all text from the BodyText div
print (soup)
# Pull text from all instances of <a> tag within BodyText div
artist_name_list_items = artist_name_list.find_all('a')