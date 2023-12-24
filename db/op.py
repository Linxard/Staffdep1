import sqlite3
import datetime




def get_table_data(table):

    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM '{table}'")

    data = cursor.fetchall()

    return data

def search_in_table_by_fio(table, argument1, argument2, argument3):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    if table == "Employee":
        cursor.execute(f"SELECT * FROM '{table}' WHERE Employee.first_name= '{argument2}'\
               AND Employee.last_name = '{argument1}' AND Employee.middle_name = '{argument3}'")
    else:
        cursor.execute(f"SELECT '{table}'.* FROM '{table}' INNER JOIN Employee ON\
                '{table}'.id_emp = Employee.id_emp WHERE Employee.first_name= '{argument2}'\
               AND Employee.last_name = '{argument1}' AND Employee.middle_name = '{argument3}'")
    data = cursor.fetchall()
    return data

def search_in_table_by_date(argument1, argument2):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT last_name, first_name, middle_name, phone_number, department, position, working_start FROM 'Employee'\
       INNER JOIN Job ON Employee.id_emp = Job.id_emp WHERE Job.working_start > '{argument1}' AND Job.working_start < '{argument2}'")
    data = cursor.fetchall()
    return data


def search_in_table_by_f(table, argument):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    if table == "Employee":
        cursor.execute(f"SELECT * FROM '{table}' WHERE last_name = '{argument}'")
    else:
        cursor.execute(f"SELECT '{table}'.* FROM '{table}' INNER JOIN Employee ON\
                '{table}'.id_emp = Employee.id_emp WHERE Employee.last_name = '{argument}'")
    data = cursor.fetchall()
    return data

def search_in_table_by_sal(argument, argument2):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT last_name, first_name, middle_name, phone_number, department, position, sum FROM Employee\
       LEFT JOIN Job ON Employee.id_emp = Job.id_emp INNER JOIN Salary ON Employee.id_emp = Salary.id_emp WHERE Salary.sum\
      > '{argument}' AND Salary.sum < '{argument2}'")
    data = cursor.fetchall()
    return data

def search_in_table_by_dep(argument):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT last_name, first_name, middle_name, phone_number, department, position FROM Employee\
   INNER JOIN Job ON Employee.id_emp = Job.id_emp WHERE Job.department = '{argument}'")
    data = cursor.fetchall()
    return data


def create_el(table):
    db = sqilite3.connect('staffdep.db')
    cursor = db.cursor()

    cursor.execute(f"")






#def search_int_table(table, argument1, argument2, argument3):
#    db = sqlite3.connect('staffdep.db')
#    cursor = db.cursor()

#    cursor.execute(f"SELECT '{table}'.* FROM '{table}' INNER JOIN Employee ON\
#                '{table}'.id_emp = Employee.id_emp WHERE Employee.first_name= '{argument2}'\
#               AND Employee.last_name = '{argument1}' AND Employee.middle_name = '{argument3}'")
#    data = cursor.fetchall()
#    return data

def get_headers(table):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()

    cursor.execute( f"PRAGMA table_info('{table}') " )
    headers = cursor.fetchall()
    return headers

def heading(heads, Table):
    Table['columns']= heads
    for header in heads:
        Table.heading(header, text=header, anchor='center')
        Table.column(header, anchor='center', stretch=True)
    return Table

def edit_el(table, element):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()
    new_values = [widget.get() for widget in data_widgets.values()]

    query = (f"UPDATE '{table}' SET {', '.join(columns[table])} WHERE {primary_key_column[selected_table]}=?")
    cursor.execute(query, (*new_values, element[0]))

    data = cursor.fetchall()


#    all_data = []
#    with sqlite3.connect('staffdep.db') as db:
 #       db.row_factory=sqlite3.Row
  #      cursor = db.cursor()
   #     query = """ SELECT * FROM Employee """
    #    cursor.execute(query)
     #   all_data = cursor
    #return all_data
