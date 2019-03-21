from datetime import datetime




def int_value_from_ru_month(date_str):
	RU_MONTH_VALUES = {'января': 1,'февраля': 2,'марта': 3,'апреля': 4,'мая': 5,'июня': 6,'июля': 7,'августа': 8,'сентября': 9,'октября': 10,'ноября': 10,'декабря': 12,}
	for k, v in RU_MONTH_VALUES.items():
		date_str = date_str.replace(k, str(v))
	d = datetime.strptime(date_str, '%d %m %Y, %H:%M')
	strg = f'{d:%d.%m.%Y}'
	return strg

date_str = '28 марта 2019'
date_str = int_value_from_ru_month(date_str+', 00:00')
print (date_str)
