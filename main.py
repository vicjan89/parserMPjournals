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
		if row[1].date() == datetime.date(2023,1,15):
			journal.append(row)

parse_MR(r'W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Стасево 16.01.23\ МВ10 Т1\МР741_Журнал_аварий.xml', journal, 'Ввод 10кВ Т-1', datetime.timedelta(minutes=3, seconds=25, milliseconds=880))
parse_MR(r'W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Стасево 16.01.23\ МВ10 Т1\МР741_ЖурналСистемы.xml', journal, 'Ввод 10кВ Т-1', datetime.timedelta(minutes=3, seconds=25, milliseconds=880))
parse_MR(r'W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Стасево 16.01.23\МВ10 ф195\Журнал аварий МР5 версия 50.03.xml', journal, 'ВЛ-195', datetime.timedelta())
parse_MR(r'W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Стасево 16.01.23\МВ10 ф195\МР5 v50 Журнал Системы.xml', journal, 'ВЛ-195', datetime.timedelta())
parse_MR(r'W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Стасево 16.01.23\ТН10 Стасево\Журнал аварий МР5 v60.xml', journal, 'ТН-10', datetime.timedelta(seconds=26, milliseconds=470))
parse_MR(r'W:\RZAI\Информация по отказам и анализ работы СРЗАИ\Стасево 16.01.23\ТН10 Стасево\МР5 v60 Журнал Системы.xml', journal, 'ТН-10', datetime.timedelta(seconds=26, milliseconds=470))
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
