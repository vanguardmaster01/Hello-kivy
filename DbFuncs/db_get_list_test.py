import sqlite3
import datetime

import os
import sys

script_dir = os.path.dirname( __file__ )
constants_dir = os.path.join( script_dir, '..', 'config' )
sys.path.append(constants_dir)
import constants

conn = sqlite3.connect(constants.dbPath)
cursor = conn.cursor()

# Get All Users
get_all_users_query = '''select id, name, price from products'''
cursor.execute(get_all_users_query)
records = cursor.fetchall()

print(records)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all the table names
tables = cursor.fetchall()

for table in tables:
    print(table[0])


conn.commit()
cursor.close()
conn.close()
