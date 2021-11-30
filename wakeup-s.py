import pandas as pd
import numpy as np
import re

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

def mergeByElements(listOfLists:list, goalList:list, delimiterList:str):
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

mergeByElements(listOfNames, clientContact, ' ')
ld['Контакт'] = clientContact #добавление колонки в дата фрейм

# Выгрузка столбцов, содержащих телефон, в списки
workTel = ld['Рабочий телефон'].tolist()
mobTel = ld['Мобильный телефон'].tolist()
otherTel = ld['Другой телефон'].tolist()

# Приведение номера телефона к одному виду
