from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import re


from bs4 import BeautifulSoup


def get_rating(driver, username):
    url = f"https://www.codechef.com/users/{username}"
    rating = None
    try:
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rating_element = soup.find('div', class_='rating-number')
        if rating_element:
            rating = rating_element.text.strip()
    except Exception as e:
        print("An error occurred:", str(e))
    return rating


def get_problems_solved(driver, username):
    url = f"https://www.codechef.com/users/{username}"
    max_pages = 3
    solved_questions = []
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
                submission_id = submission_link.split('/')[-1]
                if re.match(pattern, tim) and status == "accepted":
                    problem_link = f"https://www.codechef.com/problems/{title}"
                    # append dictionary with following items title, problem_link, submission_link, submission_id, 'Codechef', username
                    solved_questions.append({'problem_code': title, 'problem_link': problem_link,
                                            'submission_link': submission_link, 'submission_id': submission_id})
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

    return solved_questions
