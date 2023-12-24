import tkinter as tk
import sqlite3
import datetime
import re
from tkcalendar import DateEntry, Calendar
from tkinter import ttk
from tkinter import Toplevel
from tkinter.messagebox import showerror, showwarning, showinfo

def collect_salary_data(id_emp, e_sum, e_ps, e_on, e_od, e_id, sign):
    if sign:
        emp_id = int(id_emp)
    if sign == False:
        emp_id = int(e_id.get())
    summ = str(e_sum.get())
    if e_sum.get() == "":
        showerror(title="Ошибка ввода суммы", message="Введите сумму зарплаты")
        return
    pay_start = str(e_ps.get())
    if e_ps.get() == "":
        showerror(title="Ошибка ввода даты начала выплат", message="Введите дату начала выплат")
        return
    order_number = str(e_on.get())
    if e_on.get() == "":
        showerror(title="Ошибка ввода номера приказа", message="Введите номер приказа")
        return
    order_date = str(e_od.get())
    if e_od.get() == "":
        showerror(title="Ошибка ввода даты приказа", message="Введите дату приказа")
        return

    return [emp_id, summ, pay_start, order_number, order_date]


def commit_salary_edit(data, id_sal):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """UPDATE Salary SET id_emp=?, sum=?, payments_start=?, order_number=?, order_date=? 
               WHERE id_salary=?"""
    data.append(id_sal)
    cursor.execute(query, data)
    db.commit()


def commit_salary_to_database(data):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """INSERT INTO Salary (id_emp, sum, payments_start, order_number, order_date 
        ) VALUES (?, ?, ?, ?, ?)"""

    cursor.execute(query, data)
    db.commit()


def commit_salary(data, sign, id_sal):
    if sign:
        commit_salary_to_database(data)
    else:
        commit_salary_edit(data, id_sal)
  

def create_salary(window, id_emp, sign, id_sal):
    creation = Toplevel(window)
    creation.title('Управление базой данных')
    creation.geometry('800x1000')
    # Table = str(table)
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()

    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()

    l_sum = tk.Label(creation, text="Сумма")
    e_sum = tk.Entry(creation)
    l_sum.grid(row=0, column=0, sticky='w', padx=2)
    e_sum.grid(row=0, column=1, sticky='w', padx=2)

    l_ps = tk.Label(creation, text="Начало выплат")
    e_ps = DateEntry(creation, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    l_ps.grid(row=1, column=0, sticky='w', padx=2)
    e_ps.grid(row=1, column=1, sticky='w', padx=2)

    l_on = tk.Label(creation, text="Номер приказа")
    e_on = tk.Entry(creation)
    l_on.grid(row=2, column=0, sticky='w', padx=2)
    e_on.grid(row=2, column=1, sticky='w', padx=2)

    l_od = tk.Label(creation, text="Дата приказа")
    e_od = DateEntry(creation, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    l_od.grid(row=3, column=0, sticky='w', padx=2)
    e_od.grid(row=3, column=1, sticky='w', padx=2)

    l_id = tk.Label(creation, text="id сотрудника")
    e_id = tk.Entry(creation)
    l_id.grid(row=5, column=0, sticky='w', padx=2)
    e_id.grid(row=5, column=1, sticky='w', padx=2)
    if sign == True:
        e_id.insert(0, id_emp)
        e_id.config(state="readonly")

    if not sign:
        query_job = f"SELECT * FROM Salary WHERE id_salary = '{id_sal}'"
        cursor.execute(query_job)
        data_sal = cursor.fetchall()

        if data_sal:
            e_id.insert(0, data_sal[0][1])
            e_sum.insert(0, data_sal[0][2])
            e_ps.delete(0,'end')
            e_ps.insert(0, data_sal[0][3])
            e_on.insert(0, data_sal[0][4])
            e_od.delete(0,'end')
            e_od.insert(0, data_sal[0][5])
            

    b_commit = tk.Button(creation, text="Сохранить", command=lambda: commit_salary(collect_salary_data(id_emp, e_sum, e_ps, e_on, e_od, e_id, sign), sign, id_sal ))
    b_commit.grid(row=0, column=2, sticky='w', padx=2, pady=2)
