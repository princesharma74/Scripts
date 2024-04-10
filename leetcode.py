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


def get_user_data(username):
    query = """
    query GetUserContestRanking($username: String!) {
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
        
        matchedUser(username: $username) {
            username
            submitStats: submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                    submissions
                }
            }
        }
    }
    """
    user_data = {'rating': 0, 'global_rank': -1,
                    'contests_participated': 0, 'total_problems_solved': 0}
    variables = {"username": username}
    data = make_graphql_request(query, variables)

    try:
        if data:
            user_contest_ranking = data.get(
                'data', {}).get('userContestRanking', {})
            matched_user = data.get('data', {}).get('matchedUser', {})

            if user_contest_ranking:
                if 'rating' in user_contest_ranking:
                    rating = user_contest_ranking.get('rating', -1)
                    user_data['rating'] = rating

                if 'globalRanking' in user_contest_ranking:
                    global_ranking = user_contest_ranking.get(
                        'globalRanking', -1)
                    user_data['global_rank'] = global_ranking

                if 'attendedContestsCount' in user_contest_ranking:
                    contests_participated = user_contest_ranking.get(
                        'attendedContestsCount', -1)
                    user_data['contests_participated'] = contests_participated

            ac_submission_num_list = matched_user.get(
                'submitStats', {}).get('acSubmissionNum', [])
            total_problems_solved = 0
            for item in ac_submission_num_list:
                if item.get('difficulty') == 'All':
                    total_problems_solved = item.get('count', 0)
                    break
            user_data['total_problems_solved'] = total_problems_solved
    except Exception as e:
        print(f"An error occurred while processing contest data: {e}")

    return user_data


def get_user_submissions(username, limit=20):
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
        leetcode_submissions = []
        for submission in ac_submissions:
            if int(submission.get('timestamp', 0)) >= last_24_hours_timestamp:
                problem_link = f"https://leetcode.com/problems/{submission.get('titleSlug')}/"
                submission_link = f"https://leetcode.com/{submission.get('url')}"
                leetcode_submissions.append({
                    'platform': 'LeetCode',
                    'problem_title': submission.get('title'),
                    'problem_link': problem_link,
                    'submission_id': submission.get('id'),
                    'submission_url': submission_link
                })
        return leetcode_submissions
    else:
        return []
