import requests
from datetime import datetime, timedelta


def get_rating(username):
    try:
        response = requests.post(
            'https://codeforces.com/api/user.rating?handle=' + username)
        response.raise_for_status()
        data = response.json()

        last_item = data["result"][-1]
        # print(last_item["newRating"])
        return last_item["newRating"]
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        # Get the rating of a user on CodeForces
        return -1


def get_problems_solved(handle, count=20):
    # print("Codeforces running")
    url = "https://codeforces.com/api/user.status?handle=" + \
        handle + "&from=1&count=" + str(count)

    problem_codeforces = []
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
                    problem_codeforces.append({
                        'platform': 'Codeforces',
                        'problem_title': problem_name,
                        'problem_link': problem_url,
                        'submission_id': submission['id'],
                        'submission_url': submission_url
                    })
        # print("Codeforces ended")
        return problem_codeforces
    else:
        print("Error fetching data from Codeforces API.")
        return ''
