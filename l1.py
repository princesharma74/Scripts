import requests
from datetime import datetime, timedelta

url = 'https://leetcode.com/graphql'


def get_rating(username):
    query = """
    query getUserContestRanking ($username: String!) {
    userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        totalParticipants
        topPercentage
        badge {
            name
        }
    }
    }"""

    variables = {"username": username}

    response = requests.post(
        url, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        data = response.json()
        print(data)


def get_problems_solved(username):
    query_submission = """
    query RecentAcSubmissions($username: String!, $limit: Int) {
        recentAcSubmissionList(username: $username, limit: $limit) {
            id
            status
            timestamp
            url
            titleSlug
            title
        }
    }
    """

    variables = {'username': 'ShivamBedar', 'limit': 20}

    problems_leetcode = []
    last_24_hours_timestamp = int(
        (datetime.now() - timedelta(hours=24)).timestamp())
    # print(last_24_hours_timestamp)
    response = requests.post(
        url, json={'query': query_submission, 'variables': variables})
    if response.status_code == 200:
        data = response.json()
        # print(data)
        ac_submissions = data['data']['recentAcSubmissionList']
        for submission in ac_submissions:
            if (int(submission['timestamp']) >= last_24_hours_timestamp):
                problem_link = f"https://leetcode.com/problems/{submission['titleSlug']}/"
                submission_link = f"https:/leetcode.com/{submission['url']}"
                problems_leetcode.append({'problem_title':  submission['title'], 'problem_link': problem_link,
                                          'submission_link': submission_link, 'submission_id': submission['id']})
        print(problems_leetcode)
    else:
        print("Error fetching data. Status code:", response.status_code)


get_problems_solved("ShivamBedar")
