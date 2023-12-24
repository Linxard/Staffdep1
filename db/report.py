import tkinter as tk
import sqlite3
import datetime
import datetime
from tkcalendar import DateEntry, Calendar
from tkinter import ttk
from tkinter import Toplevel
from tkinter.messagebox import showerror, showwarning, showinfo

def get_fio(id, db):
    cursor = db.cursor()
    query = """SELECT last_name, first_name, middle_name FROM Employee WHERE Employee.id_emp=?"""
    cursor.execute(query, (id,))
    data = cursor.fetchone()
    fio = ' '.join(map(str, data))
    return fio
    
def get_pos(id, db):
    cursor = db.cursor()
    query = """SELECT position FROM Job INNER JOIN Employee on Employee.id_emp = Job.id_emp WHERE Employee.id_emp=?"""
    cursor.execute(query, (id,))
    data = cursor.fetchall()

    return data

def get_ws(id, db):
    cursor = db.cursor()
    query = """SELECT working_start FROM Job INNER JOIN Employee on Employee.id_emp = Job.id_emp
   WHERE Employee.id_emp=? ORDER BY working_start ASC LIMIT 1"""
    cursor.execute(query, (id,))
    data = cursor.fetchall()

    return data

def get_ed(id, db):
    cursor = db.cursor()
    query = """SELECT specialty FROM Education INNER JOIN Employee on Employee.id_emp = Education.id_emp WHERE Employee.id_emp=?"""
    cursor.execute(query, (id,))
    data = cursor.fetchall()

    return data

def get_phone(id, db):
    cursor = db.cursor()
    query = """SELECT phone_number FROM Employee WHERE Employee.id_emp = ?"""
    cursor.execute(query, (id,))
    data = cursor.fetchall()

    return data

def get_mail(id, db):
    cursor = db.cursor()
    query = """SELECT email FROM Employee WHERE Employee.id_emp = ?"""
    cursor.execute(query, (id,))
    data = cursor.fetchall()

    return data

def get_vac(id, db):
    cursor = db.cursor()
    query = """SELECT vacation_end FROM Vacation INNER JOIN Employee on Employee.id_emp = Vacation.id_emp
   WHERE Employee.id_emp=? ORDER BY vacation_end DESC LIMIT 1"""
    cursor.execute(query, (id,))
    data = cursor.fetchone()

    if data:
        vacation_end = datetime.strptime(data[0], '%Y-%m-%d')
        current_date = datetime.now()

        if current_date < vacation_end:
            return f"В отпуске до {data[0]}"
        else:
            return "Не в отпуске"
    else:
        return "Не в отпуске"
def create_report(window, id_emp):
    db = sqlite3.connect('staffdep.db')

    creation = Toplevel(window)
    creation.title('Управление базой данных')
    creation.geometry('800x1000')

    l_fio = tk.Label(creation, text="ФИО")
    l_fio.grid(row=0, column=0, sticky='w', padx=2)
    e_fio = tk.Text(creation, height=1, width=30)
    e_fio.insert("1.0", get_fio(id_emp, db))
    e_fio.configure(state="disabled", bd=0, highlightthickness=0)
    e_fio.grid(row=0, column=1, sticky='w', padx=2)

    l_pos = tk.Label(creation, text="Должность")
    l_pos.grid(row=1, column=0, sticky='w', padx=2)
    e_pos = tk.Text(creation, height=1, width=30)
    e_pos.insert("1.0", get_pos(id_emp, db))
    e_pos.configure(state="disabled", bd=0, highlightthickness=0)
    e_pos.grid(row=1, column=1, sticky='w', padx=2)

    l_ws = tk.Label(creation, text="Начало работы в компании")
    l_ws.grid(row=2, column=0, sticky='w', padx=2)
    e_ws = tk.Text(creation, height=1, width=30)
    e_ws.insert("1.0", get_ws(id_emp, db))
    e_ws.configure(state="disabled", bd=0, highlightthickness=0)
    e_ws.grid(row=2, column=1, sticky='w', padx=2)

    l_ed = tk.Label(creation, text="Образование")
    l_ed.grid(row=3, column=0, sticky='w', padx=2)
    e_ed = tk.Text(creation, height=1, width=30)
    e_ed.insert("1.0", get_ed(id_emp, db))
    e_ed.configure(state="disabled", bd=0, highlightthickness=0)
    e_ed.grid(row=3, column=1, sticky='w', padx=2)

    l_pn = tk.Label(creation, text="Телефонный номер")
    l_pn.grid(row=4, column=0, sticky='w', padx=2)
    e_pn = tk.Text(creation, height=1, width=30)
    e_pn.insert("1.0", get_phone(id_emp, db))
    e_pn.configure(state="disabled", bd=0, highlightthickness=0)
    e_pn.grid(row=4, column=1, sticky='w', padx=2)

    l_em = tk.Label(creation, text="E-mail")
    l_em.grid(row=5, column=0, sticky='w', padx=2)
    e_em = tk.Text(creation, height=1, width=30)
    e_em.insert("1.0", get_mail(id_emp, db))
    e_em.configure(state="disabled", bd=0, highlightthickness=0)
    e_em.grid(row=5, column=1, sticky='w', padx=2)

    l_vac = tk.Label(creation, text="Находится ли в отпуске")
    l_vac.grid(row=6, column=0, sticky='w', padx=2)
    e_vac = tk.Text(creation, height=1, width=30)
    e_vac.insert("1.0", get_vac(id_emp, db))
    e_vac.configure(state="disabled", bd=0, highlightthickness=0)
    e_vac.grid(row=6, column=1, sticky='w', padx=2)
    
   


