# from websocket import create_connection
import requests
import time
import json
import asyncio
import websockets
import certifi
from model.Machine import Machine
from model.Ad import Ad
from model.Product import Product
from DbFuncs import db
import base64
import ssl
import certifi
import os
import threading
from dotenv import load_dotenv
load_dotenv()
from config.global_vars import global_ads, global_machines, global_produts
from config.utils import setThreadStatus, getThreadStatus, THREAD_INIT, THREAD_RUNNING, THREAD_STOPPING, THREAD_FINISHED
from config.utils import getDBLock, DBLOCK_ADS, DBLOCK_MACHINE, DBLOCK_PRODUCT
from websockets.exceptions import ConnectionClosed

hostName = os.environ.get('hostName')
# requestTimeStep = int(os.environ.get('requestTimeStep'))

def send_get_ads_info():
    url = "/api/machine/get_ads_info"
    # Send an HTTP GET request to a URL of your choice
    response = requests.post(hostName + url, verify=False)

    if getThreadStatus() == THREAD_STOPPING:
        return

    # Check the response status code
    if response.status_code == 200:
        responseData = response.json()   # {status : , message : , details : [{},]}
        adData = responseData['details']
        # params = Ad(0, adData['type'], bytes(adData['content'], 'utf-8'))
        global_ads = []
        db.delete_ads()
        params = Ad(0, adData['type'], base64.b64decode(adData['content']))
        global_ads.append(params)
        if getThreadStatus() == THREAD_STOPPING:
            return
        db.insert_ads(params)
    else:
        print(f"Request failed with status code: {response.status_code}")


def send_get_machine_info():

    # Send an HTTP GET request to a URL of your choice
    url = "/api/machine/get_machine_info"
    response = requests.post(hostName + url, verify=False)

    if getThreadStatus() == THREAD_STOPPING:
        return
    
    # Check the response status code
    if response.status_code == 200:
        responseData = response.json()   # {status : , message : , details : [{},]}
        machineData = responseData['details']
        global_machines = []
        # delete machine table
        db.delete_machines()
        for item in machineData:
            params = Machine(0, item['name'], item['unit'], item['value'], base64.b64decode(item['thumbnail']))
    
            global_machines.append(params)

            if getThreadStatus() == THREAD_STOPPING:
                return
            db.insert_machine(params)
    else:
        print(f"Request failed with status code: {response.status_code}")

def send_get_products_info():
    url = "/api/machine/get_product_info"

    # Send an HTTP GET request to a URL of your choice
    response = requests.post(hostName + url, verify=False)
    if getThreadStatus() == THREAD_STOPPING:
        return

    # Check the response status code
    if response.status_code == 200:
        productData = response.json()   # {status : , message : , details : [{},]}
        global_produts = []
        # delete products table
        db.delete_products()
        for item in productData:
            params = Product(0, item['itemno'], item['name'], base64.b64decode(item['thumbnail']), item['nicotine'], item['batterypack'],
                             item['tankvolumn'], item['price'], item['currency'], item['caution'], item['stock'])
            global_produts.append(params)
            if getThreadStatus() == THREAD_STOPPING:
                break
            db.insert_product(params)
    else:
        print(f"Request failed with status code: {response.status_code}")

def send_sell_product():
    url = "api/machine/sell_product"

websocket=None

async def connect_to_server():
    # ssl_context = ssl.create_default_context()
    # ssl_context.load_verify_locations(certifi.where())

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    print("wss thread id", threading.get_native_id())

    setThreadStatus(THREAD_RUNNING)
    
    cnt = 0
    
    try:
        websocket = await websockets.connect('wss://212.224.86.112:8443', ssl = ssl_context)
    except:
        pass
    
    while True: 
        try:
            if getThreadStatus() == THREAD_STOPPING:
                break

            if cnt % 50 != 0:
                time.sleep(0.1)
                cnt = (cnt+1) % 50
                print('cnt', cnt)
                continue
                
            cnt = (cnt+1) % 50
            
            # async with websockets.connect('wss://212.224.86.112:8443', ssl = ssl_context) as websocket:

            if getThreadStatus() == THREAD_STOPPING:
                break
            
            sendData = {'action': 'MachineConnect'}
            await websocket.send(json.dumps(sendData))
            
            if getThreadStatus() == THREAD_STOPPING:
                break
            
            # Receive data
            response = await websocket.recv()
            responseData = json.loads(response)
            print(f"Received data: {responseData}")

            machineConnectStatus = responseData['status']
            token = responseData['token']

            if getThreadStatus() == THREAD_STOPPING:
                break                

            if machineConnectStatus == 'success':
                statusData = {
                    'action': "MachineSendStatus",
                    'payload': {
                        'serialno': "123-456-678",
                        'temparature': "XXX",
                        'token': token, 
                    }
                }
                await websocket.send(json.dumps(statusData))
                if getThreadStatus() == THREAD_STOPPING:
                    break

                statusResponse = await websocket.recv()
                if getThreadStatus() == THREAD_STOPPING:
                    break

                statusResponseData = json.loads(statusResponse)
                print(f'send_websockrt_every10s')
                machineGetStatus = statusResponseData['status']
                machineGetType = statusResponseData['type']

                if getThreadStatus() == THREAD_STOPPING:
                    break
                
                if machineGetStatus == 1:
                    if 'ads' in machineGetType:
                        getDBLock(DBLOCK_ADS).acquire()
                        try:
                            send_get_ads_info()
                        except:
                            pass
                        getDBLock(DBLOCK_ADS).release()
                    if 'machine' in machineGetType:
                        getDBLock(DBLOCK_MACHINE).acquire()
                        try:
                            send_get_machine_info()
                        except:
                            pass
                        getDBLock(DBLOCK_MACHINE).release()
                    if 'product' in machineGetType:
                        getDBLock(DBLOCK_PRODUCT).acquire()
                        try:
                            send_get_products_info()
                        except:
                            pass
                        getDBLock(DBLOCK_PRODUCT).release()
            
        except (ConnectionClosed):
            try:
                websocket = await websockets.connect('wss://212.224.86.112:8443', ssl = ssl_context)
            except:
                pass
            
    try:
        websocket.close()
    except:
        pass

    setThreadStatus(THREAD_FINISHED)

def close_connect():
    pass