import tkinter as tk
import sqlite3
import datetime
import re
from tkcalendar import DateEntry, Calendar
from tkinter import ttk
from tkinter import Toplevel
from tkinter.messagebox import showerror, showwarning, showinfo

def validate_phone_number(pn):
    # Validate phone number: Not more than 12 characters and starts with +7
    return re.match(r'^\+7\d{1,11}$', pn) #Валидация не больше 12 символов в формате +7xxxxxxxxxx

def validate_snils(pc):
    return re.match(r'^\d{3}-\d{3}-\d{3} \d{2}$', pc) #Валидация не больше 14 символов в формате xxx-xxx-xxx xx

def collect_data(e_fn, e_sn, e_mn, cb_gen, e_birth, cb_ms, e_addr_c, e_addr_st, e_addr_h, e_addr_f, e_pn, e_em, e_pc):
    fin = str(e_fn.get())
    if e_fn.get() == "":
        showerror(title="Ошибка ввода Имени", message="Введите Имя")
        return
    sn = str(e_sn.get())
    if e_sn.get() == "":
        showerror(title="Ошибка ввода Фамилии", message="Введите Фамилию")
        return
    mn = str(e_mn.get())
    if e_mn.get() == "":
        showerror(title="Ошибка ввода Отчества", message="Введите Отчество")
        return
    gen = cb_gen.get()
    if e_fn.get() == "":
        showerror(title="Ошибка ввода пола", message="Введите ваш пол")
        return
    birth = str(e_birth.get())
    if e_fn.get() == "":
        showerror(title="Ошибка ввода даты рождения", message="Введите дату рождения")
        return
    ms = cb_ms.get()
    if e_fn.get() == "":
        showerror(title="Ошибка ввода семейного положения", message="Введите семейное положение")
        return
    add = ' '.join([str(e_addr_c.get()), str(e_addr_st.get()), str(e_addr_h.get()), str(e_addr_f.get())])
    pn = str(e_pn.get())
    if not validate_phone_number(pn):
        showerror(title="Ошибка ввода номера", message="Неправильно набран номер, пожалуйста введи номер начиная с +7.")
        return
    em = str(e_em.get())
    pc = str(e_pc.get())
    if not validate_snils(pc):
        showerror(title="Ошибка ввода СНИЛС", message="Неправильно введен СНИЛС, пожалуйста введи СНИЛС в формате xxx-xxx-xxx xx.")
        return

    return [fin, sn, mn, gen, birth, ms, add, pn, em, pc]

