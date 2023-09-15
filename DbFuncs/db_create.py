import sqlite3
import datetime

import os
import sys

from config import utils


def create_tables():
	create_product_table_if_not_exists()
	create_ads_table_if_not_exists()
	create_machine_table_if_not_exists()

# create product table
def create_product_table_if_not_exists():
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		create_product_table_query = '''CREATE TABLE IF NOT EXISTS products (
									id INTEGER PRIMARY KEY AUTOINCREMENT, 
									itemno TEXT NOT NULL,
									name TEXT NOT NULL,
									thumbnail BLOB NOT NULL, 
									nicotine TEXT NOT NULL,
									batterypack TEXT NOT NULL,
									tankvolumn TEXT NOT NULL,
									price REAL NOT NULL,
									currency TEXT NOT NULL,
									caution TEXT NOT NULL,
									stock INTEGER NOT NULL
									)'''

		# Create a users table
		cursor.execute(create_product_table_query)

		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("product_table_fail", error)
	finally:
		if conn:
			conn.close()
			print('connection is closed')

# create product table
def create_ads_table_if_not_exists():
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		create_ads_table_query = '''CREATE TABLE IF NOT EXISTS ads (
									id INTEGER PRIMARY KEY AUTOINCREMENT, 
									type TEXT NOT NULL,
									content BLOB NOT NULL
									)'''

		# Create a users table
		cursor.execute(create_ads_table_query)

		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("ads_table_fail", error)
	finally:
		if conn:
			conn.close()
			print('connection is closed')

# create product table
def create_machine_table_if_not_exists():
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		create_machine_table_query = '''CREATE TABLE IF NOT EXISTS machines (
									id INTEGER PRIMARY KEY AUTOINCREMENT, 
									name TEXT NOT NULL,
									unit TEXT NOT NULL,
									value TEXT NOT NULL,
									thumbnail BLOB NOT NULL
									)'''

		# Create a users table
		cursor.execute(create_machine_table_query)

		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("machine_table_fail", error)
	finally:
		if conn:
			conn.close()
			print('connection is closed')

