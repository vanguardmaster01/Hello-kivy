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
from config.utils import lockList, stopWebsocket


hostName = os.environ.get('hostName')
# requestTimeStep = int(os.environ.get('requestTimeStep'))

# def create_connect():
#     ws = create_connection("wss://212.224.86.112:8443")
#     print(ws.recv())
#     print("Sending 'Hello, World'...")
#     ws.send("Hello, World")
#     print("Sent")
#     print("Receiving...")
#     result =  ws.recv()
#     print("Received '%s'" % result)
#     ws.close()

# create_connect()

def send_get_ads_info():
    url = "/api/machine/get_ads_info"
    # Send an HTTP GET request to a URL of your choice
    response = requests.post(hostName + url, verify=False)

    # Check the response status code
    if response.status_code == 200:
        responseData = response.json()   # {status : , message : , details : [{},]}
        adData = responseData['details']
        # params = Ad(0, adData['type'], bytes(adData['content'], 'utf-8'))
        global_ads = []
        db.delete_ads()
        params = Ad(0, adData['type'], base64.b64decode(adData['content']))
        global_ads.append(params)
        db.insert_ads(params)
    else:
        print(f"Request failed with status code: {response.status_code}")


def send_get_machine_info():

    # Send an HTTP GET request to a URL of your choice
    url = "/api/machine/get_machine_info"
    response = requests.post(hostName + url, verify=False)

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

            db.insert_machine(params)
    else:
        print(f"Request failed with status code: {response.status_code}")

def send_get_products_info():
    url = "/api/machine/get_product_info"

    # Send an HTTP GET request to a URL of your choice
    response = requests.post(hostName + url, verify=False)

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
            db.insert_product(params)
    else:
        print(f"Request failed with status code: {response.status_code}")

def send_sell_product():
    url = "api/machine/sell_product"


async def connect_to_server():
    # ssl_context = ssl.create_default_context()
    # ssl_context.load_verify_locations(certifi.where())

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    print("wss thread id", threading.get_native_id())

    try:
        async with websockets.connect('wss://212.224.86.112:8443', ssl = ssl_context) as websocket:
            print('connected')
            sendData = {'action': 'MachineConnect'}
            await websocket.send(json.dumps(sendData))
            
            # Receive data
            response = await websocket.recv()
            responseData = json.loads(response)

            print(f"Received data: {responseData}")

            machineConnectStatus = responseData['status']
            token = responseData['token']

            if machineConnectStatus == 'success':
                while True: 
                    
                    if stopWebsocket:
                        print('http_request_close')
                        break

                    statusData = {
                        'action': "MachineSendStatus",
                        'payload': {
                            'serialno': "123-456-678",
                            'temparature': "XXX",
                            'token': token, 
                        }
                    }
                    await websocket.send(json.dumps(statusData))
                    statusResponse = await websocket.recv()
                    statusResponseData = json.loads(statusResponse)
                    print(f'send_websockrt_every10s')
                    machineGetStatus = statusResponseData['status']
                    machineGetType = statusResponseData['type']
                    
                    if machineGetStatus == 1:
                        lockList[0].acquire()
                        if 'ads' in machineGetType:
                            send_get_ads_info()
                        if 'machine' in machineGetType:
                            send_get_machine_info()
                        if 'product' in machineGetType:
                            send_get_products_info()
                        lockList[0].release()
                
                    time.sleep(600)
            else:
                pass

            if stopWebsocket:
                print('websocket_close')
                await websocket.close()
    except:
        pass
        # global_ads = db.get_ad()
        # global_produts = db.get_products()
        # global_machines = db.get_machines()

# asyncio.get_event_loop().run_until_complete(connect_to_server())