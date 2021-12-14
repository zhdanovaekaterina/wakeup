import pandas as pd
import numpy as np
import re

from pandas.core.frame import DataFrame

# Задание списка полей для импорта
fieldsToImportLeads = ['ID', 'Статус', 'Название лида', 'Имя', 'Отчество', 'Фамилия', 'Дата создания', 'Рабочий телефон', 'Мобильный телефон', 'Другой телефон', 'Рабочий e-mail', 'Частный e-mail', 'Другой e-mail', 'Сумма', 'UTM Source', 'UTM Medium', 'UTM Campaign', 'Направление', 'UF_CRM_PRODUCT']
fieldsToImportDeals = ['ID', 'Направление', 'Стадия сделки', 'Название сделки', 'Сумма', 'Контакт', 'Дата создания', 'UTM Source', 'UTM Medium', 'UTM Campaign', 'Курс WakeUp', 'Телефон клиента (ОСУ)', 'Почта клиента (ОСУ)', 'Контакт: Рабочий телефон', 'Контакт: Мобильный телефон', 'Контакт: Другой телефон', 'Контакт: Рабочий e-mail', 'Контакт: Частный e-mail', 'Контакт: Другой e-mail']

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
dl = dl[(dl['Направление'].str.contains('WakeUp')) | (dl['Направление'].str.contains('Обучение WakeUp'))]

# Проверка данных сделок и лидов на наличие телефонов и e-mail. Оставляет только те записи, по которым есть телефон или e-mail. Остальные - выгружает в файл excel в текущем каталоге
(ld[((ld['Рабочий телефон'].isna()) & (ld['Мобильный телефон'].isna()) & (ld['Другой телефон'].isna()) & (ld['Рабочий e-mail'].isna()) & (ld['Частный e-mail'].isna()) & (ld['Другой e-mail'].isna()))]).to_excel('leads_without_contact.xlsx')
(dl[((dl['Телефон клиента (ОСУ)'].isna()) & (dl['Почта клиента (ОСУ)'].isna()) & (dl['Контакт: Рабочий телефон'].isna()) & (dl['Контакт: Мобильный телефон'].isna()) & (dl['Контакт: Другой телефон'].isna()) & (dl['Контакт: Рабочий e-mail'].isna()) & (dl['Контакт: Частный e-mail'].isna()) & (dl['Контакт: Другой e-mail'].isna()))]).to_excel('deals_without_contact.xlsx')

ld = ld[~((ld['Рабочий телефон'].isna()) & (ld['Мобильный телефон'].isna()) & (ld['Другой телефон'].isna()) & (ld['Рабочий e-mail'].isna()) & (ld['Частный e-mail'].isna()) & (ld['Другой e-mail'].isna()))]
dl = dl[~((dl['Телефон клиента (ОСУ)'].isna()) & (dl['Почта клиента (ОСУ)'].isna()) & (dl['Контакт: Рабочий телефон'].isna()) & (dl['Контакт: Мобильный телефон'].isna()) & (dl['Контакт: Другой телефон'].isna()) & (dl['Контакт: Рабочий e-mail'].isna()) & (dl['Контакт: Частный e-mail'].isna()) & (dl['Контакт: Другой e-mail'].isna()))]

# Выгрузка столбцов, содержащих имя, в списки
clientName = ld['Имя'].tolist()
clientSecondName = ld['Отчество'].tolist()
clientSurname = ld['Фамилия'].tolist()

# Явное преобразование типов элементов в списке в строку

def typeChange(listOfElements:list):
    '''Принимает в качестве аргумента список и преобразует каждый его элемент в строку. Возвращает список строк.'''
    for i in range(0, len(listOfElements)):
        listOfElements[i] = str(listOfElements[i])

typeChange(clientName)
typeChange(clientSecondName)
typeChange(clientSurname)
listOfNames = [clientName, clientSecondName, clientSurname]
clientContact = []

# Объединение значений в строках в одно, без проверки на дубли

def mergeByElements(listOfLists:list, goalList:list, delimiterList=' '):
    '''Принимает список списков, которые нужно объединить поэлементно и объединяет их в целевой список с помощью заданного символа объединения.
        Проверяет входные списки на одинаковую длину.
        Не объединяет значения 'nan'.
    '''
    flag = False
    if goalList != []:
        return 'Ошибка: в целевом списке содержатся данные'
    lenthInner = len(listOfLists[0]) #длина внутреннего списка
    for i in range(1, len(listOfLists)):
        if len(listOfLists[i]) != lenthInner:
            flag = True
    if flag:
        return 'Ошибка: переданные списки разной длины'
    for k in range(0, lenthInner):
        temp = []
        for n in range(0, len(listOfLists)):
            if listOfLists[n][k] != 'nan':
                temp.append(listOfLists[n][k])
        goalList.append(delimiterList.join(temp))