def commit_to_database(data):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """INSERT INTO Employee (first_name, last_name, middle_name, gender, birth_date, martial_status, 
        address, phone_number, email, pension_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    cursor.execute(query, data)
    db.commit()

def commit_edit(data, id):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    query = """UPDATE Employee SET first_name=?, last_name=?, middle_name=?, gender=?, birth_date=?, martial_status=?, 
        address=?, phone_number=?, email=?, pension_code=? WHERE id_emp=?"""
    data.append(id)
    cursor.execute(query, data)
    db.commit()

def commit(e_fn, e_sn, e_mn, cb_gen, e_birth, cb_ms, e_addr_c, e_addr_st, e_addr_h, e_addr_f, e_pn, e_em, e_pc, sign, id):
    data = collect_data(e_fn, e_sn, e_mn, cb_gen, e_birth, cb_ms, e_addr_c, e_addr_st, e_addr_h, e_addr_f, e_pn, e_em, e_pc)
    #showinfo(title="tired", message=data)    
    if data:
        if sign == True:
            commit_to_database(data)
        else:
            commit_edit(data, id)



def create_employee(window, sign, id):
    creation = Toplevel(window)
    creation.title('Управление базой данных')
    creation.geometry('800x1000')

    l_fn = tk.Label(creation, text="Имя")
    e_fn = tk.Entry(creation)
    l_fn.grid(row=0, column=0, sticky='w', padx=2)
    e_fn.grid(row=0, column=1, sticky='w', padx=2)
    
    l_sn = tk.Label(creation, text="Фамилия")
    e_sn = tk.Entry(creation)
    l_sn.grid(row=1, column=0, sticky='w', padx=2)
    e_sn.grid(row=1, column=1, sticky='w', padx=2)
    
    l_mn = tk.Label(creation, text="Отчество")
    e_mn = tk.Entry(creation)
    l_mn.grid(row=2, column=0, sticky='w', padx=2)
    e_mn.grid(row=2, column=1, sticky='w', padx=2)

    l_gen = tk.Label(creation, text="Пол")
    genders = ["М", "Ж"]
    cb_gen = ttk.Combobox(creation, values=genders, state="readonly")
    l_gen.grid(row=3, column=0, sticky='w', padx=2)
    cb_gen.grid(row=3, column=1, sticky='w', padx=2)

    l_birth = tk.Label(creation, text="Дата рождения")
    e_birth = DateEntry(creation, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    l_birth.grid(row=4, column=0, sticky='w', padx=2)
    e_birth.grid(row=4, column=1, sticky='w', padx=2)

    l_ms = tk.Label(creation, text="Семейное положение")
    martial_status = ["Холост", "Не замужем", "Женат", "За мужем"]
    cb_ms = ttk.Combobox(creation, values=martial_status, state="readonly")
    l_ms.grid(row=5, column=0, sticky='w', padx=2)
    cb_ms.grid(row=5, column=1, sticky='w', padx=2)

    l_addr = tk.Label(creation, text="Адрес", width = "4")
    l_addr.grid(row=6, column=0, sticky='w')

    l_addr_c = tk.Label(creation, text="Город", width = "4")
    e_addr_c = tk.Entry(creation, width = "20")
    l_addr_c.grid(row=6, column=1, sticky='w', padx=1)
    e_addr_c.grid(row=6, column=2, sticky='w', padx=1)

    l_addr_st = tk.Label(creation, text="Улица", width = "4")
    e_addr_st = tk.Entry(creation, width = "20")
    l_addr_st.grid(row=6, column=3, sticky='w', padx=1)
    e_addr_st.grid(row=6, column=4, sticky='w', padx=1)

    l_addr_h = tk.Label(creation, text="Дом", width = "4")
    e_addr_h = tk.Entry(creation, width = "6")
    l_addr_h.grid(row=6, column=5, sticky='w', padx=1)
    e_addr_h.grid(row=6, column=6, sticky='w', padx=1)

    l_addr_f = tk.Label(creation, text="Квартира", width = "7")
    e_addr_f = tk.Entry(creation, width = "6")
    l_addr_f.grid(row=6, column=7, sticky='w', padx=1)
    e_addr_f.grid(row=6, column=8, sticky='w', padx=1)

    l_pn = tk.Label(creation, text="Телефонный номер")
    e_pn = tk.Entry(creation)
    l_pn.grid(row=7, column=0, sticky='w', padx=2)
    e_pn.grid(row=7, column=1, sticky='w', padx=2)

    l_em = tk.Label(creation, text="e-mail")
    e_em = tk.Entry(creation)
    l_em.grid(row=9, column=0, sticky='w', padx=2)
    e_em.grid(row=9, column=1, sticky='w', padx=2)

    l_pc = tk.Label(creation, text="СНИЛС")
    e_pc = tk.Entry(creation)
    l_pc.grid(row=8, column=0, sticky='w', padx=2)
    e_pc.grid(row=8, column=1, sticky='w', padx=2)

    b_commit = tk.Button(creation, text = "Сохранить", command = lambda: commit(e_fn, e_sn, e_mn, cb_gen, e_birth, cb_ms, e_addr_c, e_addr_st, e_addr_h, e_addr_f, e_pn, e_em, e_pc, sign, id))
    b_commit.grid(row = 0, column =2, sticky = 'w', padx=2, pady=2)


