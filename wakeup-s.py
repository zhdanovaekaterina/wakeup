from functions import typeChange, mergeByElements, deleteNans, mergeTelephones, mergeLines
import pandas as pd
import numpy as np
import re

from pandas.core.frame import DataFrame

# Задание списка полей для импорта
fieldsToImportLeads = ['ID', 'Статус', 'Название лида', 'Дата создания', 'Рабочий телефон', 'Мобильный телефон', 'Другой телефон', 'UTM Source', 'UTM Medium', 'UTM Campaign']
fieldsToImportDeals = ['ID', 'Направление', 'Стадия сделки', 'Название сделки', 'Сумма', 'Контакт', 'Дата создания', 'UTM Source', 'UTM Medium', 'UTM Campaign', 'Курс WakeUp', 'Телефон клиента (ОСУ)', 'Почта клиента (ОСУ)', 'Контакт: Рабочий телефон', 'Контакт: Мобильный телефон', 'Контакт: Другой телефон']

# Импорт данных
ld = pd.read_csv('LEAD.csv', delimiter=';')
dl = pd.read_csv('DEAL.csv', delimiter=';')
ld = ld[fieldsToImportLeads]
dl = dl[fieldsToImportDeals]

# Фильтрация лишних заявок в лидах
ld = ld[(~ld['Название лида'].str.contains('.*Instagram WakeUP')) & (~ld['Название лида'].str.contains('.*[Тт]ест.*')) & (~ld['Название лида'].str.contains('Mango.*')) & (~ld['Название лида'].str.contains('Манго.*')) & (~ld['Название лида'].str.contains('BIG NEWS.*')) & (~ld['Название лида'].str.contains('Дмитрий Ивашин')) & (~ld['Название лида'].str.contains('Илья')) & (~ld['Название лида'].str.contains('Лид #87868')) & (~ld['Название лида'].str.contains('ЛУЧШИЙ ТРЕНЕР ПО ПРОДАЖАМ.*')) & (~ld['Название лида'].str.contains('Стенд WakeUP.*')) & (~ld['Статус'].str.contains('Тестирование'))]

# Фильтрация лишних заявок в сделках
dl = dl[(~dl['Стадия сделки'].str.contains('[Тт]ест.*')) & (~dl['Название сделки'].str.contains('.*[Тт]ест.*'))]
dl = dl[(~dl['Название сделки'].str.contains('Заявка на демо-модуль'))]

# Проверка данных сделок и лидов на наличие телефонов и e-mail. Оставляет только те записи, по которым есть телефон или e-mail. Остальные - выгружает в файл excel в текущем каталоге
(ld[((ld['Рабочий телефон'].isna()) & (ld['Мобильный телефон'].isna()) & (ld['Другой телефон'].isna()))]).to_excel('leads_without_contact.xlsx')
(dl[((dl['Телефон клиента (ОСУ)'].isna()) & (dl['Почта клиента (ОСУ)'].isna()) & (dl['Контакт: Рабочий телефон'].isna()) & (dl['Контакт: Мобильный телефон'].isna()) & (dl['Контакт: Другой телефон'].isna()))]).to_excel('deals_without_contact.xlsx')

ld = ld[~((ld['Рабочий телефон'].isna()) & (ld['Мобильный телефон'].isna()) & (ld['Другой телефон'].isna()))]
dl = dl[~((dl['Телефон клиента (ОСУ)'].isna()) & (dl['Почта клиента (ОСУ)'].isna()) & (dl['Контакт: Рабочий телефон'].isna()) & (dl['Контакт: Мобильный телефон'].isna()) & (dl['Контакт: Другой телефон'].isna()))]

# Выгрузка столбцов, содержащих телефон, в списки
workTel = ld['Рабочий телефон'].tolist()
mobTel = ld['Мобильный телефон'].tolist()
otherTel = ld['Другой телефон'].tolist()
listOfRawTelephones = [otherTel, workTel, mobTel]

workTelDl = dl['Контакт: Рабочий телефон'].tolist()
mobTelDl = dl['Контакт: Мобильный телефон'].tolist()
otherTelDl = dl['Контакт: Другой телефон'].tolist()
osuTelDl = dl['Телефон клиента (ОСУ)'].tolist()
listOfRawTelephonesDl = [otherTelDl, osuTelDl, workTelDl, mobTelDl]

# Явное преобразование всех номеров телефонов в строки
for telItem in listOfRawTelephones:
    typeChange(telItem)

for telItem in listOfRawTelephonesDl:
    typeChange(telItem)

# Приведение номеров телефонов к единому формату и запись в общий список телефонов и почт (важна запись в порядке перебора списков при записи id по номеру)
newWorkTel = [''.join(filter(str.isdigit, tel)) for tel in workTel]
newMobTel = [''.join(filter(str.isdigit, tel)) for tel in mobTel]
newOtherTel = [''.join(filter(str.isdigit, tel)) for tel in otherTel]
listOfTelephones = [newOtherTel, newWorkTel, newMobTel]

newWorkTelDL = [''.join(filter(str.isdigit, tel)) for tel in workTelDl]
newMobTelDl = [''.join(filter(str.isdigit, tel)) for tel in mobTelDl]
newOtherTelDl = [''.join(filter(str.isdigit, tel)) for tel in otherTelDl]
newOsuTelDl = [''.join(filter(str.isdigit, tel)) for tel in osuTelDl]
listOfTelephonesDl = [newOtherTelDl, newWorkTelDL, newMobTelDl, newOsuTelDl]

keyTelLd = []
keyTelDl = []

mergeTelephones(listOfTelephones, keyTelLd)
mergeTelephones(listOfTelephonesDl, keyTelDl)

# Загрузка ключевого телефона в дата фреймы
# НЕТ ПРОВЕРКИ ОДИНАКОВОЙ ДЛИНЫ КЛЮЧЕВОГО СТОЛБЦА И ЦЕЛЕВОГО ДАТА ФРЕЙМА
ld['Ключевой телефон'] = keyTelLd
ld.loc[ld['Ключевой телефон'] == '', 'Ключевой телефон'] = np.NaN
dl['Ключевой телефон'] = keyTelDl
dl.loc[dl['Ключевой телефон'] == '', 'Ключевой телефон'] = np.NaN
ld.drop(['Рабочий телефон', 'Мобильный телефон', 'Другой телефон'], 1, inplace=True) #удаление лишних колонок
dl.drop(['Контакт: Рабочий телефон', 'Контакт: Мобильный телефон', 'Контакт: Другой телефон', 'Телефон клиента (ОСУ)'], 1, inplace=True)

# Соединение строк по ключевому телефону - для каждого столбца отдельно. Результат - новый df

keyColumn1 = ld.columns[len(ld.columns)-1]
listOfColumns1 = ld.columns
ldResult = mergeLines(ld, keyColumn1, listOfColumns1)
ldResult

keyColumn2 = dl.columns[len(dl.columns)-1]
listOfColumns2 = dl.columns
dlResult = mergeLines(dl, keyColumn2, listOfColumns2)
dlResult

# Объединение двух датафреймов по ключу. Выгрузка в excel
mergedData = ldResult.merge(dlResult, left_index = True, right_index = True, how='outer')
mergedData.to_excel('merdedData.xlsx')

