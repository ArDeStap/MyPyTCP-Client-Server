import requests

def weatherAPICall(CityName):
    WEATHER_API_KEY = f'https://api.openweathermap.org/data/2.5/weather?q={CityName}&appid=5c995a7ee47c74c508a39c429c298aee&units=metric'
    return WEATHER_API_KEY

def makeGetRequest(RequestLink, body = {}, header = {}):
    responseData = requests.get(RequestLink, headers=header, data=body).json()
    return responseData

def ProcessCommand(TextCommand):

    if 'hello' in TextCommand.decode().lower():
        return "Hello from PYTHON TCP SERVER".encode()
    elif 'exit' in TextCommand.decode().lower():
        return "TCP SERVER KILLED".encode()
    elif 'start' in TextCommand.decode().lower():
        return "TCP SERVER IS STARTED".encode()
    elif 'weather' in TextCommand.decode().lower(): 
        city = 'Набережные Челны'
        WthrData = makeGetRequest(weatherAPICall(city))
        returnString = f'Today in {city} {WthrData['weather'][0]['description']}. temperature is {WthrData['main']['temp']}, feels like a {WthrData['main']['feels_like']}. \nwind speed: {WthrData['wind']['speed']} kmph'
        return returnString.encode()
    else:
        return f"I don't Recognize the command".encode()