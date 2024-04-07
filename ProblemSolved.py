import requests
from collections import Counter
from datetime import datetime

url = 'https://leetcode.com/graphql'


def get_problems_solved(username):
    query_submission = """
    query getRecentSubmissions($username: String!, $limit: Int) {
        recentSubmissionList(username: $username, limit: $limit) {
            timestamp
        }
    }
    """

    variables = {'username': username, 'limit': 10}

    response = requests.post(
        url, json={'query': query_submission, 'variables': variables})

    if response.status_code == 200:
        data = response.json()
        recent_submissions = data['data']['recentSubmissionList']

        # Extracting submission dates
        submission_dates = [datetime.fromtimestamp(
            int(sub['timestamp'])).strftime('%Y-%m-%d') for sub in recent_submissions]
        print(submission_dates)
        # Counting submissions per month and per day
        month_count = Counter([date[:7] for date in submission_dates])
        day_count = Counter(submission_dates)

        # Finding the most active month and day
        most_active_month = max(month_count, key=month_count.get)
        most_active_day = max(day_count, key=day_count.get)

        print("Most active month:", most_active_month)
        print("Number of submissions in the most active month:",
              month_count[most_active_month])
        print("Most active day:", most_active_day)
        print("Number of submissions in the most active day:",
              day_count[most_active_day])

    else:
        print("Error fetching data. Status code:", response.status_code)


get_problems_solved("ShivamBedar")
