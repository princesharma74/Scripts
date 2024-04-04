import requests
from datetime import datetime, timedelta


def get_rating(username):
    try:
        response = requests.post(
            'https://codeforces.com/api/user.rating?handle=' + username)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()

        # Extract and print new ratings
        for item in data["result"]:
            print(item["newRating"])
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        # Get the rating of a user on CodeForces


def get_problems_solved(handle, count=20):
    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count={count}"
    problem_codeforces = []
    response = requests.get(url)
    if response.status_code == 200:
        submissions = response.json()['result']
        recent_time = datetime.now() - timedelta(hours=24)

        for submission in submissions:
            creation_time = datetime.fromtimestamp(
                submission['creationTimeSeconds'])
            if creation_time > recent_time and submission['verdict'] == 'OK':
                problem_name = submission['problem']['name']
                problem_url = f"https://codeforces.com/problemset/problem/{submission['problem']['contestId']}/{submission['problem']['index']}"
                submission_url = f"https://codeforces.com/contest/{submission['contestId']}/submission/{submission['id']}"

                problem_codeforces.append(
                    {'problem_code': submission['problem']['contestId'],
                     'problem_link': problem_url,
                     'submission_link': submission_url,
                     'submission_id': submission['id']})

        return problem_codeforces
    else:
        print("Error fetching data from Codeforces API.")
        return None


# Example usage:
handle = 'guptajirock176'
recent_correct_submissions = get_problems_solved(handle)
get_rating(handle)
if recent_correct_submissions:
    print("Recent Correct Submissions:")
    for submission in recent_correct_submissions:
        print(f"Problem Code: {submission['problem_code']}")
        print(f"Problem URL: {submission['problem_link']}")
        print(f"Submission URL: {submission['submission_link']}")
        print(f"submission id: {submission['submission_id']}")
        print()
else:
    print("Failed to retrieve recent correct submissions.")
