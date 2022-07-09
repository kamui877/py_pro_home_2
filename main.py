from pprint import pprint
import csv
import re


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def sort_list(list_to_sort):
    list_1 = list()
    list_2 = list()
    result = list()
    list_d = list()
    for list_ in list_to_sort:
        #Делит список на 2, в первом ФИО, во втором все остальное
        if list_[1] == '' or list_[2] == '':
            var = [list_[0], list_[1], list_[2]]
            list_1.append(', '.join(var).replace(',', '').split())
        else:
            list_1.append(list_[0: 3])
        list_2.append([list_[3], list_[4], list_[5], list_[6]])
    for el in list_1:
        #Добавляет пустой элемент в список, если ФИО не полное, чтобы во всех списках было равное кол-во значений
        if len(el) < 3:
            el.append('')
    for el in range(9):
        #Объединяет два списка в один
        list_1[el].append(', '.join(list_2[el]))
        result.append(', '.join(list_1[el]).split(', '))
    for el in result:
        for el1 in result:
            if el1[0] in el and el[1] in el and el != el1:
                #Переносит все списки с дублями в другой список, устраняет все дубли с помощью функции
                list_d.append(delete_doubles(el, el1))
                result.remove(el)
                result.remove(el1)
    for el in list_d:
        #Переносит готовые списки обратно в result
        result.append(el)
    return result


def delete_doubles(d1, d2):
    #Объединяет списки с дублями в один
    list_res = []
    for val, key in zip(d1, d2):
        if val == key:
            list_res.append(val)
        elif val == '':
            list_res.append(key)
        elif key == '':
            list_res.append(val)
    return list_res


def result(list_):
    #Создает новый список с измененными номерами
    result_list = list()
    numbers = list()
    for el in sort_list(list_):
        if el[5] != 'phone':
            numbers.append(el[5])
    text = ', '.join(numbers)
    pattern = r'(\+7|8) *\(*(495)\)*[ -]*(\d{3})-*(\d{2})-*(\d{2}) *(\(*(доб.) (\d{4})\)*)*'
    res = re.sub(pattern, r'\1(\2)\3-\4-\5 \7\8', text).split(',')
    res.insert(0, 'phone')
    for el in range(len(sort_list(list_))):
        result_list.append(sort_list(list_)[el])
        result_list[el][5] = res[el]
    return result_list


with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result(contacts_list))
