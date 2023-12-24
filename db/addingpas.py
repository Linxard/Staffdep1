import tkinter as tk
import sqlite3
import datetime
import re
from tkcalendar import DateEntry, Calendar
from tkinter import ttk
from tkinter import Toplevel
from tkinter.messagebox import showerror, showwarning, showinfo

def validate_series(ser):
    if ser and re.match(r'^\d{6}$', ser):
        return True
    return False

def validate_number(num):
    if num and re.match(r'^\d{4}$', num):
        return True
    return False

def collect_passport_data(id_emp, e_ser, e_num, e_gb_dep, e_gb_c, e_gb_dis, e_gd, e_id, sign):
    if sign:
        emp_id = int(id_emp)
    if not sign:
        emp_id = int(e_id.get())
    series = str(e_ser.get())
    if not validate_series(series):
        showerror(title="Ошибка ввода серии паспорта", message="Выберите серию в формате xxxxxx")
        return None
    number = str(e_num.get())
    if not validate_number(number):
        showerror(title="Ошибка ввода номера паспорта", message="Выберите номер в формате xxxx")
        return None
    given_by = ' '.join([str(e_gb_dep.get()), str(e_gb_c.get()), str(e_gb_dis.get())])
    if e_gb_dep.get() == "" or e_gb_c.get() == "" or e_gb_dis.get() == "":
        showerror(title="Ошибка ввода выдачи паспорта", message="Введите кем был паспорт выдан")
        return None
    given_date = str(e_gd.get())
    if given_date == "":
        showerror(title="Ошибка ввода даты выдачи", message="Введите дату выдачи паспорта")
        return None

    return [emp_id, series, number, given_by, given_date]

def commit_passport_to_database(data):
    if data is None:
        return  # Прерывание выполнения при возникновении ошибки валидации

    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """INSERT INTO Passport (id_emp, series, number, given_by, given_date) 
               VALUES (?, ?, ?, ?, ?)"""

    cursor.execute(query, data)
    db.commit()


def commit_passport_edit(data, id_passport):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """UPDATE Passport SET id_emp=?, series=?, number=?, given_by=?, given_date=? 
               WHERE id_passport=?"""
    data.append(id_passport)
    cursor.execute(query, data)
    db.commit()


def commit_passport(data, sign, id_passport):
    if sign:
        commit_passport_to_database(data)
    else:
        commit_passport_edit(data, id_passport)

def create_passport(window, id_emp, sign, id_passport):
    creation = Toplevel(window)
    creation.title('Управление базой данных')
    creation.geometry('800x1000')
    #Table = str(table)

    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()

    l_ser = tk.Label(creation, text="Серия")
    e_ser = tk.Entry(creation)
    l_ser.grid(row=0, column=0, sticky='w', padx=2)
    e_ser.grid(row=0, column=1, sticky='w', padx=2)

    l_num = tk.Label(creation, text="Номер")
    e_num = tk.Entry(creation)
    l_num.grid(row=2, column=0, sticky='w', padx=2)
    e_num.grid(row=2, column=1, sticky='w', padx=2)

    l_gb = tk.Label(creation, text="Кем выдан", width="10")
    l_gb.grid(row=3, column=0, sticky='w')
    l_gb_dep = tk.Label(creation, text="Отдел", width='6')
    l_gb_dep.grid(row=3, column=1, sticky='w', padx=2)
    e_gb_dep = tk.Entry(creation)
    e_gb_dep.grid(row=3, column=2, sticky='w', padx=2)
    l_gb_c = tk.Label(creation, text="Город", width='8')
    l_gb_c.grid(row=3, column=3, sticky='w', padx=2)
    e_gb_c = tk.Entry(creation, width='10')
    e_gb_c.grid(row=3, column=4, sticky='w', padx=2)
    l_gb_dis = tk.Label(creation, text="Код подразделения", width='16')
    l_gb_dis.grid(row=3, column=5, sticky='w', padx=4)
    e_gb_dis = tk.Entry(creation, width='8')
    e_gb_dis.grid(row=3, column=6, sticky='w', padx=2)

    l_gd = tk.Label(creation, text="Дата выдачи")
    e_gd = DateEntry(creation, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    l_gd.grid(row=4, column=0, sticky='w', padx=2)
    e_gd.grid(row=4, column=1, sticky='w', padx=2)

    l_id = tk.Label(creation, text="id сотрудника")
    e_id = tk.Entry(creation)
    l_id.grid(row=5, column=0, sticky='w', padx=2)
    e_id.grid(row=5, column=1, sticky='w', padx=2)
    if sign == True:
        e_id.insert(0, id_emp)
        e_id.config(state="readonly")

    if not sign:
        query_passport = f"SELECT * FROM Passport WHERE id_passport = '{id_passport}'"
        cursor.execute(query_passport)
        data_passport = cursor.fetchall()

        if data_passport:
            data_gb = data_passport[0][4].split()
            e_id.insert(0, data_passport[0][1])
            e_ser.insert(0, data_passport[0][2])
            e_num.insert(0, data_passport[0][3])
            e_gb_dep.insert(0, data_gb[0])
            e_gb_c.insert(0, data_gb[1])
            e_gb_dis.insert(0, data_gb[2])
            e_gd.delete(0,'end')
            e_gd.insert(0, data_passport[0][5])

    b_commit = tk.Button(creation, text="Сохранить", command=lambda: commit_passport(collect_passport_data(id_emp, e_ser, e_num, e_gb_dep, e_gb_c, e_gb_dis, e_gd, e_id, sign), sign, id_passport))
    b_commit.grid(row=0, column=2, sticky='w', padx=2, pady=2)
