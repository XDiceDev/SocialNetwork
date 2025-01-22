import requests

url = "http://127.0.0.1:8000/register/"
data = {"username": "testuser", "password": "12345"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
print(response.json())

#тест регистрации
#В бд появился testuser