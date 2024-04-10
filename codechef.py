from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium_driver import driversetup
import random
from bs4 import BeautifulSoup


def get_user_data(driver, username):
    url = f"https://www.codechef.com/users/{username}"
    user_data = {'rating': 0, 'contests_participated': 0,
                   'highest_rating': 0, 'global_rank': -1, 'country_rank': -1, 'total_problems_solved': 0}
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
                user_data['rating'] = int(match.group())

        # Extracting highest rating
        rating_header = soup.find('div', class_='rating-header text-center')
        if rating_header:
            small_tag = rating_header.find('small')
            if small_tag:
                highest_rating_text = small_tag.text.strip()
                highest_rating_match = re.search(
                    r'Highest Rating (\d+)', highest_rating_text)
                if highest_rating_match:
                    user_data['highest_rating'] = int(
                        highest_rating_match.group(1))

        # Extracting contests participated
        contests_info = soup.find(
            'div', class_='contest-participated-count')
        if contests_info:
            contests_text = contests_info.text.strip()
            contests_count = contests_text.split(':')[-1].strip()
            if contests_count.isdigit():
                user_data['contests_participated'] = int(contests_count)

        # Extracting highest rating, global rank, and country rank
        rank_info = soup.find('div', class_='rating-ranks')
        if rank_info:
            rank_items = rank_info.find_all('strong')
            if len(rank_items) >= 2:
                user_data['global_rank'] = int(rank_items[0].text.strip())
                user_data['country_rank'] = int(rank_items[1].text.strip())
        # Extracting total problems solved
        problems_section = soup.find(
            'section', class_='rating-data-section problems-solved')
        if problems_section:
            # Find the Practice Problems heading
            practice_heading = problems_section.find(
                'h3', text=re.compile(r'Practice Problems \(\d+\):'))
            if practice_heading:
                # Extract the number using regular expression
                match = re.search(r'\((\d+)\)', practice_heading.text)
                if match:
                    total_problems_solved = int(match.group(1))
                    user_data['total_problems_solved'] = total_problems_solved
    except Exception as e:
        print("An error occurred:", str(e))

    return user_data


def get_user_submissions(driver, username):
    url = f"https://www.codechef.com/users/{username}"
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
                status = row.find_elements(
                    By.XPATH, ".//td")[2].find_element(By.XPATH, ".//span").get_attribute("title")
                title = row.find_elements(By.XPATH, ".//td")[1].text
                submission_link = row.find_elements(
                    By.XPATH, ".//td")[4].find_element(By.XPATH, ".//a").get_attribute("href")
                # submission_id = submission_link.split('/')[-1]
                # print("Submission Link:", submission_link)

                if re.match(pattern, tim) and status == "accepted":
                    problem_link = f"https://www.codechef.com/problems/{title}"
                    # print(submission_link)
                    if (submission_link != None):
                        submission_id = submission_link.split('/')[-1]
                    else:
                        submission_id = 11111111
                        submission_link = "No Submission Link Available"
                    # append dictionary with following items title, problem_link, submission_link, submission_id, 'Codechef', username
                    codechef_submissions.append({
                        'platform': 'Codechef',
                        'problem_title': title,
                        'problem_link': problem_link,
                        'submission_url': submission_link,
                        'submission_id': submission_id
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

# print()
