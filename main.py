import requests
from selenium_driver import driversetup
import codeforces
import codechef
import leetcode
import getUser
import os
from dotenv import load_dotenv

driver = driversetup()
load_dotenv()


def user_submissions(username, platform):
    print(f"Getting submissions for {platform}...")
    if platform == 'codeforces':
        return codeforces.get_user_submissions(username)
    elif platform == 'codechef':
        return codechef.get_user_submissions(driver, username)
    elif platform == 'leetcode':
        return leetcode.get_user_submissions(username)


def get_user_data(username, platform):
    print(f"Getting rating for {platform}...")
    if platform == 'codeforces':
        return codeforces.get_user_data(username)
    elif platform == 'codechef':
        return codechef.get_user_data(driver, username)
    elif platform == 'leetcode':
        return leetcode.get_user_data(username)


def push_to_api(endpoint, data, method='POST'):
    bearer_token = os.getenv('BEARER_TOKEN')
    api_endpoint = "http://ec2-13-48-96-215.eu-north-1.compute.amazonaws.com/api/"
    api_url = api_endpoint + endpoint
    headers = {
        'Authorization': f'Bearer {bearer_token}',
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
    for user in users:
        print(f"Running tasks for {user['username']}...")
        username = user['username']
        codechef_id = user['codechef_id']
        codeforces_id = user['codeforces_id']
        leetcode_id = user['leetcode_id']
        user_data = {
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
        }
        cfrating = get_user_data(codeforces_id, 'codeforces')
        ccrating = get_user_data(codechef_id, 'codechef')
        lcrating = get_user_data(leetcode_id, 'leetcode')

        if (cfrating != -1):
            user_data['codeforces_rating'] = cfrating['rating']
            user_data['number_of_codeforces_contests'] = cfrating['contests_participated']
            user_data['number_of_codeforces_questions'] = cfrating['total_problems_solved']
            user_data['global_rank_codeforces'] = cfrating['global_rank']
        if (ccrating != -1):
            user_data['codechef_rating'] = ccrating['rating']
            user_data['number_of_codechef_contests'] = ccrating['contests_participated']
            user_data['number_of_codechef_questions'] = ccrating['total_problems_solved']
            user_data['global_rank_codechef'] = ccrating['global_rank']
        if (lcrating != -1):
            user_data['leetcode_rating'] = lcrating['rating']
            user_data['number_of_leetcode_contests'] = lcrating['contests_participated']
            user_data['number_of_leetcode_questions'] = lcrating['total_problems_solved']
            user_data['global_rank_leetcode'] = lcrating['global_rank']
        push_to_api(f'user/{username}/update', user_data, method='PATCH')

        submissions = []
        for platform in ['leetcode', 'codeforces', 'codechef']:
            submissions.extend(user_submissions(user[platform+'_id'], platform))

        push_to_api(f'user/{username}/updatesubmissions', submissions)


def main():
    users = getUser.get_user()
    run_tasks(users)


if __name__ == "__main__":
    main()
