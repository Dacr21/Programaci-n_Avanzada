# -*- coding: utf-8 -*-
#%%
import sqlite3

datafile = "C:\\Users\\DiegoCR\\Desktop\\2021-02\\Programacion_avanzada_de_computadoras\\Semana_7\\chinook.db"

with sqlite3.connect(datafile) as conn:
    cur = conn.cursor()

    sql = """SELECT employees.FirstName, employees.LastName,SUM(invoices.Total)
            FROM employees
            JOIN customers
            JOIN invoices
            ON employees.EmployeeId = customers.SupportRepid
            AND invoices.CustomerId = customers.CustomerId
            GROUP BY employees.FirstName,employees.LastName
            ORDER BY SUM(invoices.Total) DESC
            LIMIT 1"""

    for item in cur.execute(sql):
        print(item[0], "  ", item[1], item[2])