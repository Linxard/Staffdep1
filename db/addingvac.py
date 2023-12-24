import tkinter as tk
import sqlite3
import datetime
from tkcalendar import DateEntry, Calendar
from tkinter import ttk
from tkinter import Toplevel
from tkinter.messagebox import showerror, showwarning, showinfo


def collect_vacation_data(id_emp, cb_typ, e_vs, e_ve, e_id, sign):
    if sign:
        emp_id = int(id_emp)
    if sign == False:
        emp_id = str(e_id.get())
    type = str(cb_typ.get())
    if cb_typ.get() == "":
        showerror(title="Ошибка ввода типа отпуска", message="Выберите тип отпуска")
        return
    vac_start = str(e_vs.get())
    if e_vs.get() == "":
        showerror(title="Ошибка ввода даты начала отпуска", message="Введите дату начала отпуска")
        return
    vac_end = str(e_ve.get())
    if e_ve.get() == "":
        showerror(title="Ошибка ввода даты окончания отпуска", message="Введите дату окончания отпуска")
        return

    return [emp_id, type, vac_start, vac_end]

def commit_vacation_to_database(data):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """INSERT INTO Vacation (id_emp, type, vacation_start, vacation_end 
        ) VALUES (?, ?, ?, ?)"""

    cursor.execute(query, data)
    db.commit()
 

def commit_vacation_edit(data, id_vacation):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """UPDATE Vacation SET id_emp=?, type=?, vacation_start=?, vacation_end=? 
               WHERE id_vacation=?"""
    data.append(id_vacation)
    cursor.execute(query, data)
    db.commit()


def commit_vacation(data, sign, id_vacation):
    if sign:
        commit_vacation_to_database(data)
    else:
        commit_vacation_edit(data, id_vacation)


def create_vacation(window, id_emp, sign, id_vacation):
    creation = Toplevel(window)
    creation.title('Управление базой данных')
    creation.geometry('800x1000')
    # Table = str(table)

    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()

    l_typ = tk.Label(creation, text="Тип отпуска")
    vac_types = ["Основной", "Дополнительный", "Учебный", "Социальный", "Неоплачиваемый"]
    cb_typ = ttk.Combobox(creation, values=vac_types, state="readonly", width=8)
    l_typ.grid(row=0, column=0, sticky='w', padx=2)
    cb_typ.grid(row=0, column=1, sticky='w', padx=2)

    l_vs = tk.Label(creation, text="Начало отпуска")
    e_vs = DateEntry(creation, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    l_vs.grid(row=1, column=0, sticky='w', padx=2)
    e_vs.grid(row=1, column=1, sticky='w', padx=2)

    l_ve = tk.Label(creation, text="Конец отпуска")
    e_ve = DateEntry(creation, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    l_ve.grid(row=2, column=0, sticky='w', padx=2)
    e_ve.grid(row=2, column=1, sticky='w', padx=2)

    l_id = tk.Label(creation, text="id сотрудника")
    e_id = tk.Entry(creation)
    l_id.grid(row=5, column=0, sticky='w', padx=2)
    e_id.grid(row=5, column=1, sticky='w', padx=2)
    if sign == True:
        e_id.insert(0, id_emp)
        e_id.config(state="readonly")

    if not sign:
        query_vac = f"SELECT * FROM Vacation WHERE id_vacation = '{id_vacation}'"
        cursor.execute(query_vac)
        data_vac = cursor.fetchall()

        if data_vac:
            e_id.insert(0, data_vac[0][1])
            cb_typ.set(data_vac[0][2])
            e_vs.delete(0,'end')
            e_vs.insert(0, data_vac[0][3])
            e_ve.delete(0,'end')
            e_ve.insert(0, data_vac[0][4])

    b_commit = tk.Button(creation, text="Сохранить", command=lambda: commit_vacation(collect_vacation_data(id_emp, cb_typ, e_vs, e_ve, e_id, sign), sign, id_vacation))
    b_commit.grid(row=0, column=2, sticky='w', padx=2, pady=2)
