import requests


def get_user():
    api_url = 'http://ec2-13-48-96-215.eu-north-1.compute.amazonaws.com/api/users'
    headers = {
        'Authorization': 'Bearer C6efvByQWTLM8DTlyImyv_tL7aPVAVLvISzI_1ssvJo',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("User data fetched successfully:")
            # for user in data:
            #     print(user)
            return data
        else:
            print(f"Failed to fetch user data. Status code: {
                  response.status_code}, Error: {response.text}")
    except Exception as e:
        print("An error occurred:", e)
