import requests
from datetime import datetime, timedelta
import pytz

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


def get_user_data(userinfo):
    query = """
    query UserContestRanking($username: String!) {
        userContestRanking(username: $username) {
            rating
            globalRanking
            attendedContestsCount
        }
        matchedUser(username: $username) {
            submitStats {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """
    username = userinfo.get('leetcode_id', '')
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
                    userinfo['rating'] = int(rating)

                if 'globalRanking' in user_contest_ranking:
                    global_ranking = user_contest_ranking.get(
                        'globalRanking', -1)
                    userinfo['global_rank'] = global_ranking

                if 'attendedContestsCount' in user_contest_ranking:
                    contests_participated = user_contest_ranking.get(
                        'attendedContestsCount', -1)
                    userinfo['number_of_contests'] = contests_participated

            ac_submission_num_list = matched_user.get(
                'submitStats', {}).get('acSubmissionNum', [])
            total_problems_solved = 0
            for item in ac_submission_num_list:
                if item.get('difficulty') == 'All':
                    total_problems_solved = item.get('count', 0)
                    break
            userinfo['number_of_questions'] = total_problems_solved
    except Exception as e:
        print(f"An error occurred while processing contest data: {e}")

    return userinfo


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
    
    # last_24_hours_timestamp = int(
    #     (datetime.now() - timedelta(hours=24)).timestamp())
    data = make_graphql_request(query_submission, variables)

    if data:
        ac_submissions = data.get('data', {}).get('recentAcSubmissionList', [])
        leetcode_submissions = []
        for submission in ac_submissions:
            # if int(submission.get('timestamp', 0)) >= last_24_hours_timestamp:
            problem_link = f"https://leetcode.com/problems/{submission.get('titleSlug')}/"
            submission_link = f"https://leetcode.com{submission.get('url')}"
            submission_time = datetime.fromtimestamp(
                int(submission.get('timestamp')))
            date = submission_time.astimezone(pytz.timezone('Asia/Kolkata'))
            formatted_date = date.isoformat()
            leetcode_submissions.append({
                'platform': 'leetcode',
                'problem_title': submission.get('title'),
                'problem_link': problem_link,
                'submission_id': int(submission.get('id')),
                'submission_url': submission_link,
                'submitted_at': formatted_date
            })
        return leetcode_submissions
    else:
        return []


# print(get_user_data("))
# userinfo = {'id': 'pdk123', 'rating': 1598, 'global_rank': 231234,
#             'number_of_contests': 5, 'number_of_questions': 45, 'user': 'princesharma74'}
# print(get_user_data(userinfo))
# print(get_user_submissions('pdk123'))
