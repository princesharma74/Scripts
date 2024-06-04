from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium_driver import driversetup
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import requests


import re


def get_user_data(driver, userinfo):
    username = userinfo.get('codechef_id', None)
    url = f"https://www.codechef.com/users/{username}"

    response = requests.get(f'https://www.codechef.com/users/{username}')
    if (response.status_code == 404):
        print(f"codechef userdata: username {username} not found")
    try:
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extracting rating
        rating_element = soup.find('div', class_='rating-number')
        if rating_element:
            cf_rating = rating_element.text.strip()
            match = re.search(r'\d+', cf_rating)
            if match:
                userinfo['rating'] = int(match.group())

        # Extracting highest rating
        rating_header = soup.find('div', class_='rating-header text-center')
        if rating_header:
            small_tag = rating_header.find('small')
            if small_tag:
                highest_rating_text = small_tag.text.strip()
                highest_rating_match = re.search(
                    r'Highest Rating (\d+)', highest_rating_text)
                if highest_rating_match:
                    userinfo['highest_rating'] = int(
                        highest_rating_match.group(1))

        # Extracting contests participated
        contests_info = soup.find(
            'div', class_='contest-participated-count')
        if contests_info:
            contests_text = contests_info.text.strip()
            contests_count = contests_text.split(':')[-1].strip()
            if contests_count.isdigit():
                userinfo['number_of_contests'] = int(contests_count)

        # Extracting highest rating, global rank, and country rank
        rank_info = soup.find('div', class_='rating-ranks')
        if rank_info:
            rank_items = rank_info.find_all('strong')
            if len(rank_items) >= 2:
                userinfo['global_rank'] = int(rank_items[0].text.strip())
                userinfo['country_rank'] = int(rank_items[1].text.strip())

        # Extracting total problems solved
        problems_section = soup.find(
            'section', class_='rating-data-section problems-solved')
        if problems_section:
            # Find and process headings within the problems section
            headings = problems_section.find_all('h3')
            userinfo['number_of_questions'] = int(0)
            for heading in headings:
                if 'Total Problems Solved' in heading.text:
                    # print(heading)
                    match = re.search(r'\d+', heading.text)
                    if match:
                        # problem_type = match.group(1).strip()
                        problems_solved = int(match.group())
                        userinfo['number_of_questions'] += problems_solved

    except Exception as e:
        print("An error occurred:", str(e))

    return userinfo


def get_user_submissions(driver, username):
    url = f"https://www.codechef.com/users/{username}"
    response = requests.get(url, allow_redirects=False)

    # Check if the request was redirected
    if response.status_code != 200:  # 302 status code indicates redirection
        redirected_url = response.headers.get('Location')
        if redirected_url == 'https://www.codechef.com/':
            print(f"The username '{username}' does not exist on CodeChef.")
            return []
    max_pages = 3
    codechef_submissions = []
    pattern = r"\d{1,2}\s(sec|min|hour)s?\sago"

    try:
        driver.get(url)
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//table[@class='dataTable']/tbody")))
        page_count = 1

        while True:
            for row in table.find_elements(By.XPATH, ".//tr"):
                tim = row.find_elements(
                    By.XPATH, ".//td")[0].get_attribute("title")
                # print("Time:", tim)
                if re.match(pattern, tim):
                    tim = datetime.now().strftime('%I:%M %p %d/%m/%y')
                    continue
                date = datetime.strptime(
                    tim, '%I:%M %p %d/%m/%y')

                # Set the timezone to 'Asia/Kolkata' (+05:30)
                date = pytz.timezone('Asia/Kolkata').localize(date)
                # Format the datetime
                formatted_date = date.isoformat()
                status = row.find_elements(
                    By.XPATH, ".//td")[2].find_element(By.XPATH, ".//span").get_attribute("title")
                title = row.find_elements(By.XPATH, ".//td")[1].text
                submission_link = row.find_elements(
                    By.XPATH, ".//td")[4].find_element(By.XPATH, ".//a").get_attribute("href")
                # submission_id = submission_link.split('/')[-1]
                # print("Submission Link:", submission_link)

                # if re.match(pattern, tim) and status == "accepted":
                if status == "accepted":
                    problem_link = f"https://www.codechef.com/problems/{title}"
                    # print(submission_link)
                    if (submission_link != None):
                        submission_id = submission_link.split('/')[-1]
                    else:
                        submission_id = 11111111
                        submission_link = "No_Submission_Link_Available"
                    # append dictionary with following items title, problem_link, submission_link, submission_id, 'codechef', username
                    codechef_submissions.append({
                        'platform': 'codechef',
                        'problem_title': title,
                        'problem_link': problem_link,
                        'submission_url': submission_link,
                        'submission_id': int(submission_id),
                        'submitted_at': formatted_date,
                    })
            try:
                next_button = driver.find_element(
                    By.XPATH, './/a[@onclick="onload_getpage_recent_activity_user(\'next\');"]')
            except:
                print("Error: Only one page...")
            if next_button.get_attribute("class") == "disabled" or page_count >= max_pages:
                break

            driver.execute_script("arguments[0].click();", next_button)
            WebDriverWait(driver, 10).until(EC.staleness_of(table))
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//table[@class='dataTable']/tbody")))
            page_count += 1
    except Exception as e:
        print("An error occurred:", str(e))

    return codechef_submissions


# driversetup function is defined in selenium_driver.py
# driver = driversetup()

# usernameInv = "pdk123" // Invalid user
# usernameV = "princesharma74" // Valid user

# print(get_user_submissions(driver, usernameV)) // to check submissions of valid user
# print(get_user_submissions(driver, usernameInv)) // to check submissions of invalid user

# userinfov = {'id': 'princesharma74', 'rating': 3, 'global_rank': 1121,
#           'number_of_contests': 12, 'number_of_questions': 34, 'user': 'princesharma74'}  // Valid userData

# print(get_user_data(driver, userinfoV))  // to check user data of valid user

# userinfoInv = {'id': 'pdk123', 'rating': null, 'global_rank': null,
#         'number_of_contests': null, 'number_of_questions': null, 'user': 'pappu'}  // Invalid userData

# print(get_user_data(driver, userinfoInv))  // to check user data of invalid user

# driver.quit()
