import requests

client_id = '46tornai9v'
client_secret = '5bcj2ZdQLOEs9uNzFEOicY9rduIQMbFCmbiYWmjO'

url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
}
params = {"query": '대구 달서구 조암남로32길 20-4'}
response = requests.get(url, headers=headers, params=params)


print(response.json())