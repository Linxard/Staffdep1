import tkinter as tk
import op
import addingemp
import addingedu
import addingfam
import addingjob
import addingpas
import addingsal
import addingvac
import deleting
import report
from tkcalendar import DateEntry, Calendar
import sqlite3
from tkinter import ttk
from tkinter import Toplevel
from tkinter.messagebox import showerror, showwarning, showinfo
    

def delete():
    deleting.delete_el(tables_dict[cb_table.get()], int(id_value))


id_value = None

def create_empl():
    sign = True
    addingemp.create_employee(window, sign, Emp_id)

def edit():
    if cb_table.get() == "Сотрудник":
        sign = False
        addingemp.create_employee(window, sign, id_value)
    if cb_table.get() == "Образование":
        sign =False
        addingedu.create_education(window, Emp_id.get(), sign, id_value)
    if cb_table.get() == "Семья":
        sign = False
        addingfam.create_fam(window, Emp_id.get(), sign, id_value)
    if cb_table.get() == "Работа":
        sign = False
        addingjob.create_job(window, Emp_id.get(),deps_dict, pos_dict, sign, id_value)
    if cb_table.get() == "Паспорт":
        sign = False
        addingpas.create_passport(window, Emp_id.get(), sign, id_value)
    if cb_table.get() == "Зарплата":
        sign = False
        addingsal.create_salary(window, Emp_id.get(), sign, id_value)
    if cb_table.get() == "Отпуск":
        sign = False
        addingvac.create_vacation(window, Emp_id.get(), sign, id_value)

def create_wind():
    if cb_create_el.get() == "Образование":
        print(Emp_id)
        sign = True
        addingedu.create_education(window, Emp_id.get(), sign, id_value)
    elif cb_create_el.get() == "Семья":
        sign = True
        addingfam.create_fam(window, Emp_id.get(), sign, id_value)
    elif cb_create_el.get() == "Работа":
        sign = True
        addingjob.create_job(window, Emp_id.get(), deps_dict, pos_dict, sign, id_value)
    elif cb_create_el.get() == "Паспорт":
        sign = True
        addingpas.create_passport(window, Emp_id.get(), sign, id_value)
    elif cb_create_el.get() == "Зарплата":
        sign = True
        addingsal.create_salary(window, Emp_id.get(), sign, id_value)
    elif cb_create_el.get() == "Отпуск":
        sign = True
        addingvac.create_vacation(window, Emp_id.get(), sign, id_value)
    else:
        showinfo(title = "Выберите таблицу", message = "Выберите таблицу, в которую будет внесена запись")

def create_report():
        report.create_report(window, Emp_id.get())

def search():
    if cb_element_for_search.get() == "ФИО":
        request=e_search.get().split()
        counter = len(request)
        if counter == 3:
            Table.delete(*Table.get_children())
            for row in op.search_in_table_by_fio(tables_dict[cb_table.get()],request[0],request[1],request[2]):
                Table.insert('', tk.END, values=row)
        else:
            showwarning(title="Ошибка ввода", message="Введите ФИО в формате <Фамилия Имя Отчество>")
    elif cb_element_for_search.get() == "Фамилия":
        request=e_search.get()
        Table.delete(*Table.get_children())
        for row in op.search_in_table_by_f(tables_dict[cb_table.get()],request):
            Table.insert('', tk.END, values=row)
    elif cb_element_for_search.get() == "Дата приема на работу":
        header = ['Имя', 'Фамилия', 'Отчество', 'Номер телефона', 'Отдел', 'Должность', 'Дата начала работы']
        op.heading(header, Table)
        request=str(e_search.get())
        request2=str(e_search2.get())
        Table.delete(*Table.get_children())
        for row in op.search_in_table_by_date(request, request2):
            Table.insert('', tk.END, values=row)
    elif cb_element_for_search.get() == "Зарплата":
        header = ['Имя', 'Фамилия', 'Отчество', 'Номер телефона', 'Отдел', 'Должность', 'Зарплата']
        op.heading(header, Table)
        request=int(e_search.get())
        request2=int(e_search2.get())
        Table.delete(*Table.get_children())
        for row in op.search_in_table_by_sal(request, request2):
            Table.insert('', tk.END, values=row)
    elif cb_element_for_search.get() == "Отдел":
        header = ['Имя', 'Фамилия', 'Отчество', 'Номер телефона', 'Отдел', 'Должность']
        op.heading(header, Table)
        request=e_search.get()
        Table.delete(*Table.get_children())
        for row in op.search_in_table_by_dep(request):
            Table.insert('', tk.END, values=row)


##Создание графического интерфейса
global window 
window = tk.Tk()
window.title('Управление базой данных')
window.geometry('870x870')
window.minsize(300,300)


frame_actions = tk.Frame(window, width = 870, height = 100, bg='green')
frame_view = tk.Frame(window, width = 870, heigh = 700, bg = 'blue')

