import tkinter as tk
import sqlite3
import datetime
from tkcalendar import DateEntry, Calendar
from tkinter import ttk
from tkinter import Toplevel
from tkinter.messagebox import showerror, showwarning, showinfo


def collect_family_data(id_emp, cb_fam, e_fn, e_sn, e_mn, e_bd, e_id, sign):
    if sign == False:
        emp_id = str(e_id.get())
    if sign:
        emp_id = id_emp
    family_ship = str(cb_fam.get())
    if cb_fam.get() == "":
        showerror(title="Ошибка ввода родства", message="Выберите тип родства")
        return
    first_name = str(e_fn.get())
    if e_fn.get() == "":
        showerror(title="Ошибка ввода Имени", message="Введите Имя")
        return
    second_name = str(e_sn.get())
    if e_sn.get() == "":
        showerror(title="Ошибка ввода фамилии", message="Введите фамилию")
        return
    middle_name = str(e_mn.get())
    if e_mn.get() == "":
        showerror(title="Ошибка ввода отчества", message="Введите отчество")
        return
    birth_date = str(e_bd.get())
    if e_bd.get() == "":
        showerror(title="Ошибка ввода даты рождения", message="Введите дату рождения")
        return

    return [emp_id, family_ship, first_name, second_name, middle_name, birth_date]

def commit_family_to_database(data):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """INSERT INTO Family (id_emp, familyship, first_name, second_name, middle_name, birth_date) 
            VALUES (?, ?, ?, ?, ?, ?)"""

    cursor.execute(query, data)
    db.commit()

def commit_family_edit(data, id_member):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """UPDATE Family SET id_emp=?, familyship=?, first_name=?, second_name=?, middle_name=?, birth_date=? 
            WHERE id_member=?"""
    data.append(id_member)
    cursor.execute(query, data)
    db.commit()

def commit_family(data, sign, id_member):
    if sign:
        commit_family_to_database(data)
    else:
        commit_family_edit(data, id_member)

def create_fam(window, id_emp, sign, id_member):

    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = f"SELECT * FROM Family WHERE id_member = '{id_member}'"
    cursor.execute(query)
    data = cursor.fetchall()

    creation = Toplevel(window)
    creation.title('Управление базой данных')
    creation.geometry('300x150')
    creation.resizable(0, 0)

    types = ["Сын/Дочь", "Муж/Жена", "Отец/Мать"]

    l_fam = tk.Label(creation, text="Тип родства")
    cb_fam = ttk.Combobox(creation, values=types, state="readonly")
    l_fam.grid(row=0, column=0, sticky='w', padx=2)
    cb_fam.grid(row=0, column=1, sticky='w', padx=2)
    if sign == False:
        cb_fam.set(data[0][2])

    l_fn = tk.Label(creation, text="Имя")
    e_fn = tk.Entry(creation)
    l_fn.grid(row=2, column=0, sticky='w', padx=2)
    e_fn.grid(row=2, column=1, sticky='w', padx=2)
    if sign == False:
        e_fn.insert(0, data[0][3])

    l_sn = tk.Label(creation, text="Фамилия")
    e_sn = tk.Entry(creation)
    l_sn.grid(row=3, column=0, sticky='w', padx=2)
    e_sn.grid(row=3, column=1, sticky='w', padx=2)
    if sign == False:
        e_sn.insert(0, data[0][4])

    l_mn = tk.Label(creation, text="Отчество")
    e_mn = tk.Entry(creation)
    l_mn.grid(row=4, column=0, sticky='w', padx=2)
    e_mn.grid(row=4, column=1, sticky='w', padx=2)
    if sign == False:
        e_mn.insert(0, data[0][5])

    l_bd = tk.Label(creation, text="Дата рождения")
    e_bd = DateEntry(creation, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    l_bd.grid(row=5, column=0, sticky='w', padx=2)
    e_bd.grid(row=5, column=1, sticky='w', padx=2)
    if sign == False:
        e_bd.delete(0,'end')
        e_bd.insert(0, data[0][6])

    l_id = tk.Label(creation, text="id сотрудника")
    e_id = tk.Entry(creation)
    l_id.grid(row=6, column=0, sticky='w', padx=2)
    e_id.grid(row=6, column=1, sticky='w', padx=2)
    if sign == False:
        e_id.insert(0, data[0][1])
    elif sign == True:
        e_id.insert(0, id_emp)
        e_id.config(state="readonly")

    b_commit = tk.Button(creation, text="Сохранить", command=lambda: commit_family(collect_family_data(id_emp, cb_fam, e_fn, e_sn, e_mn, e_bd, e_id, sign), sign, id_member))
    b_commit.grid(row=0, column=2, sticky='w', padx=2, pady=2)
