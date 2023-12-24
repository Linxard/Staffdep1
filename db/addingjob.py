import tkinter as tk
import sqlite3
import datetime
from tkcalendar import DateEntry, Calendar
from tkinter import ttk
from tkinter import Toplevel
from tkinter.messagebox import showerror, showwarning, showinfo


def collect_job_data(id_emp, cb_dep, cb_pos, e_on, e_od, e_ws, e_id, dep, pos, sign):
    if sign == False:
        emp_id = str(e_id.get())
    if sign:
        emp_id = id_emp

    selected_dep = str(cb_dep.get())
    if cb_dep.get() == "":
        showerror(title="Ошибка ввода отдела", message="Выберите отдел")
        return
    selected_pos= str(cb_pos.get())
    if cb_pos.get() == "":
        showerror(title="Ошибка ввода должности", message="Выберите должность")
        return

    order_name = str(e_on.get())
    if e_on.get() == "":
        showerror(title="Ошибка ввода номера приказа", message="Введите номер приказа")
        return
    order_date = str(e_od.get())
    if e_od.get() == "":
        showerror(title="Ошибка ввода даты приказа", message="Введите дату приказа")
        return
    working_start = str(e_ws.get())
    if e_ws.get() == "":
        showerror(title="Ошибка ввода даты начала работы", message="Введите дату начала работы")
        return

    return [emp_id, selected_dep, selected_pos, order_name, order_date, working_start]

def commit_job_to_database(data):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """INSERT INTO Job (id_emp, department, position, order_number, order_date, working_start) 
               VALUES (?, ?, ?, ?, ?, ?)"""

    cursor.execute(query, data)
    db.commit()

def commit_job_edit(data, id_job):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """UPDATE Job SET id_emp=?, department=?, position=?, order_number=?, order_date=?, working_start=? 
               WHERE id_job=?"""
    data.append(id_job)
    cursor.execute(query, data)
    db.commit()

def commit_job(data, sign, id_job):
    if sign:
        commit_job_to_database(data)
    else:
        commit_job_edit(data, id_job)

def create_job(window, id_emp, dep, pos, sign, id_job):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()

    creation = Toplevel(window)
    creation.title('Управление базой данных')
    creation.geometry('800x1000')

    dep_values = list(dep.values())
    pos_values = list(pos.values())

    l_dep = tk.Label(creation, text="Отдел")
    cb_dep = ttk.Combobox(creation, values=dep_values, state="readonly")
    l_dep.grid(row=0, column=0, sticky='w', padx=2)
    cb_dep.grid(row=0, column=1, sticky='w', padx=2)

    l_pos = tk.Label(creation, text="Должность")
    cb_pos = ttk.Combobox(creation, values=pos_values, state="readonly")
    l_pos.grid(row=2, column=0, sticky='w', padx=2)
    cb_pos.grid(row=2, column=1, sticky='w', padx=2)

    l_on = tk.Label(creation, text="Номер приказа")
    e_on = tk.Entry(creation)
    l_on.grid(row=3, column=0, sticky='w', padx=2)
    e_on.grid(row=3, column=1, sticky='w', padx=2)

    l_od = tk.Label(creation, text="Дата приказа")
    e_od = DateEntry(creation, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    l_od.grid(row=4, column=0, sticky='w', padx=2)
    e_od.grid(row=4, column=1, sticky='w', padx=2)

    l_ws = tk.Label(creation, text="Начало работы")
    e_ws = DateEntry(creation, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    l_ws.grid(row=5, column=0, sticky='w', padx=2)
    e_ws.grid(row=5, column=1, sticky='w', padx=2)

    l_id = tk.Label(creation, text="id сотрудника")
    e_id = tk.Entry(creation)
    l_id.grid(row=6, column=0, sticky='w', padx=2)
    e_id.grid(row=6, column=1, sticky='w', padx=2)
    if sign == True:
        e_id.insert(0, id_emp)
        e_id.config(state="readonly")

    if not sign:
        query_job = f"SELECT * FROM Job WHERE id_job = '{id_job}'"
        cursor.execute(query_job)
        data_job = cursor.fetchall()

        if data_job:
            cb_dep.set(data_job[0][2])
            cb_pos.set(data_job[0][3])
            e_on.insert(0, data_job[0][4])
            e_id.delete(0,'end')
            e_od.insert(0, data_job[0][5])
            e_ws.delete(0,'end')
            e_ws.insert(0, data_job[0][6])
            e_id.insert(0, data_job[0][1])

    b_commit = tk.Button(creation, text="Сохранить", command=lambda: commit_job(collect_job_data(id_emp, cb_dep, cb_pos, e_on, e_od, e_ws, e_id, dep, pos, sign), sign, id_job))
    b_commit.grid(row=0, column=2, sticky='w', padx=2, pady=2)
