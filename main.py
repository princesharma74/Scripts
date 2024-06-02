import requests
from selenium_driver import driversetup
import codeforces
from datetime import datetime, timedelta
import codechef
import leetcode
import upcomingContests
import leetcodeContest
import codeforcesContest
import codechefContest
import getUser
import os
from dotenv import load_dotenv
import json

driver = driversetup()
load_dotenv()

platforms = ['codeforces', 'codechef', 'leetcode']

api_endpoint = os.getenv('BACKEND_API_URL')

def user_submissions(username, platform):
    print(f"Getting submissions for {platform}...")
    if platform == 'codeforces':
        return codeforces.get_user_submissions(username)
    elif platform == 'codechef':
        return codechef.get_user_submissions(driver, username)
    elif platform == 'leetcode':
        return leetcode.get_user_submissions(username)


def get_user_data(userinfo, platform):
    print(f"Getting rating for {platform}...")
    if platform == 'codeforces':
        return codeforces.get_user_data(userinfo)
    elif platform == 'codechef':
        return codechef.get_user_data(driver, userinfo)
    elif platform == 'leetcode':
        return leetcode.get_user_data(userinfo)


def get_contest_data():
    print("Getting upcoming contests...")
    contest_data = upcomingContests.getCodeforcesContests()
    contest_data.extend(upcomingContests.getCodechefContests())
    contest_data.extend(upcomingContests.getLeetcodecontests())
    return contest_data


def get_contest_history(username, platform):
    print(f"Getting contest history for {platform}...")
    if platform == 'codeforces':
        return codeforcesContest.codeforces_contestHistory(username)
    elif platform == 'codechef':
        return codechefContest.codechef_contestHistory(driver, username)
    elif platform == 'leetcode':
        return leetcodeContest.leetcode_contestHistory(username)


def push_to_api(endpoint, data, method='POST'):
    bearer_token = os.getenv('BEARER_TOKEN')
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
        print(f"Running tasks for [{user['first_name']}] @{user['username']}...")
        username = user['username']
        email = user['email']
        user_data = {}
        submissions = []
        contest_data = []
        platforms = ['codeforces', 'codechef', 'leetcode']
        for platform in platforms:
            if platform in user and f'{platform}_id' in user[platform] and user[platform][f'{platform}_id'] is not None:
                user_data[platform] = get_user_data(user[platform], platform)
                submissions.extend(user_submissions(
                    user[platform][f'{platform}_id'], platform))
                contest_data.extend(get_contest_history(
                    user[platform][f'{platform}_id'], platform))
        # print(json.dumps(contest_data, indent=4))
        push_to_api(f'/users/{email}/update', user_data, method='PATCH')
        # print(contest_data)
        push_to_api(f'/users/{email}/ratingchange/updateAll', contest_data, method='PATCH')
        # print(user_data)
        print(f"Data for {username} fetched successfully.")
        push_to_api(f'/users/{email}/submissions/update', submissions, method='PATCH')
        print(f"Submissions for {username} fetched successfully.")


def main():
    users = getUser.get_user()
    run_tasks(users)
    print("Getting upcoming contests...")
    contest_data = upcomingContests.getCodeforcesContests()
    contest_data.extend(upcomingContests.getCodechefContests())
    contest_data.extend(upcomingContests.getLeetcodecontests())
    # print(json.dumps(contest_data, indent=4))
    push_to_api('/contests/update', contest_data, method='PATCH')
    # contestdata = codeforcesContest.codeforces_contestHistory("aar9av")
    # contestdata.extend(
    #     codechefContest.codechef_contestHistory(driver, "aar9av"))
    # push_to_api('user/aar9av/create-rating-changes', contestdata)


if __name__ == "__main__":
    main()
