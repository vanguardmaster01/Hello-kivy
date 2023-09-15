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

hostName = 'https://212.224.86.112:8443'

# def create_connect():
#     ws = create_connection("ws://echo.websocket.events/")
#     print(ws.recv())
#     print("Sending 'Hello, World'...")
#     ws.send("Hello, World")
#     print("Sent")
#     print("Receiving...")
#     result =  ws.recv()
#     print("Received '%s'" % result)
#     ws.close()

async def connect_to_server():
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())
    
    async with websockets.connect('wss://212.224.86.112:8443', ssl = ssl_context) as websocket:
        sendData = {'action': 'MachineConnect'}
        await websocket.send(json.dumps(sendData))

        # Receive data
        response = await websocket.recv()
        responseData = json.loads(response)

        print(f"Received: {response}")
        print(f"Received data: {responseData}")

        if responseData['status']:
            while True:
                statusData = {
                    'action': "MachineSendStatus",
                    'payload': {
                        'serialno': "123-456-678",
                        'temparature': "XXX",
                        'token': responseData['token'], 
                    }
                }
                await websocket.send(json.dumps(statusData))
                statusResponse = await websocket.recv()
                statusResponseData = json.loads(statusResponse)

# asyncio.get_event_loop().run_until_complete(connect_to_server())


async def connect_and_send():
    async with websockets.connect('wss://example.com/ws') as websocket:
        await websocket.send("Hello, server!")

# asyncio.get_event_loop().run_until_complete(connect_and_send())

def send_get_machine_info():
    # delete machine table
    db.delete_machines()

    # Send an HTTP GET request to a URL of your choice
    url = "/api/machine/get_machine_info"
    response = requests.post(hostName + url, verify=False)

    # Check the response status code
    if response.status_code == 200:
        responseData = response.json()   # {status : , message : , details : [{},]}
        machineData = responseData['details']
        for item in machineData:
            params = Machine(0, item['name'], item['unit'], item['value'], base64.b64decode(item['thumbnail']))
            db.insert_machine(params)
    else:
        print(f"Request failed with status code: {response.status_code}")

def send_get_ads_info():
    url = "/api/machine/get_ads_info"
    db.delete_ads()
    # Send an HTTP GET request to a URL of your choice
    response = requests.post(hostName + url, verify=False)

    # Check the response status code
    if response.status_code == 200:
        responseData = response.json()   # {status : , message : , details : [{},]}
        adData = responseData['details']
        # params = Ad(0, adData['type'], bytes(adData['content'], 'utf-8'))
        params = Ad(0, adData['type'], base64.b64decode(adData['content']))
        db.insert_ads(params)
    else:
        print(f"Request failed with status code: {response.status_code}")

def send_get_products_info():
    url = "/api/machine/get_product_info"
    # delete machine table
    db.delete_products()

    # Send an HTTP GET request to a URL of your choice
    response = requests.post(hostName + url, verify=False)

    # Check the response status code
    if response.status_code == 200:
        productData = response.json()   # {status : , message : , details : [{},]}
        for item in productData:
            params = Product(0, item['itemno'], item['name'], base64.b64decode(item['thumbnail']), item['nicotine'], item['batterypack'],
                             item['tankvolumn'], item['price'], item['currency'], item['caution'], item['stock'])
            db.insert_product(params)
    else:
        print(f"Request failed with status code: {response.status_code}")

def send_sell_product():
    url = "api/machine/sell_product"


# send_get_machine_info()
# send_get_products_info()
# send_get_ads_info()