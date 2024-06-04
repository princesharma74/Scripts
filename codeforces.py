import requests
from datetime import datetime, timedelta
import pytz
from bs4 import BeautifulSoup


def get_user_data(userinfo):
    username = userinfo.get('codeforces_id')
    response = requests.get(
        f'https://codeforces.com/contests/with/{username}', allow_redirects=False)

    if (response.status_code != 200):
        print(f"codeforces userdata: user {username} not found")
    try:
        response = requests.post(
            'https://codeforces.com/api/user.rating?handle=' + username)
        response.raise_for_status()
        data = response.json()
        if data and "result" in data:
            if data["result"]:
                last_item = data.get('result')[-1]
                rating = last_item.get("newRating")
                userinfo['rating'] = rating
                total_contests_participated = len(data.get("result"))
                userinfo['number_of_contests'] = total_contests_participated
        else:
            print("No data available.")

        userinfo['number_of_questions'] = get_total_problems_solved(
            username)
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
    except KeyError as ke:
        print("Key error occurred:", ke)
    return userinfo


def get_total_problems_solved(username):
    url = f"https://codeforces.com/profile/{username}"
    response = requests.get(url)
    response.raise_for_status()
    if (response.status_code != 200):
        print(f"codeforces getTotalProblemSolved: user {username} not found")
        return 0
    soup = BeautifulSoup(response.text, 'html.parser')
    problems_solved_div = soup.find(
        'div', class_='_UserActivityFrame_counterValue')
    total_problems_solved_text = problems_solved_div.text.strip()
    total_problems_solved = int(total_problems_solved_text.split()[0])
    return total_problems_solved


def get_user_submissions(handle, count=100):

    url = "https://codeforces.com/api/user.status?handle=" + \
        handle + "&from=1&count=" + str(count)
    response = requests.get(url)
    if (response.status_code != 200):
        print(f"codeforces userSubmission: user {handle} not found")
        return []
    codeforces_submissions = []
    response = requests.get(url)
    response.raise_for_status()
    submissions = response.json().get('result', [])

    if submissions:
        for submission in submissions:
            if 'creationTimeSeconds' in submission and 'verdict' in submission:
                creation_time = submission['creationTimeSeconds']
                date = datetime.fromtimestamp(
                    creation_time, pytz.timezone('Asia/Kolkata'))
                # Format the datetime
                formatted_date = date.isoformat()
                # if creation_time > recent_time and submission['verdict'] == 'OK':
                if submission['verdict'] == 'OK':
                    problem_name = submission.get('problem').get('name')
                    problem_url = f"https://codeforces.com/problemset/problem/{submission.get('problem').get('contestId')}/{submission.get('problem').get('index')}"
                    submission_url = f"https://codeforces.com/contest/{submission.get('contestId')}/submission/{submission.get('id')}"
                    codeforces_submissions.append({
                        'platform': 'codeforces',
                        'problem_title': problem_name,
                        'problem_link': problem_url,
                        'submission_id': int(submission.get('id')),
                        'submission_url': submission_url,
                        'submitted_at': formatted_date
                    })
        # print("codeforces ended")
        return codeforces_submissions
    else:
        print("Error fetching data from codeforces API.")
        return ''


# print(get_user_submissions('PDK123'))

# userinfo = {'id': 'princesharma74', 'rating': 324, 'global_rank': 22323,
#             'number_of_contests': 2, 'number_of_questions': 233, 'user': 'princesharma74'}
# print(get_user_data(userinfo))