frame_actions.place(relx=0,rely=0, relwidth=1, relheigh=0.125)
frame_view.place(relx=0,rely=0.125, relwidth=1, relheigh=0.875)
tables_dict = {"Сотрудник":"Employee", "Образование":"Education", "Семья":"Family", "Работа":"Job", "Паспорт":"Passport","Зарплата":"Salary","Отпуск":"Vacation"}
tables = ['Сотрудник','Отдел','Образование','Семья','Работа','Паспорт','Должность','Зарплата','Отпуск']
tables_noemp = ['Образование','Семья','Работа','Паспорт','Зарплата','Отпуск']

Emp_id = tk.IntVar()
all_selected_items = tk.IntVar()

def on_table_click(event):
    global id_value
    selected_item = Table.selection()
    if selected_item:
        item_values = Table.item(selected_item)['values']
        if item_values:
            id_value = item_values[0]
    if cb_table.get() == "Сотрудник":
        selected_items = Table.selection()
        if selected_items:
            selected_item = selected_items[0]
            all_selected_items.set(Table.item(selected_item)['values'])
            selected_id = Table.item(selected_item, 'values')[0]
            Emp_id.set(int(selected_id))

Table = ttk.Treeview(frame_view, show ='headings') 
Table.bind("<<TreeviewSelect>>", on_table_click)

searching = ["ФИО", "Фамилия", "Дата приема на работу", "Зарплата", "Отдел"]

cb_table = ttk.Combobox(frame_actions, values = tables, state="readonly", width=15)
b_create_el = ttk.Button(frame_actions, text ="Добавить сотрудника", width=30, command=create_empl)
cb_create_el = ttk.Combobox(frame_actions, values = tables_noemp, state="readonly", width =15)
b_edit_el = ttk.Button(frame_actions, text ="Редактировать запись", width=20, command = edit)
b_del_el = ttk.Button(frame_actions, text ="Удалить запись", width=14, command = delete)
b_add_el = ttk.Button(frame_actions, text = "Добавить запись о сотруднике", width = 30, command = create_wind)
l_search = ttk.Label(frame_actions, text = "Поиск элемента в таблице", width=30, background = "green")
e_search = ttk.Entry(frame_actions, width=30)
b_search = ttk.Button(frame_actions, text = "Найти", width=20, command=search)
#b_search_in_table = ttk.Button(frame_actions, text = "Найти в таблице", width=20, command=search_in_table)
b_create_data = ttk.Button(frame_actions, text ="Создать сводку", width=16, command=create_report)
cb_element_for_search = ttk.Combobox(frame_actions, values = searching, state ="readonly", width = 27)

cb_table.grid(row=0, column=0, sticky='w', padx=10, pady=5)
b_create_el.grid(row=0, column=1, sticky='w', padx=10, pady=5)
cb_create_el.grid(row=1, column=0, sticky ='w', padx=10, pady=5)
b_add_el.grid(row=1, column=1, sticky ='w', padx=10, pady=5)
b_edit_el.grid(row=2, column=1, sticky='w', padx=2, pady=5)
b_del_el.grid(row=2, column=2, sticky='w', padx = 2, pady=5)
b_create_data.grid(row=2, column=0, sticky='w', padx=(2, 0), pady=5)

l_search.grid(row=0, column=8, sticky='w', padx=10)
cb_element_for_search.grid(row=1, column=8, sticky="w", padx=10)
e_search.grid(row=2, column=8, sticky='w', padx=10, pady=(0, 1))
b_search.grid(row=2, column=10, sticky='w', padx=10, pady=2)
e_search2 = ttk.Entry(frame_actions, width =13)
e_search2.grid(row=2, column=9, sticky='w', padx=1, pady=(0, 1))
## Конец создания графического интерфейса

