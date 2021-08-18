import requests
import time
import json
def get_data(service, appid,city):
    while True:
        time.sleep(1)
        url = f'{service}?q={city}&appid={appid}'
        response = requests.get(url)
        if response.status_code == 200:
            print(url)
            break
    return response.json()

appid = 'a4460539c767d93b54b387eca0ae4098'
service = 'https://samples.openweathermap.org/data/2.5/weather'
city = 'Moscow'
response = get_data(service, appid, city)

print('Получен результат')
print(response)

with open('1_2_authorization.json', 'w') as f:
    json_repo = json.dump(response, f)






