import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_endpoint = os.getenv('BACKEND_API_URL')

def get_users():
    bearer_token = os.getenv('BEARER_TOKEN')
    api_url = api_endpoint + "/users/paginated"
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    
    users = []
    page = 1
    size = 1  # Adjust as needed or set dynamically

    while True:
        try:
            response = requests.get(f"{api_url}?page={page}&size={size}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                users.extend(data['results'])
                if page >= data['pagination']['totalPages']:
                    break
                page += 1
            else:
                print(f"Failed to fetch user data. Status code: {response.status_code}, Error: {response.text}")
                break
        except Exception as e:
            print("An error occurred:", e)
            break
    
    print("All user data fetched successfully.")
    return users
