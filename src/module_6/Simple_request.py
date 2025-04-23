import requests
user_ids = [
"f458007fb54eb38cac35d8d511fd06083ddf015da78fca32da094b128b7071255cf81e6a673d189eadae7c26e68a874013a5085a8c2994facbeb0456bfedc8f5",
"fbcc82d7f8dd19868aafe4e835bce3146bafb3e11c3b579a77edc9a3816281aa50cc5ad694550d3f29b61fb850a8b649100ebc75f11056d82f3493fdd9572af8",
"c8be5c39a159901b9a12d1f4628499430bbb81538daae17220e3e3b131f2ae82f157f80c156ba470b978f0c142c6a094c392e3a6e8d9546a98e5570b71e12bd2",
"f064150faf9a044dbe12b0591d127eeee3ccc2bd7be29350e909145b1083b8aa37e27d718897c98a9f8597dee163dabe2a0e98bbacfc8dbb001b215c220924e6"
]

url = "http://127.0.0.1:8000/predict"
for user_id in user_ids:
    params = {"user_id": user_id}
    print(params)
    try:
        response = requests.post(url, params=params)
        print("Status Code:", response.status_code)
        print("Response:", response.json())
        print("---------")
    except Exception as e:
        print(f"Error with user_id {user_id}: {e}")
try:
    response = requests.get("http://127.0.0.1:8000/metrics")
    print(response.status_code)
    print(response.json())
except Exception as e:
    print("Error in request metrics")