from pprint import pprint
import re

# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

print('Первоначальная таблица: ')
for items in contacts_list:
    print(items)

r1_tel= r'(\+7\s*|8\s*)\(*(\d{3})\)*\s*-*(\d{3})-*\s*(\d{2})-*\s*(\d{2})'
r1_tel_sub = r'+7(\2)\3-\4-\5'

r2_add_tell = r'\(?(доб\.)\s*(\d+)\)?'
r2_add_tell_sub = r'\1\2'

r_tel_add = r'(\+7\s*|8\s*)\(*(\d{3})\)*\s*-*(\d{3})-*\s*(\d{2})-*\s*(\d{2})(\s*|\,)(\(?(доб\.)\s*(\d+)\)?)?'
r_tel_add_sub = r'+7(\2)\3-\4-\5 \8\9'

r3_email = r'(\w+\.?\w+@([a-z0-9]+)\.([a-z]+))'

for i in range(1, len(contacts_list)):

    # Преобразуем телефон и доб.номер с помощью regex
    tel = contacts_list[i][5]
    pattern = re.compile(r_tel_add )
    text_new = pattern.sub(r_tel_add_sub, tel)

    contacts_list[i][5] = text_new


    # Преобразуем имя-фамилию и отчетсво  - вначел обдиняем через join потом разделеяем через
    # группы регулярных выражений

    regexp = re.compile(r'(?P<last>[-а-яёА-ЯЁ]+)' #Фамилия
                        r'( (?P<first>([-а-яёА-ЯЁ]+)))?' # Имя необязательное
                        r'( (?P<middle>([-а-яёА-ЯЁ]+)))?' # Отчетсво необязательное

                        )
    name = contacts_list[i][0:3]
    delimiter = ' '
    single_str_name = delimiter.join(name)


    result = regexp.search(single_str_name)
    lastname = result.group('last')
    firstname = result.group('first')
    if firstname == None:
        firstname = ''
    middlename = result.group('middle')
    if middlename == None:
        middlename = ''

    contacts_list[i][0] = lastname
    contacts_list[i][1] = firstname
    contacts_list[i][2] = middlename

print('\nТаблица с отформатированнми именами и телефонами:')
for items in contacts_list:
    print(items)


# Убираем дублирующие строки и дополняем информацию
# Форимруем множество уникальных имен
name_set = []
for i in range(1, len(contacts_list)):
    name_set.append(contacts_list[i][0])

name_set = set(name_set)


#Новая финальная таблица
new_table=[]
for name in name_set:
    new_row_name = []
    # Запомениаем кол-во индексом с дублирующие данныыми
    index = []
    for i in range(1, len(contacts_list)):
        # проверяем по первому имени
        if name == contacts_list[i][0]:
            index.append(i)

    # Если ФИО - одина раз упомнинается
    if len(index) == 1:
        new_table.append(contacts_list[index[0]])

    # Если ФИО дублируется два раза
    else:
        for y in range(0,7):
            if contacts_list[index[0]][y] == contacts_list[index[1]][y]:

                new_row_name.append(contacts_list[index[0]][y])
            elif (contacts_list[index[0]][y] == '' and contacts_list[index[1]][y]):
                new_row_name.append(contacts_list[index[1]][y])
            elif (contacts_list[index[0]][y] and contacts_list[index[1]][y]== ''):
                new_row_name.append(contacts_list[index[0]][y])
            elif (contacts_list[index[0]][y] == '' and contacts_list[index[1]][y] == ''):
                txt = ''
                new_row_name.append(txt)

        new_table.append(new_row_name)

#Добавляем первую строку - названия столбцов
new_table.insert(0, contacts_list[0])

print('\nФинальная таблица:')
for item in new_table:
    print(item)

with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(new_table)