import json
import os
from datetime import datetime

def request_to_json(request, valid_mimetypes, upload_folder):
    '''
    получает json результат по запросу
    '''
    #проверяем есть ли файл
    if not 'file' in request.files:
        return json.dumps({'error': 'no file'}), 400
    #получаем информацию о файле
    file = request.files.get('file')
    filename = file.filename
    mimetype = file.content_type
    #проверяем тип файла
    if not mimetype in valid_mimetypes:
        return json.dumps({'error': 'bad-type'}), 400
    #сохраняем файл
    now = datetime.now()
    time = now.strftime("%m_%d_%Y_%H_%M_%S_")
    filename_full = f'{time}_{filename}'
    if not os.path.exists(upload_folder):
        os.mkdir(upload_folder)
    file_path = os.path.join(upload_folder, filename_full)
    file.save(file_path)
    #работаем с файлом
    with open(file_path, "r") as f:
        text = f.read()
    #удаляем файл
    os.remove(file_path)
    return str_to_json_struct(text), 200

def id_to_json(id, json_folder):
    json_path = os.path.join(json_folder, f'{id}.json')
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            json_text = f.read()
            return json_text, 200
    else:
        return json.dumps({'error': 'wrong id'}), 400
    
def get_lines(s):
    '''
    разделяет общую строку на строки
    по символам \r и \n
    '''
    arr_without_cr = s.split('\r')
    arr_without_cr_and_lf = []
    for v in arr_without_cr:
        vsplit = v.split('\n')
        if '' in vsplit:
            vsplit.remove('')
        arr_without_cr_and_lf.extend(vsplit)
    return arr_without_cr_and_lf

def count_level(s):
    '''
    определяет уровень вложенности раздела строки
    (считает количество знаков "#")
    если уровень равен 0, значит, строка не является
    заголовком раздела, а является содержимым предыдущего раздела
    '''
    lvl = 0
    while s[lvl] == '#':
        lvl+=1
        if lvl == len(s):
            return lvl
    return lvl

def get_levels(lines):
    '''
    записывает номера строк и их уровень в один список
    '''
    levels = []
    cutted_lines = []
    for i,line in enumerate(lines):
        level = count_level(line)
        levels.append([i,level])
        cutted_lines.append(line[level:])
    return levels, cutted_lines

def get_struct(levels, n):
    '''
    преобразуем список номеров страниц и их уровней в 
    список словарей с полями:

    "section" - номер строки, содержащей название раздела уровня n
    "content" - список строк, содержащихся в данном разделе
    "subsections" - список строк, являющимися подразделами данного раздела
    каждый подраздел содержит такую же структуру
    '''
    levels_new = []
    for i,v in enumerate(levels):
        #находим в списке разделы уровня n, добавляем словарь
        if v[1] == n:
            levels_new.append({"section":v[0], "content":[], "subsections":[]})
        else:
            if v[1] == 0:
                try:
                    #последующие строки с уровнем 0 помещаем в поле "content"
                    levels_new[-1]["content"].append(v[0])
                except IndexError:
                    print('Неправильная структура разделов. Перед содержимым раздела нет заголовка раздела')
            else:
                try:
                    #если уровень последующих строк не равен ни n ни 0,
                    #то помещаем их в список в поле "subsections"
                    levels_new[-1]["subsections"].append(v)
                except IndexError:
                    print('Неправильная структура разделов. Перед подразделом нет раздела более высокого уровня')
    #проверяем, можно ли разбить список еще на более глубокие подразделы
    #проходим по всем получившимся словарям
    for i,v in enumerate(levels_new):
        if len(v["subsections"])>0:
            #выполняем функцию еще раз для подразделов,
            #увеличив уровень глубины разделов на 1
            subsections = get_struct(v["subsections"],n+1)
            levels_new[i]["subsections"] = subsections
    return levels_new

def str_to_json_struct(s):
    '''
    комбинирует все функции в одну
    формирует общий json
    '''
    lines = get_lines(s)
    levels, lines = get_levels(lines)
    struct = get_struct(levels,1)
    struct_main = {"lines":lines, "structure":struct}
    return json.dumps(struct_main)