mergeByElements(listOfNames, clientContact)
ld['Контакт'] = clientContact #добавление колонки в дата фрейм
ld = ld.drop('Имя', 1) #удаление лишних колонок
ld = ld.drop('Отчество', 1)
ld = ld.drop('Фамилия', 1)

# Выгрузка столбцов, содержащих телефон, в списки
workTel = ld['Рабочий телефон'].tolist()
mobTel = ld['Мобильный телефон'].tolist()
otherTel = ld['Другой телефон'].tolist()
workEmail = ld['Рабочий e-mail'].tolist()
privateEmail = ld['Частный e-mail'].tolist()
otherEmail = ld['Другой e-mail'].tolist()
listOfRawTelephones = [otherTel, workTel, mobTel, otherEmail, workEmail, privateEmail]

workTelDl = dl['Контакт: Рабочий телефон'].tolist()
mobTelDl = dl['Контакт: Мобильный телефон'].tolist()
otherTelDl = dl['Контакт: Другой телефон'].tolist()
osuTelDl = dl['Телефон клиента (ОСУ)'].tolist()
workEmailDl = dl['Контакт: Рабочий e-mail'].tolist()
privateEmailDl = dl['Контакт: Частный e-mail'].tolist()
otherEmailDl = dl['Контакт: Другой e-mail'].tolist()
osuEmailDl = dl['Почта клиента (ОСУ)'].tolist()
listOfRawTelephonesDl = [otherTelDl, osuTelDl, workTelDl, mobTelDl, otherEmailDl, osuEmailDl, workEmailDl, privateEmailDl]

# Явное преобразование всех номеров телефонов в строки
for telItem in listOfRawTelephones:
    typeChange(telItem)

for telItem in listOfRawTelephonesDl:
    typeChange(telItem)

def deleteNans(rawList:list):
    for i in range(len(rawList)):
        if rawList[i] == 'nan':
            rawList[i] = ''
    return rawList

# Приведение номеров телефонов к единому формату и запись в общий список телефонов и почт (важна запись в порядке перебора списков при записи id по номеру)
newWorkTel = [''.join(filter(str.isdigit, tel)) for tel in workTel]
newMobTel = [''.join(filter(str.isdigit, tel)) for tel in mobTel]
newOtherTel = [''.join(filter(str.isdigit, tel)) for tel in otherTel]
newotherEmail = deleteNans(otherEmail)
newworkEmail = deleteNans(workEmail)
newprivateEmail = deleteNans(privateEmail)
listOfTelephones = [newOtherTel, newWorkTel, newMobTel, newotherEmail, newworkEmail, newprivateEmail]

newWorkTelDL = [''.join(filter(str.isdigit, tel)) for tel in workTelDl]
newMobTelDl = [''.join(filter(str.isdigit, tel)) for tel in mobTelDl]
newOtherTelDl = [''.join(filter(str.isdigit, tel)) for tel in otherTelDl]
newOsuTelDl = [''.join(filter(str.isdigit, tel)) for tel in osuTelDl]
newotherEmailDl = deleteNans(otherEmailDl)
newosuEmailDl = deleteNans(osuEmailDl)
newworkEmailDl = deleteNans(workEmailDl)
newprivateEmailDl = deleteNans(privateEmailDl)
listOfTelephonesDl = [newOtherTelDl, newWorkTelDL, newMobTelDl, newOsuTelDl, newotherEmailDl, newosuEmailDl, newworkEmailDl, newprivateEmailDl]

keyTelLd = []
keyTelDl = []

def mergeTelephones(listOfLists:list, goalList:list):
    '''Принимает список списков телефонов, из которых необходимо оставить ключевой номер.
        Проверяет входные списки на одинаковую длину.
        Возвращает список номеров телефонов, собранный из всех списков.
        Важно передавать списки в порядке приоритета.
    '''
    flag = False
    if goalList != []:
        return 'Ошибка: в целевом списке содержатся данные'
    lenthInner = len(listOfLists[0]) #длина внутреннего списка
    for i in range(1, len(listOfLists)):
        if len(listOfLists[i]) != lenthInner:
            flag = True
    if flag:
        return 'Ошибка: переданные списки разной длины'
    for k in range(0, lenthInner):
        temp = []
        for n in range(0, len(listOfLists)):
            if len(temp) == 1:
                break
            if listOfLists[n][k] != '':
                temp.append(listOfLists[n][k])
        goalList.append(*temp)

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

def mergeLines(keyDataFrame, keyColumn:str, listOfColumns:list):
    '''Принимает исходный дата фрейм, ключевой столбец, по которому будут объединяться данные, и список столбцов, которые необходимо объединить.
        Возвращает объединенный датафрейм.
    '''
    tempLists = []
    for i in listOfColumns:
        tempList1 = pd.Series(keyDataFrame.groupby([keyColumn])[i].apply(list))
        tempLists.append(tempList1)
    resultDataFrame = pd.DataFrame(tempLists)
    resultDataFrame = resultDataFrame.transpose()
    return resultDataFrame

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

