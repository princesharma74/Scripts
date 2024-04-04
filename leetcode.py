import time
from bs4 import BeautifulSoup
import requests
import re

url = 'https://leetcode.com/graphql'


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
    }"""

    variables = {"username": username}

    response = requests.post(
        url, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        data = response.json()
        print(data)


def get_problems_solved(username):
    query_submission = """
    query RecentAcSubmissions($username: String!) {
        recentAcSubmissionList(username: $username) {
            id
            status
            timestamp
            url
            titleSlug
            title
        }
    }
"""
    variables = {'username': 'ShivamBedar'}
    response = requests.post(
        url, json={'query': query_submission, 'variables': variables})
    if response.status_code == 200:
        data = response.json()
        print(data)
    # url = f'https://leetcode.com/{username}'
    # problems_leetcode = []
    # driver.get(url)
    # time.sleep(10)

    # soup = BeautifulSoup(driver.page_source, 'html.parser')

    # # Extract the titles of the most recent problems solved
    # div = soup.find_all('div', attrs={'data-title': True})
    # # rating = soup.find
    # for i in div:
    #     children = i.findChildren('span')
    #     pattern = r'^(a\ minute\ ago|a\ few\ seconds\ ago|an\ hour\ ago|\d+\ hours\ ago|\d+\ minutes\ ago)$'
    #     match = re.search(pattern, children[1].text)
    #     # concatenate the link with the base url
    #     if match:
    #         submission_link = f"https://leetcode.com{i.parent['href']}"
    #         problem_link = f"https://leetcode.com/problems/{i['data-title'].lower().replace(' ', '-')}/"
    #         submission_id = i.parent['href'].split('/')[-2]
    #         problems_leetcode.append({'problem_title':  i['data-title'], 'problem_link': problem_link,
    #                                  'submission_link': submission_link, 'submission_id': submission_id})
    #     else:
    #         break

    # return problems_leetcode


get_rating("ShivamBedar")
