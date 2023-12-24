
import tkinter as tk
import sqlite3
import datetime
from tkcalendar import DateEntry, Calendar
from tkinter import ttk
from tkinter import Toplevel
from tkinter.messagebox import showerror, showwarning, showinfo

global emp_id

def collect_education_data(e_id, e_inst, e_fac, cb_tut, e_sp, e_eds, e_edn, id_emp, sign):
    if sign == False:
        emp_id = str(e_id.get())
    if sign:
        emp_id = id_emp
    inst = str(e_inst.get())
    if e_inst.get() == "":
        showerror(title="Ошибка ввода названия учреждения", message="Введите название учреждения")
        return
    fac = str(e_fac.get())
    if e_fac.get() == "":
        showerror(title="Ошибка ввода факультета", message="Введите название факультета")
        return
    tut = cb_tut.get()
    if cb_tut.get() == "":
        showerror(title="Ошибка ввода типа обучения", message="Введите выберите тип")
        return
    sp = str(e_sp.get())
    if e_sp.get() == "":
        showerror(title="Ошибка ввода специальности", message="Введите специальность")
        return
    eds = str(e_eds.get())
    if e_eds.get() == "":
        showerror(title="Ошибка ввода даты начала обучения", message="Введите дату")
        return
    edn = str(e_edn.get())
    if e_edn.get() == "":
        showerror(title="Ошибка ввода даты окончания обучения", message="Введите дату")
        return

    return [emp_id, inst, fac, tut, sp, eds, edn]

def commit_education_to_database(data):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """INSERT INTO Education (id_emp, institute_name, faculty, tution, specialty, education_start, education_end) 
            VALUES (?, ?, ?, ?, ?, ?, ?)"""

    cursor.execute(query, data)
    db.commit()
    

def commit_education_edit(data, id_diploma):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """UPDATE Education SET id_emp=?, institute_name=?, faculty=?, tution=?, specialty=?, education_start=?, education_end=? 
            WHERE id_diploma=?"""
    data.append(id_diploma)
    cursor.execute(query, data)
    db.commit()
    

def commit_education(data, sign, id_diploma):
    if sign:
        commit_education_to_database(data)
    else:
        commit_education_edit(data, id_diploma)

def create_education(window, id_emp, sign, id_diploma):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = f"SELECT Education.* FROM Education WHERE id_diploma = '{id_diploma}'"
    cursor.execute(query)
    data = cursor.fetchall()

    creation = Toplevel(window)
    creation.title('Управление базой данных')
    creation.geometry('800x1000')

    l_inst = tk.Label(creation, text="Учреждение")
    e_inst = tk.Entry(creation)
    l_inst.grid(row=0, column=0, sticky='w', padx=2)
    e_inst.grid(row=0, column=1, sticky='w', padx=2)
    if sign == False:
        e_inst.insert(0, data[0][2])

    l_fac = tk.Label(creation, text="Факультет")
    e_fac = tk.Entry(creation)
    l_fac.grid(row=2, column=0, sticky='w', padx=2)
    e_fac.grid(row=2, column=1, sticky='w', padx=2)
    if sign == False:
        e_fac.insert(0, data[0][3])

    l_tut = tk.Label(creation, text="Форма обучения")
    tutions = ["Очная", "Заочная"]
    cb_tut = ttk.Combobox(creation, values=tutions, state="readonly")
    l_tut.grid(row=3, column=0, sticky='w', padx=2)
    cb_tut.grid(row=3, column=1, sticky='w', padx=2)
    if sign == False:
        cb_tut.set(data[0][4])

    l_sp = tk.Label(creation, text="Специальность")
    e_sp = tk.Entry(creation)
    l_sp.grid(row=4, column=0, sticky='w', padx=2)
    e_sp.grid(row=4, column=1, sticky='w', padx=2)
    if sign == False:
        e_sp.insert(0, data[0][5])

    l_eds = tk.Label(creation, text="Дата начала обучения")
    e_eds = DateEntry(creation, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    l_eds.grid(row=5, column=0, sticky='w', padx=2)
    e_eds.grid(row=5, column=1, sticky='w', padx=2)
    if sign == False:
        e_eds.delete(0,'end')
        e_eds.insert(0, data[0][6])

    l_edn = tk.Label(creation, text="Дата окончания обучения")
    e_edn = DateEntry(creation, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    l_edn.grid(row=6, column=0, sticky='w', padx=2)
    e_edn.grid(row=6, column=1, sticky='w', padx=2)
    if sign == False:
        e_edn.delete(0,'end')
        e_edn.insert(0, data[0][7])
   
    l_id = tk.Label(creation, text="id сотрудника")
    e_id = tk.Entry(creation)
    l_id.grid(row=7, column=0, sticky='w', padx=2)
    e_id.grid(row=7, column=1, sticky='w', padx=2)
    if  sign == False:
        e_id.insert(0, data[0][1])
    elif sign == True:
        e_id.insert(0, id_emp)
        e_id.config(state="readonly")


    b_commit = tk.Button(creation, text="Сохранить", 
                        command=lambda: commit_education(collect_education_data(e_id, e_inst, e_fac, cb_tut, e_sp, e_eds, e_edn, id_emp, sign), sign, id_diploma))
    b_commit.grid(row=0, column=2, sticky='w', padx=2, pady=2)