import pandas as pd
import numpy as np

def typeChange(listOfElements:list):
    '''Принимает в качестве аргумента список и преобразует каждый его элемент в строку. Возвращает список строк.'''
    for i in range(0, len(listOfElements)):
        listOfElements[i] = str(listOfElements[i])


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


def deleteNans(rawList:list):
    for i in range(len(rawList)):
        if rawList[i] == 'nan':
            rawList[i] = ''
    return rawList


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


