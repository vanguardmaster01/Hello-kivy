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
from model.Ad import Ad
from model.Machine import Machine

def insert_ads(ad):
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		insert_query = """insert into ads (type, content)
							values (?, ?)"""

		blodData = utils.convert_to_blod_data(ad.content)
		data = (ad.type, (blodData))
		
		cursor.execute(insert_query, data)
		
		print("inserted ad successfully")
		
		conn.commit()
		cursor.close()

		return True
	except sqlite3.Error as error:
		print('insert_ad_fail', error)
		return False
	finally:
		if conn:
			conn.close()
			print('connection is closed')
		return False

def insert_machine(machine):
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		insert_query = """insert into machines (name, unit, value)
							values (?, ?, ?)"""

		data = (machine.name, machine.unit, machine.value)
		
		cursor.execute(insert_query, data)
		
		print("inserted machine successfully")
		
		conn.commit()
		cursor.close()

		return True
	except sqlite3.Error as error:
		print('insert_machine_fail', error)
		return False
	finally:
		if conn:
			conn.close()
			print('connection is closed')
		return False


# insert into product table
def insert_product(product):
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		insert_query = """insert into products (itemno, name, thumbnail, nicotine, batterypack, tankvolumn, price, currency, caution)
							values (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
		imageBlob = utils.convert_to_blod_data(product.thumbnail)
		data = (product.itemno, product.name, (imageBlob), product.nicotine, product.batterypack, product.tankvolumn, product.price, product.currency, product.caution)
		cursor.execute(insert_query, data)
		
		print("inserted successfully")
		
		conn.commit()
		cursor.close()

		return True
	except sqlite3.Error as error:
		print('insert_prodcut_fail', error)
		return False
	finally:
		if conn:
			conn.close()
			print('connection is closed')
		return False

# update product item
def update_product(id, image, price):
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		update_query = '''update products set thumbnail = ?, price = ? where id = ?'''
		imageBlob = utils.convert_to_blod_data(image)
		params = (imageBlob, price, id)
		cursor.execute(update_query, params)
		
		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print('update_product_fail', error)
	finally:
		if conn:
			conn.close()
			print('connection is closed')

# get all products
def get_products():
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		select_query = '''select * from products'''
		cursor.execute(select_query)
		records = cursor.fetchall()

		products = []
		for record in records:
			product = convert_to_product(record)
			products.append(product)

		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print('get_prodcuts_fail', error)
		records = []
	finally:
		if conn:
			conn.close()
			print('connection is closed')

	return products

# get product
def get_product(id):
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		select_query = '''select * from products where id = ?'''
		cursor.execute(select_query, (id,))
		record = cursor.fetchone()
		
		product = convert_to_product(record)

		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print('get_prodcut_fail', error)
		record = None
	finally:
		if conn:
			conn.close()
			print('connection is closed')

	return product

# get Ad
def get_ad():
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		select_query = '''select * from ads'''
		cursor.execute(select_query)
		record = cursor.fetchone()

		ad = convert_to_ad(record)
		print(f'len(ad):{ad.type}')
		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print('get_ad_fail', error)
		ad = None
	finally:
		if conn:
			conn.close()
			print('connection is closed')

	return ad

# get Ad
def get_ad_row(id):
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		select_query = '''select * from ads where id = ?'''
		cursor.execute(select_query, (id,))
		record = cursor.fetchone()

		ad = convert_to_ad(record)

		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print('get_ad_fail', error)
		ad = None
	finally:
		if conn:
			conn.close()
			print('connection is closed')

	return ad


# get Ad
def get_machine(id):
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		select_query = '''select * from machines where id = ?'''
		cursor.execute(select_query, (id,))
		record = cursor.fetchone()
		
		machine = convert_to_machine(record)

		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print('get_machine_fail', error)
		machine = None
	finally:
		if conn:
			conn.close()
			print('connection is closed')

	return machine

def get_product_count():
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		select_query = '''select count(id) from products '''
		cursor.execute(select_query)
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

	return record[0]	

# delete Machines
def delete_machines():
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		delete_query = '''delete from machines'''
		cursor.execute(delete_query)
		
		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print('delete_machine_fail', error)
	finally:
		if conn:
			conn.close()
			print('connection is closed')

# delete Ads
def delete_ads():
	try:
		conn = sqlite3.connect(utils.dbPath)
		cursor = conn.cursor()

		delete_query = '''delete from ads'''
		cursor.execute(delete_query)
		
		conn.commit()
		cursor.close()

	except sqlite3.Error as error:
		print('delete_ads_fail', error)
	finally:
		if conn:
			conn.close()
			print('connection is closed')

def convert_to_product(record):
	product = Product(record[0], record[1], record[2], record[3], record[4], 
				   record[5], record[6], record[7], record[8], record[9])

	return product

def convert_to_ad(record):
	ad = Ad(record[0], record[1], record[2])
	return ad
	
def convert_to_machine(record):
	machine = Machine(record[0], record[1], record[2], record[3])
	return machine

