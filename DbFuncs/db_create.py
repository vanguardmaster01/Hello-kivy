import sqlite3
import datetime

import os
import sys

script_dir = os.path.dirname( __file__ )
utils_dir = os.path.join( script_dir, '..', 'config' )
sys.path.append(utils_dir)
import utils


# create product table
def create_table_if_not_exists():
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		create_product_table_query = '''CREATE TABLE IF NOT EXISTS products (
									id INTEGER PRIMARY KEY AUTOINCREMENT, 
									name TEXT NOT NULL,
									image BLOB NOT NULL, 
									count INTEGER NOT NULL,
									price REAL NOT NULL,
									modifiedAt timestamp							
									)'''

		# Create a users table
		cursor.execute(create_product_table_query)

		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("fail", error)
	finally:
		if conn:
			conn.close()
			print('connection is closed')

def insertData(name, avatar, modifiedAt):
	try:
		# Connect to the database (create a new file if it doesn't exist)
		conn = sqlite3.connect(utils.dbPath)

		# Create a cursor object to execute SQL commands
		cursor = conn.cursor()

		# #drop table
		# cursor.execute('drop table if exists clients')
		# print('dropped successfully')

		create_user_table_query = '''CREATE TABLE IF NOT EXISTS clients (
									id INTEGER PRIMARY KEY AUTOINCREMENT, 
									name TEXT NOT NULL,
									avatar BLOB NOT NULL, 
									modifiedAt timestamp							
									)'''

		# Create a users table
		cursor.execute(create_user_table_query)

		print('Created successfully')

		# cursor.execute("PRAGMA table_info('clients')")
		# columns = cursor.fetchall()
		# print(columns)

		# Insert User into table
		insert_user_query = """insert into clients (name, avatar, modifiedAt) 
								values (?, ?, ?)"""
		avatarBlog = convertToBlobData(avatar)
		insert_data = (name, avatarBlog, modifiedAt)
		cursor.execute(insert_user_query, insert_data)
		print('inserted successfully')

		# Get All Users
		get_all_users_query = '''select id, name from clients'''
		cursor.execute(get_all_users_query)
		records = cursor.fetchall()

		print(records)

						
		# Commit the changes and close the connection
		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("fail", error)
	finally:
		if conn:
			conn.close()
			print('connection is closed')

# insertData("Smith", "D:\Workspace\Python\Kivy\Hello-kivy\img/1-1.png", datetime.datetime.now())