from websocket import create_connection
import requests
import time

def create_connect():
    ws = create_connection("ws://echo.websocket.events/")
    print(ws.recv())
    print("Sending 'Hello, World'...")
    ws.send("Hello, World")
    print("Sent")
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)
    ws.close()

def send_vending_status():
    while True:
        # Send an HTTP GET request to a URL of your choice
        url = "https://example.com"  # Replace with the URL you want to request
        response = requests.get(url)

        # Check the response status code
        if response.status_code == 200:
            print("Request successful.")
        else:
            print(f"Request failed with status code: {response.status_code}")

        # Wait for 5 seconds before sending the next request
        time.sleep(5)