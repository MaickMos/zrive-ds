import requests

url = "http://127.0.0.1:8000/predict"
params = {"user_id": 3768240439428}  # Parámetros de la petición
#"f064150faf9a044dbe12b0591d127eeee3ccc2bd7be29350e909145b1083b8aa37e27d718897c98a9f8597dee163dabe2a0e98bbacfc8dbb001b215c220924e6"

response = requests.post(url, params=params)

print("Status Code:", response.status_code)
print("Response:", response.json())