def data_search(event):
    global e_search
    global e_search2
    e_search.destroy()
    e_search2.destroy()
    if cb_element_for_search.get() == "Дата приема на работу":
        e_search = DateEntry(frame_actions, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        e_search.grid(row=2, column=8, sticky='w', padx=2, pady=(0, 1))
        #l_search = ttk.Label(frame_actions, text =" ---- ", width=4, background="green")
        #l_search.grid(row=2, column=9)
        e_search2 = DateEntry(frame_actions, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        e_search2.grid(row=2, column=9, sticky='w', padx=2, pady=(0, 1))
    elif cb_element_for_search.get() == "Зарплата":
        e_search = ttk.Entry(frame_actions, width=13)
        e_search2 = ttk.Entry(frame_actions, width =13)
        e_search.grid(row=2, column=8, sticky='w', padx=1, pady=(0, 1))
        e_search2.grid(row=2, column=9, sticky='w', padx=1, pady=(0, 1))
    else:
        e_search = ttk.Entry(frame_actions, width=30)
        e_search.grid(row=2, column=8, sticky='w', padx=10, pady=(0, 1))
cb_element_for_search.bind("<<ComboboxSelected>>", data_search)
##Заполнение таблицы

emp_heads = ['id_сотрудника', 'Имя','Фамилия','Отчество','Пол','Дата рождения',
'Семейное положение','Адрес','Телефонный номер','Электронная почта','СНИЛС']

dep_heads = ['id_отдела','Название отдела']

edu_heads = ['id_диплома','id_сотрудника','Название института','Факультет','Обучение','Специальность',
'Дата начала обучения','Дата окончания обучения']

fam_heads = ['id_члена семьи','id_сотрудника','Отношения','Имя','Фамилия','Отчество','Дата рождения']

job_heads = ['id_работы','id_сотрудника','Отдел','Должность','Номер приказа','Дата приказа','Дата начала работы']

pas_heads = ['id_паспорта','id_сотрудника','Серия','Номер','Кем выдан','Дата выдачи']

pos_heads = ['id_должности','Должность']

sal_heads = ['id_зарплаты','id_сотрудника','Сумма','Дата начала выплат','Номер приказа','Дата приказа']

vac_heads = ['id_отпуска','id_сотрудника','Тип','Дата начала отпуска','Дата окончания отпуска']



def selected(event):
    Emp_id = 0
    cb_table.delete('')
    if cb_table.get() == 'Сотрудник':
        header = emp_heads
        Table.delete(*Table.get_children())
        op.heading(header, Table)
        for row in op.get_table_data("Employee"):
            Table.insert('', tk.END, values=row)
        Table.column(emp_heads[0], stretch=tk.NO, width=0)
        Table.column(emp_heads.index('id_сотрудника'), stretch=tk.NO, width=0)
    elif cb_table.get() == 'Отдел':
        header = dep_heads
        Table.delete(*Table.get_children())
        op.heading(header, Table)
        for row in op.get_table_data("Department"):
            Table.insert('', tk.END, values=row)
    elif cb_table.get() == 'Образование':
        header = edu_heads
        Table.delete(*Table.get_children())
        op.heading(header, Table)
        for row in op.get_table_data("Education"):
            Table.insert('', tk.END, values=row)
        Table.column(edu_heads[0], stretch=tk.NO, width=0)
        Table.column(edu_heads.index('id_сотрудника'), stretch=tk.NO, width=0)
    elif cb_table.get() == 'Семья':
        header = fam_heads
        Table.delete(*Table.get_children())
        op.heading(header, Table)
        for row in op.get_table_data("Family"):
            Table.insert('', tk.END, values=row)
        Table.column(fam_heads[0], stretch=tk.NO, width=0)
        Table.column(fam_heads.index('id_сотрудника'), stretch=tk.NO, width=0)
    elif cb_table.get() == 'Работа':
        header = job_heads
        Table.delete(*Table.get_children())
        op.heading(header, Table)
        for row in op.get_table_data("Job"):
            Table.insert('', tk.END, values=row)
        Table.column(job_heads[0], stretch=tk.NO, width=0)
        Table.column(job_heads.index('id_сотрудника'), stretch=tk.NO, width=0)
    elif cb_table.get() == 'Паспорт':
        header = pas_heads
        Table.delete(*Table.get_children())
        op.heading(header, Table)
        for row in op.get_table_data("Passport"):
            Table.insert('', tk.END, values=row)
        Table.column(pas_heads[0], stretch=tk.NO, width=0)
        Table.column(pas_heads.index('id_сотрудника'), stretch=tk.NO, width=0)
    elif cb_table.get() == 'Должность':
        header = pos_heads
        Table.delete(*Table.get_children())
        op.heading(header, Table)
        for row in op.get_table_data("Position"):
            Table.insert('', tk.END, values=row)
    elif cb_table.get() == 'Зарплата':
        header = sal_heads
        Table.delete(*Table.get_children())
        op.heading(header, Table)
        for row in op.get_table_data("Salary"):
            Table.insert('', tk.END, values=row)
        Table.column(sal_heads[0], stretch=tk.NO, width=0)
        Table.column(sal_heads.index('id_сотрудника'), stretch=tk.NO, width=0)
    elif cb_table.get() == 'Отпуск':
        header=vac_heads
        Table.delete(*Table.get_children())
        op.heading(header, Table)
        for row in op.get_table_data("Vacation"):
            Table.insert('', tk.END, values=row)
        Table.column(vac_heads[0], stretch=tk.NO, width=0)
        Table.column(vac_heads.index('id_сотрудника'), stretch=tk.NO, width=0)

cb_table.bind("<<ComboboxSelected>>", selected)


scroll_bary = ttk.Scrollbar(frame_view, command = Table.yview)
Table.configure(yscrollcommand=scroll_bary.set)
scroll_bary.pack(side=tk.RIGHT, fill=tk.Y)

scroll_barx = ttk.Scrollbar(orient = "horizontal", command = Table.xview)
Table.configure(xscrollcommand=scroll_barx.set)
scroll_barx.pack(side=tk.BOTTOM, fill=tk.X)

Table.pack(expand=tk.YES, fill=tk.BOTH)

deps_dict = {'suply' : 'Снабжение', 'energ' : 'Энергетика', 'staff' : 'Кадры', 'produc' : 'Производство', 'sales' : 'Сбыт', 'acc' : 'Бухгалтерия'}
pos_dict = {'eng' : 'Инженер', 'main_eng' : 'Главный инженер', 'mngr' : 'Менеджер', 'jan' : 'Уборщик','acc' : 'Бухгалтер'}




##Конец заполнения таблицы

window.mainloop()
