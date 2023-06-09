import sqlite3
from tabulate import tabulate

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Retrieve table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()

# Iterate over table names and print table contents
for table_name in table_names:
    table_name = table_name[0]
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    rows = cursor.fetchall()

    headers = [description[0] for description in cursor.description]
    print(f"Table: {table_name}")
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print()

cursor.close()
conn.close()
