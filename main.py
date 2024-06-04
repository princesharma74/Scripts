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

def push_to_api(endpoint, data, chunk_size=5, method='POST'):
    bearer_token = os.getenv('BEARER_TOKEN')
    api_url = api_endpoint + endpoint
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    # If the data is an array, chunk it into smaller pieces
    if isinstance(data, list):
        data_chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    else:
        data_chunks = [data]

    # Push each chunk of data to the API
    for i, chunk in enumerate(data_chunks):
        chunk_size = len(chunk)
        print(f"Processing chunk {i+1}/{len(data_chunks)} of size {chunk_size}...")
        try:
            if method.upper() == 'POST':
                response = requests.post(api_url, json=chunk, headers=headers)
            elif method.upper() == 'PATCH':
                response = requests.patch(api_url, json=chunk, headers=headers)
            response.raise_for_status()
            print("Chunk pushed successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to push chunk. Error: {e}")

def run_tasks(users):
    for user in users:
        print(f"Running tasks for [{user.get('first_name')}] @{user.get('username')}...")
        username = user.get('username')
        email = user.get('email')
        user_data = {}
        submissions = []
        contest_data = []
        platforms = ['codeforces', 'codechef', 'leetcode']
        for platform in platforms:
            platform_data = user.get(platform)
            if platform_data and platform_data.get(f'{platform}_id') is not None:
                platform_id = platform_data[f'{platform}_id']
                user_data[platform] = get_user_data(platform_data, platform)
                submissions.extend(user_submissions(platform_id, platform))
                contest_data.extend(get_contest_history(platform_id, platform))
        # print(json.dumps(contest_data, indent=4))
        user_data['lastUpdatedAt'] = datetime.now().isoformat()[:-3] + 'Z'
        push_to_api(f'/users/{email}/update', user_data, method='PATCH') # no pagination required
        # print(contest_data)
        push_to_api(f'/users/{email}/ratingchange/updateAll', contest_data, method='PATCH') # pagination required
        # print(user_data)
        print(f"Rating changes for {username} pushed successfully.")
        push_to_api(f'/users/{email}/submissions/update', submissions, method='PATCH') # pagination required
        print(f"Submissions for {username} pushed successfully.")



def main():
    users = getUser.get_users()
    run_tasks(users)
    print("Getting upcoming contests...")
    contest_data = upcomingContests.getCodeforcesContests()
    contest_data.extend(upcomingContests.getCodechefContests())
    contest_data.extend(upcomingContests.getLeetcodecontests())
    # print(json.dumps(contest_data, indent=4)) #check
    push_to_api('/contests/update', contest_data, method='PATCH')
    # contestdata = codeforcesContest.codeforces_contestHistory("aar9av")
    # contestdata.extend(
    #     codechefContest.codechef_contestHistory(driver, "aar9av"))
    # push_to_api('user/aar9av/create-rating-changes', contestdata)


if __name__ == "__main__":
    main()
