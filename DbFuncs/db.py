import sqlite3
import datetime

import os
import sys

script_dir = os.path.dirname( __file__ )
constants_dir = os.path.join( script_dir, '..', 'config' )
sys.path.append(constants_dir)
import constants

from model.Product import Product


# convert image to blob data
def convertToBlobData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

	
# insert into product table
def insertProduct(product):
	try:
		conn = sqlite3.connect(constants.dbPath)
		cursor = conn.cursor()

		insert_query = """insert into products (name, image, count, price, modifiedAt)
							values (?, ?, ?, ?, ?)"""

		imageBlob = convertToBlobData(product.image)
		data = (product.name, imageBlob, product.count, product.price, datetime.datetime.now())
		
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
def updateProduct(id, count):
	try:
		conn = sqlite3.connect(constants.dbPath)
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
def getProducts():
	try:
		conn = sqlite3.connect(constants.dbPath)
		cursor = conn.cursor()

		select_query = '''select id, name, count from products'''
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
