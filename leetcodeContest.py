import requests
from datetime import datetime, timedelta, timezone


def leetcode_contestHistory(username):
    query = """
    query userContestRankingHistory($username: String!) {
        userContestRankingHistory(username: $username) {
            attended
            rating
            ranking
            trendDirection
            problemsSolved
            totalProblems
            finishTimeInSeconds
            contest {
                title
                startTime
            }
        }
    }
    """

    url = 'https://leetcode.com/graphql'

    variables = {
        "username": username
    }

    rankingHistory = []

    response = requests.post(
        url, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        data = response.json()

        user_contest_ranking_history = data['data']['userContestRankingHistory']

        if user_contest_ranking_history is None:
            print("No contest history found for the user")
            return rankingHistory

        prevRating = 1500
        for history in user_contest_ranking_history:
            if history['attended']:
                contestinfo = {}
                contestinfo['user'] = username
                contestinfo['rating_change'] = int(
                    (history['rating'])-prevRating)
                prevRating = int(history['rating'])
                contestinfo['final_rating'] = int(history['rating'])
                contestinfo['number_of_problems_solved'] = history['problemsSolved']
                contestinfo['rank'] = history['ranking']
                time = history['contest']['startTime']
                timestamp = int(time)
                datetime_obj = datetime.fromtimestamp(timestamp)
                # Convert the datetime object to the desired format
                formatted_time = datetime_obj.strftime("%Y-%m-%dT%H:%M:%S%z")
                # Adjust the timezone offset
                formatted_time_with_timezone = datetime_obj.astimezone(
                    timezone(timedelta(hours=5, minutes=30))).strftime("%Y-%m-%dT%H:%M:%S%z")

                contestinfo['contest'] = {
                    'title': history['contest']['title'], 'start_time': formatted_time_with_timezone, 'platform': 'Leetcode', 'url': f"https://leetcode.com/contest/{(history['contest']['title']).replace(' ', '-').lower()}", 'duration': '', 'total_questions': 4}
                rankingHistory.append(contestinfo)

    else:
        # Print an error message if the request was unsuccessful
        print("Error fetching data. Status code:", response.status_code)
    return rankingHistory


# usernameV = 'coder_s_176'  # valid username
# checking history for valid username
# contestHistory = leetcode_contestHistory(usernameV)

# print(contestHistory)
# usernameInv = 'shivamBedar'  # invalid username
# # checking history for invalid username
# contestHistory = leetcode_contestHistory(usernameInv)


# print("Contest History:")
# for contest in contestHistory:
#     print(contest)
#     print("\n")
