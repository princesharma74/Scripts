import codechef
import l1
import cf
from selenium_driver import driversetup
import schedule
import time

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


# Define a function to perform the tasks you want to run every 2 minutes
def run_tasks():
    print("Running tasks...")
    # Initialize the Selenium driver
    driver = driversetup()

    final_result = []

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

    def get_rating(username, platform):
        print(f"Getting rating for {platform}...")
        if platform == 'codeforces':
            rating = cf.get_rating(username)
        if platform == 'codechef':
            rating = codechef.get_rating(driver, username)
        if platform == 'leetcode':
            rating = l1.get_rating(username)
        return rating

    for user in users:
        username = user['username']
        platform_data = user['platform']
        user_dict = {"username": username, "platform": {}}
        for platform, handle in platform_data.items():
            submissions = get_submissions(handle, platform)
            rating = get_rating(handle, platform)
            user_dict["platform"][platform] = {
                "handle": handle, "submissions": submissions, "rating": rating}
        final_result.append(user_dict)

    print(final_result)


# Schedule the tasks to run every 2 minutes
schedule.every(2).minutes.do(run_tasks)

# Keep the script running indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
