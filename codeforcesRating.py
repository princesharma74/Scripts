import requests
# import json

response = requests.post(
    'https://codeforces.com/api/user.rating?handle=guptajirock176')
data = response.json()
# data1 = json.loads(data)
for item in data["result"]:
    print(item["newRating"])
# print(data)
