import json
import socket
# from . import Commands
import requests
import time

HOST = '127.0.0.1'
PORT = 65432

def weatherAPICall(CityName):
    WEATHER_API_KEY = f'https://api.openweathermap.org/data/2.5/weather?q={CityName}&appid=5c995a7ee47c74c508a39c429c298aee&units=metric'
    return WEATHER_API_KEY

def makeGetRequest(RequestLink, body = {}, header = {}):
    responseData = requests.get(RequestLink, headers=header, data=body).json()
    return responseData


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    endTCPServer = False

    while True:
        
        if endTCPServer:
            break

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            
            while conn:
                
                data = conn.recv(131072)
                
                if not data:
                    break            

                if 'hello' in data.decode().lower():
                    conn.sendall("Hello from PYTHON TCP SERVER".encode())
                elif 'exit' in data.decode().lower():
                    conn.sendall("TCP SERVER KILLED".encode())
                    time.sleep(0.5)
                    endTCPServer = True
                    break
                elif 'start' in data.decode().lower():
                    conn.sendall("TCP SERVER IS STARTED".encode())
                elif 'weather' in data.decode().lower(): 
                    city = 'Набережные Челны'
                    WthrData = makeGetRequest(weatherAPICall(city))
                    returnString = f'Today in {city} {WthrData['weather'][0]['description']}. temperature is {WthrData['main']['temp']}, feels like a {WthrData['main']['feels_like']}. \nwind speed: {WthrData['wind']['speed']} kmph'
                    conn.sendall(returnString.encode())
                else:
                    try:
                        JasonData = json.loads(data.decode().lower())
                        if JasonData['name']:
                            conn.sendall(f'hello, {JasonData['name']}'.encode())
                    except ValueError as e:
                        conn.sendall(f"I don't Recognize the command, {e}".encode())

            


            


