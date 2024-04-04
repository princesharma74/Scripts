import codeforces
import codechef
import leetcode
from selenium_driver import driversetup


'''
codeforces_username = 'guptajirock176'
# create a selenium driver
driver = driversetup()

problems = codeforces.get_problems_solved(driver, codeforces_username)
print(problems)'''

'''
leetcode_username = 'aar9av'
# create a selenium driver
driver = driversetup()
problems = leetcode.get_problems_solved(driver, leetcode_username)
print(problems)
'''

# codechef_username = 'coder_s_176'
# # create a selenium driver
# driver = driversetup()
# problems = codechef.get_problems_solved(driver, codechef_username)
# print(problems)


# for user in users:
#     dummy = {
#         'username': '',
#         'rating': '',
#         'submissions':
#     }
#     user['platform']['codeforces']
driver = driversetup()

users = [
    {
        'username': 'princesharma74',
        'platform': {
            'codeforces': 'princesharma74',
            'codechef': 'princesharma74',
            'leetcode': 'princesharma74',
        }
    },
    {
        'username': 'ShivamBedar23',
        'platform': {
            'codeforces': 'guptajirock176',
            'codechef': 'coder_s_176',
            'leetcode': 'ShivamBedar',
        }
    },
    {
        'username': 'aar9av',
        'platform': {
            'codeforces': 'aar9av',
            'codechef': 'aar9av',
            'leetcode': 'aar9av',
        }
    },
]

# Initialize an empty dictionary to store the final result
final_result = []

# Define a function to get submissions for a user on a specific platform


def get_submissions(username, platform):
    # Initialize an empty list to store submissions
    submissions = []
    # Call the respective function based on the platform
    if platform == 'codeforces':
        submissions = codeforces.get_problems_solved(driver, username)
    elif platform == 'codechef':
        submissions = codechef.get_problems_solved(driver, username)
    # elif platform == 'leetcode':
    #     submissions = leetcode.get_problems_solved(driver, username)
    return submissions

# defining a function to get rating for a user on a specific platform


def get_rating(username, platform):
    if platform == 'codeforces':
        # rating = codeforces.get_rating(driver, username)
        rating = 1600
    if platform == 'codechef':
        rating = codechef.get_rating(driver, username)
    if platform == 'leetcode':
        rating = 1600
    return rating


# Iterate over the users list
for user in users:
    username = user['username']
    platform_data = user['platform']
    # Initialize a dictionary for the current user
    user_dict = {"username": username, "platform": {}}
    # Iterate over the platforms for the current user
    for platform, handle in platform_data.items():
        # Call the function to get submissions for the current platform and user
        submissions = get_submissions(handle, platform)
        rating = get_rating(handle, platform)
        # Append submissions to the user_dict under the respective platform
        user_dict["platform"][platform] = {
            "handle": handle, "submissions": submissions, "rating": rating}
    # Append the user_dict to the final_result
    final_result.append(user_dict)

# Print the final_result
print(final_result)
