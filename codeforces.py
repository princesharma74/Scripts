import requests
from datetime import datetime, timedelta


def get_user_data(username):
    user_data = {}
    try:
        response = requests.post(
            'https://codeforces.com/api/user.rating?handle=' + username)
        response.raise_for_status()
        data = response.json()
        user_data = {
            'rating': 0, 'contests_participated': 0, 'total_problems_solved': 0, 'global_rank': -1}
        if data and "result" in data:
            if data["result"]:
                last_item = data["result"][-1]
                rating = last_item["newRating"]
                user_data['rating'] = rating
                total_contests_participated = len(data["result"])
                user_data['contests_participated'] = total_contests_participated
        else:
            print("No data available.")
            return user_data

        user_data['total_problems_solved'] = get_total_problems_solved(
            username)
        return user_data
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return user_data
    except KeyError as ke:
        print("Key error occurred:", ke)
        return user_data


def get_total_problems_solved(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=10000"
    response = requests.get(url)

    if response.status_code == 200:
        submissions = response.json()['result']
        solved_problems = set()  # Using a set to store unique problem identifiers

        for submission in submissions:
            if submission['verdict'] == 'OK':
                problem_id = (
                    submission['problem']['contestId'], submission['problem']['index'])
                solved_problems.add(problem_id)

        total_problems_solved = len(solved_problems)
        return total_problems_solved
    else:
        print("Error fetching data from Codeforces API.")
        return None


def get_user_submissions(handle, count=20):
    # print("Codeforces running")
    url = "https://codeforces.com/api/user.status?handle=" + \
        handle + "&from=1&count=" + str(count)

    codeforces_submissions = []
    response = requests.get(url)

    if response.status_code == 200:
        if 'result' in response.json():
            submissions = response.json()['result']
        else:
            submissions = []
        recent_time = datetime.now() - timedelta(hours=24)

        for submission in submissions:
            if 'creationTimeSeconds' in submission and 'verdict' in submission:
                creation_time = datetime.fromtimestamp(
                    submission['creationTimeSeconds'])
                if creation_time > recent_time and submission['verdict'] == 'OK':
                    problem_name = submission['problem']['name']
                    problem_url = f"https://codeforces.com/problemset/problem/{submission['problem']['contestId']}/{submission['problem']['index']}"
                    submission_url = f"https://codeforces.com/contest/{submission['contestId']}/submission/{submission['id']}"
                    codeforces_submissions.append({
                        'platform': 'Codeforces',
                        'problem_title': problem_name,
                        'problem_link': problem_url,
                        'submission_id': submission['id'],
                        'submission_url': submission_url
                    })
        # print("Codeforces ended")
        return codeforces_submissions
    else:
        print("Error fetching data from Codeforces API.")
        return ''
