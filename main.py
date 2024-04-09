import requests
from selenium_driver import driversetup
import codeforces
import codechef
import leetcode
import getUser

driver = driversetup()


def get_submissions(username, platform):
    print(f"Getting submissions for {platform}...")
    if platform == 'codeforces':
        return codeforces.get_problems_solved(username)
    elif platform == 'codechef':
        return codechef.get_problems_solved(driver, username)
    elif platform == 'leetcode':
        return leetcode.get_problems_solved(username)


def get_rating(username, platform):
    print(f"Getting rating for {platform}...")
    if platform == 'codeforces':
        return codeforces.get_rating(username)
    elif platform == 'codechef':
        return codechef.get_rating(driver, username)
    elif platform == 'leetcode':
        return leetcode.get_rating(username)


def push_to_api(endpoint, data, method='POST'):
    api_url = f'http://ec2-13-48-96-215.eu-north-1.compute.amazonaws.com/api/{
        endpoint}'
    headers = {
        'Authorization': 'Bearer C6efvByQWTLM8DTlyImyv_tL7aPVAVLvISzI_1ssvJo',
        'Content-Type': 'application/json'
    }
    try:
        if method.upper() == 'POST':
            response = requests.post(api_url, json=data, headers=headers)
        elif method.upper() == 'PATCH':
            response = requests.patch(api_url, json=data, headers=headers)
        response.raise_for_status()
        print("Data pushed successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to push data. Error: {e}")


def run_tasks(users):
    print("Running tasks...")
    for user in users:
        username = user['username']
        codechef_id = user['codechef_id']
        codeforces_id = user['codeforces_id']
        leetcode_id = user['leetcode_id']

        rating_data = {
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'codeforces_rating': int(get_rating(codeforces_id, 'codeforces')),
            'codechef_rating': int(get_rating(codechef_id, 'codechef')),
            'leetcode_rating': int(get_rating(leetcode_id, 'leetcode'))
        }
        push_to_api(f'user/{username}/update', rating_data, method='PATCH')

        submissions = []
        for platform in ['leetcode', 'codeforces', 'codechef']:
            submissions.extend(get_submissions(user[platform+'_id'], platform))

        push_to_api(f'user/{username}/updatesubmissions', submissions)


def main():
    users = getUser.get_user()
    run_tasks(users)


if __name__ == "__main__":
    main()
