import requests
from datetime import datetime, timedelta
import bs4


def get_codechef_user_info(handle):
    try:
        response = requests.get(f"https://www.codechef.com/users/{handle}")
        response.raise_for_status()  # Raise error for non-200 status codes

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        user_details_container = soup.select_one('.user-details-container')
        if user_details_container:
            profile = user_details_container.find('img')['src']
            name = user_details_container.find('h2').text.strip()
        else:
            profile = ""
            name = ""

        rating_number = soup.select_one(".rating-number")
        if rating_number:
            current_rating = int(rating_number.text)
        else:
            current_rating = 0

        highest_rating_link = soup.select(".rating-number")[1].find_next('a')
        if highest_rating_link:
            highest_rating = int(highest_rating_link.text.split('Rating')[1])
        else:
            highest_rating = 0

        user_country_flag = soup.select_one('.user-country-flag')
        if user_country_flag:
            country_flag = user_country_flag['src']
        else:
            country_flag = ""

        user_country_name = soup.select_one('.user-country-name')
        if user_country_name:
            country_name = user_country_name.text
        else:
            country_name = ""

        rating_ranks = soup.select('.rating-ranks a')
        if rating_ranks:
            global_rank = int(rating_ranks[0].text)
            country_rank = int(rating_ranks[1].text)
        else:
            global_rank = 0
            country_rank = 0

        stars_element = soup.select_one('.rating')
        if stars_element:
            stars = stars_element.text.strip() or "unrated"
        else:
            stars = "unrated"

        user_data = {
            "name": name,
            "currentRating": current_rating,
            "highestRating": highest_rating,
            "countryFlag": country_flag,
            "countryName": country_name,
            "globalRank": global_rank,
            "countryRank": country_rank,
            "stars": stars
        }

        return user_data

    except requests.exceptions.RequestException as e:
        print("Error fetching CodeChef data:", e)
        return {}


def get_codeforces_rating(username):
    try:
        response = requests.get(
            'https://codeforces.com/api/user.rating?handle=' + username)
        response.raise_for_status()
        data = response.json()

        if 'result' in data and data['result']:
            last_rating = data["result"][-1]["newRating"]
            return last_rating
        else:
            print("No rating data found for user:", username)
            return -1
    except requests.exceptions.RequestException as e:
        print("Error fetching CodeForces rating data:", e)
        return -1


def get_codeforces_problems_solved(handle, count=20):
    try:
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
            return problem_codeforces
        else:
            print("Error fetching data from Codeforces API.")
            return []
    except requests.exceptions.RequestException as e:
        print("Error fetching CodeForces problems data:", e)
        return []


# Example usage:
codechef_handle = "coder_s_176"
codeforces_handle = "guptajirock176"

codechef_info = get_codechef_user_info(codechef_handle)
codeforces_rating = get_codeforces_rating(codeforces_handle)
codeforces_problems_solved = get_codeforces_problems_solved(codeforces_handle)

print("CodeChef Info:", codechef_info)
print("Codeforces Rating:", codeforces_rating)
print("Codeforces Problems Solved:")
for problem in codeforces_problems_solved:
    print(problem)
