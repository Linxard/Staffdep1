import sqlite3

def delete_el(table, id):
    db = sqlite3.connect('staffdep.db')
    cursor = db.cursor()

    table = table.lower()  # Приводим к нижнему регистру

    if table == "employee":
        query = f"DELETE FROM Employee WHERE id_emp={id}"
    elif table == "education":
        query = f"DELETE FROM Education WHERE id_diploma={id}"
    elif table == "family":
        query = f"DELETE FROM Family WHERE id_member={id}"
    elif table == "job":
        query = f"DELETE FROM Job WHERE id_job={id}"
    elif table == "passport":
        query = f"DELETE FROM Passport WHERE id_passport={id}"
    elif table == "salary":
        query = f"DELETE FROM Salary WHERE id_salary={id}"
    elif table == "vacation":
        query = f"DELETE FROM Vacation WHERE id_vacation={id}"

    cursor.execute(query)
    db.commit()



