import sqlite3
import datetime
from config import utils

# import os
# import sys

# script_dir = os.path.dirname( __file__ )
# urils_dir = os.path.join( script_dir, '..', 'config' )
# sys.path.append(urils_dir)
# import utils

from model.Product import Product

# insert into product table
def insert_product(product):
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		insert_query = """insert into products (name, image, count, price, modifiedAt)
							values (?, ?, ?, ?, ?)"""

		imageBlob = utils.convert_to_blod_data(product.image)
		data = (product.name, (imageBlob), product.count, product.price, datetime.datetime.now())
		
		cursor.execute(insert_query, data)
		
		print("inserted successfully")
		
		conn.commit()
		cursor.close()

		return True
	except sqlite3.Error as error:
		print('fail', error)
		return False
	finally:
		if conn:
			conn.close()
			print('connection is closed')
		return False

# update product item
def update_product(id, count):
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		update_query = '''update products set count = ? where id = ?'''
		params = (count, id)
		cursor.execute(update_query, params)
		
		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print('fail', error)
	finally:
		if conn:
			conn.close()
			print('connection is closed')

# get all products
def get_products():
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		select_query = '''select id, name, image, count, price from products'''
		cursor.execute(select_query)
		records = cursor.fetchall()
		
		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print('fail', error)
		records = []
	finally:
		if conn:
			conn.close()
			print('connection is closed')

	return records

# get product
def get_product(id):
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		print(f'id: {id}')
		select_query = '''select id, name, image, count, price from products where id = ?'''
		cursor.execute(select_query, (id,))
		record = cursor.fetchone()
		
		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print('fail', error)
		record = None
	finally:
		if conn:
			conn.close()
			print('connection is closed')

	return record
