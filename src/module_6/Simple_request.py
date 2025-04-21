import requests

url = "http://127.0.0.1:8000/predict"
params = {"user_id": 3768240439428}  # Parámetros de la petición

response = requests.post(url, params=params)

print("Status Code:", response.status_code)
print("Response:", response.json())
