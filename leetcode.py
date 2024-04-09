import requests
from datetime import datetime, timedelta

LEETCODE_API_URL = 'https://leetcode.com/graphql'


def make_graphql_request(query, variables):
    try:
        response = requests.post(LEETCODE_API_URL, json={
                                 'query': query, 'variables': variables})
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error making GraphQL request: {e}")
        return None


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
    }
    """

    variables = {"username": username}
    data = make_graphql_request(query, variables)
    if data:
        # print(data)
        return data.get('data', {}).get('userContestRanking', []).get('rating')


def get_problems_solved(username, limit=20):
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

    variables = {'username': username, 'limit': limit}
    last_24_hours_timestamp = int(
        (datetime.now() - timedelta(hours=24)).timestamp())
    data = make_graphql_request(query_submission, variables)

    if data:
        ac_submissions = data.get('data', {}).get('recentAcSubmissionList', [])
        problems_leetcode = []
        for submission in ac_submissions:
            if int(submission.get('timestamp', 0)) >= last_24_hours_timestamp:
                problem_link = f"https://leetcode.com/problems/{submission.get('titleSlug')}/"
                submission_link = f"https://leetcode.com/{submission.get('url')}"
                problems_leetcode.append({
                    'platform': 'LeetCode',
                    'problem_title': submission.get('title'),
                    'problem_link': problem_link,
                    'submission_id': submission.get('id'),
                    'submission_url': submission_link
                })
        return problems_leetcode