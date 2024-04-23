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

driver = driversetup()
load_dotenv()

platforms = ['codeforces', 'codechef', 'leetcode']


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
    api_endpoint = "https://72zlh1l27i.execute-api.ap-south-1.amazonaws.com/dev/api/"
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
        user_data = {}
        submissions = []
        contest_data = []
        for platform in platforms:
            if platform in user and 'user_id' in user[platform] and user[platform]['user_id'] is not None:
                user_data[platform] = get_user_data(user[platform], platform)
                submissions.extend(user_submissions(
                    user[platform]['user_id'], platform))
                contest_data.extend(get_contest_history(
                    user[platform]['user_id'], platform))
        push_to_api(f'user/{username}/update', user_data, method='PATCH')
        # print(contest_data)
        push_to_api(f'user/{username}/create-rating-changes', contest_data)
        # print(user_data)
        print(f"Data for {username} fetched successfully.")

        push_to_api(f'user/{username}/updatesubmissions', submissions)
        # print(submissions)
        print(f"Submissions for {username} fetched successfully.")


def main():
    users = getUser.get_user()
    run_tasks(users)
    # print(users)
    # print("Getting upcoming contests...")
    # contest_data = upcomingContests.getCodeforcesContests()
    # contest_data.extend(upcomingContests.getCodechefContests())
    # contest_data.extend(upcomingContests.getLeetcodecontests())
    # push_to_api('contests/create', contest_data)
    # contestdata = codeforcesContest.codeforces_contestHistory("aar9av")
    # contestdata.extend(
    #     codechefContest.codechef_contestHistory(driver, "aar9av"))
    # print(contestdata)
    # push_to_api('user/aar9av/create-rating-changes', contestdata)


if __name__ == "__main__":
    main()
