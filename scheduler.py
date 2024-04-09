import requests
import codechef
import getUser
from selenium_driver import driversetup
import l1
import cf
driver = driversetup()
# users = [
# {
#     'username': 'ShivamBedar23',
#     'platform': {
#         'codeforces': 'guptajirock176',
#         'codechef': 'coder_s_176',
#         'leetcode': 'ShivamBedar',
#     }
# },
#     {
#         'username': 'princesharma74',
#         'platform': {
#             'codeforces': 'princesharma74',
#             'codechef': 'princesharma74',
#             'leetcode': 'princesharma74',
#         }
#     },
# ]

# Function to get submissions for a user from different platforms


def get_submissions(username, platform):
    print(f"Getting submissions for {platform}...")
    submissions = []
    if platform == 'codeforces':
        submissions = cf.get_problems_solved(username)
    elif platform == 'codechef':
        submissions = codechef.get_problems_solved(driver, username)
    elif platform == 'leetcode':
        submissions = l1.get_problems_solved(username)
    return submissions

# Function to get rating for a user from different platforms


def get_rating(username, platform):
    print(f"Getting rating for {platform}...")
    if platform == 'codeforces':
        rating = cf.get_rating(username)
    elif platform == 'codechef':
        rating = codechef.get_rating(driver, username)
    elif platform == 'leetcode':
        rating = l1.get_rating(username)
    return rating

# Function to push data to the API endpoint


def push_submissions_to_api(data, username):
    api_url = f'http://ec2-13-48-96-215.eu-north-1.compute.amazonaws.com/api/user/{
        username}/updatesubmissions'
    headers = {
        'Authorization': 'Bearer C6efvByQWTLM8DTlyImyv_tL7aPVAVLvISzI_1ssvJo',
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 200:
        print("Data pushed successfully.")
    else:
        print(f"Failed to push data. Status code: {
              response.status_code}, Error: {response.text}")

# function to push rating to the API endpoint


def push_rating_to_api(data, username):
    api_url = f'http://ec2-13-48-96-215.eu-north-1.compute.amazonaws.com/api/user/{
        username}/update'
    headers = {
        'Authorization': 'Bearer C6efvByQWTLM8DTlyImyv_tL7aPVAVLvISzI_1ssvJo',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.patch(api_url, json=data, headers=headers)
        if response.status_code == 200:
            print("Data pushed successfully.")
        else:
            print(f"Failed to push data. Status code: {
                  response.status_code}, Error: {response.text}")
    except Exception as e:
        print("An error occurred:", e)  # Function to run tasks


def run_tasks():
    users = getUser.get_user()
    print("Running tasks...")
    final_rating = []
    for user in users:
        username = user['username']
        codechef_id = user['codechef_id']
        codeforces_id = user['codeforces_id']
        leetcode_id = user['leetcode_id']
        rating_data = {}
        submission_data = []
        rating_data['email'] = user['email']
        rating_data['first_name'] = user['first_name']
        rating_data['last_name'] = user['last_name']
        rating_data['codeforces_rating'] = int(get_rating(
            codeforces_id, 'codeforces'))
        rating_data['codechef_rating'] = int(
            get_rating(codechef_id, 'codechef'))
        rating_data['leetcode_rating'] = int(
            get_rating(leetcode_id, 'leetcode'))
        push_rating_to_api(rating_data, username)
        leetcode_submission = get_submissions(leetcode_id, 'leetcode')
        codeforces_submission = get_submissions(codeforces_id, 'codeforces')
        codechef_submission = get_submissions(codechef_id, 'codechef')
        for submission in leetcode_submission:
            submission_data.append(submission)
        for submission in codeforces_submission:
            submission_data.append(submission)
        for submission in codechef_submission:
            submission_data.append(submission)
        push_submissions_to_api(submission_data, username)
        print(submission_data)
    # print(rating_data)
    # temp = {'email': 'guptajirock176@gmail.com', 'first_name': 'Shivam', 'last_name': 'Gupta',
    #         'codeforces_rating': 1081, 'codechef_rating': '1810', 'leetcode_rating': 1848}
    # Push data to API
    # push_submissions_to_api(final_result)
    # username = 'coder_s_176'
    # push_rating_to_api(temp, username)


# Execute tasks
# run_tasks()

# data = [
# 	{
# 		"platform": "Codeforces", 
# 		"problem_title": "New Problem", 
# 		"problem_link": "https://www.codeforces.com/new-problem", 
# 		"submission_id": "121", 
# 		"submission_url": "https://www.codeforces.com/user/princesharma74/23243"
# 	},	
# 	{
# 		"platform": "Codechef", 
# 		"problem_title": "New ", 
# 		"problem_link": "https://www.codeforces.com/new-problem1", 
# 		"submission_id": "12133", 
# 		"submission_url": "https://www.codeforces.com/user/princesharma74/23243"
# 	}
# ]	
# push_submissions_to_api(data, 'coder_s_176')
