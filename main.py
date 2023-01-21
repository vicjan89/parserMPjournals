import xml.etree.ElementTree as ET
import datetime
import re

journal = []
def parse_MR(path, journal, name_equipment, dtime):
	tree = ET.parse(path)
	root = tree.getroot()
	for child in root:
		row = [name_equipment]
		for i in child[1:]:
			if i.tag in ('Время', '_timeCol'):
				try:
					dt = datetime.datetime.strptime(i.text[:-3], '%d-%m-%y %H:%M:%S')
					dt += datetime.timedelta(milliseconds=int(i.text[-2:]+'0'))
				except ValueError:
					dt = datetime.datetime.strptime(i.text[:-3], '%d.%m.%y %H:%M:%S')
					dt += datetime.timedelta(milliseconds=int(i.text[-2:] + '0'))
				row.append(dt + dtime)
			else:
				if i.text:
					i.tag = re.sub(r'_x...._', ' ', i.tag).replace('_', '')
					row.append(i.tag+' '+i.text)
				else:
					row.append(' ')
		if row[1].date() == datetime.date(2023,1,21):
			journal.append(row)

parse_MR(r'W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\522\МР700_ЖурналСистемы.xml', journal, 'ВВ-522', datetime.timedelta(hours=-2, minutes=1, seconds=-3, milliseconds=0))
parse_MR(r'W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\527\Журнал аварий МР 700.xml', journal, 'ВВ-527', datetime.timedelta(minutes=-14, seconds=-9, milliseconds=0))
parse_MR(r'W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\527\МР700_ЖурналСистемы.xml', journal, 'ВВ-527', datetime.timedelta(minutes=-14, seconds=-9, milliseconds=0))
parse_MR(r'W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\573\Журнал аварий МР 700.xml', journal, 'ВВ-573', datetime.timedelta(seconds=2))
parse_MR(r'W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\573\МР700_ЖурналСистемы.xml', journal, 'ВВ-573', datetime.timedelta(seconds=2))
parse_MR(r"W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\577\Журнал аварий МР 700.xml", journal, 'ВВ-577', datetime.timedelta(seconds=1))
parse_MR(r"W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\577\МР700_ЖурналСистемы.xml", journal, 'ВВ-577', datetime.timedelta(seconds=1))
parse_MR(r"W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\вв 5с\МР700_ЖурналСистемы.xml", journal, 'Ввод 5с', datetime.timedelta(seconds=2))
parse_MR(r"W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\вв 6с\Журнал аварий МР 700.xml", journal, 'Ввод 6с', datetime.timedelta(seconds=2, milliseconds=-10))
parse_MR(r"W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\вв 6с\МР700_ЖурналСистемы.xml", journal, 'Ввод 6с', datetime.timedelta(seconds=2, milliseconds=-10))
parse_MR(r"W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\свв 5\МР700_ЖурналСистемы.xml", journal, 'СВВ 5с', datetime.timedelta(seconds=2, milliseconds=-360))
parse_MR(r"W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\свв 6\МР700_ЖурналСистемы.xml", journal, 'СВВ 6с', datetime.timedelta(seconds=2, milliseconds=180))
parse_MR(r"W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\тн 5с\МР600_ЖурналСистемы.xml", journal, 'ТН 5с', datetime.timedelta(seconds=3))
parse_MR(r"W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Технологическая\авария технол. 21.01\тн 6с\МР600_ЖурналСистемы.xml", journal, 'ТН 6с', datetime.timedelta(seconds=4))
journal.sort(key=lambda dt: dt[1])
table = '''<!DOCTYPE HTML>
<html>
 <head>
  <meta charset="utf-8">
  <title>События МР</title>
    <style>
   table { 
    width: 100%; /* Ширина таблицы */
    border: 4px double black; /* Рамка вокруг таблицы */
    border-collapse: collapse; /* Отображать только одинарные линии */
   }
   </style>
 </head>
 <body>
  <table border="1">
     <caption>События МР</caption>'''
for row in journal:
	table += '<tr>\n'
	for item in row:
		table += f'<td>{item}</td>'
	table += '</tr>\n'
table += '</table></body></html>'
with open('События совмещённые МР.html', 'w', encoding='utf-8') as file:
	file.write(table)
