import requests
import json
from datetime import datetime, timedelta, timezone
import pytz

def getCodeforcesContests():
    response = requests.get("https://codeforces.com/api/contest.list")
    codeforcesContests = []
    if response.status_code == 200:
        jsonResponse = json.loads(response.text)
        contests = jsonResponse.get("result")
        for contest in contests:
            if contest["phase"] == "BEFORE":
                codeforcesContest = {}
                codeforcesContest["platform"] = "codeforces"
                codeforcesContest["title"] = contest.get("name")
                codeforcesContest["url"] = "https://codeforces.com/contests/" + str(contest.get("id"))
                # Convert start time to UTC and format as ISO 8601
                start_time = datetime.fromtimestamp(contest.get("startTimeSeconds"), tz=timezone.utc)
                start_time_iso = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                codeforcesContest["start_time"] = start_time_iso
                codeforcesContest["duration"] = "PT" + str(contest.get("durationSeconds") // 3600).zfill(2) + "H" + str((contest.get("durationSeconds") % 3600) // 60).zfill(2) + "M"
                
                codeforcesContests.append(codeforcesContest)
    return codeforcesContests

def getCodechefContests():
    contest_details = []
    start_date = datetime(2024, 4, 18, tzinfo=timezone.utc)
    start_num = 130
    today = datetime.now(tz=timezone.utc)
    contest_since_start = (today - start_date).days // 7
    current_num = start_num + contest_since_start + 1
    current_date = today + timedelta(days=(2 - today.weekday() + 7) % 7)

    # Find the next Wednesday
    for i in range(5):
        # Generate the contest name
        contest_name = f"Starters {i + current_num}"
        # Generate the contest URL
        contest_url = f"https://www.codechef.com/START{i + current_num}"
        # Calculate the start time (assuming 2:30 PM UTC)
        start_time = current_date.replace(hour=14, minute=30, second=0, microsecond=0)
        # Add 2 hours to the start time for the duration
        end_time = start_time + timedelta(hours=2)
        # Format start time and duration as ISO 8601 strings
        start_time_iso = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        duration_iso = "PT2H"  # Duration is 2 hours
        # Define the total number of questions
        total_questions = 8
        # Create contest details dictionary
        contest_info = {
            "title": contest_name,
            "url": contest_url,
            "platform": "codechef",
            "start_time": start_time_iso,
            "duration": duration_iso,
            "total_questions": total_questions
        }
        # Append contest details to the list
        contest_details.append(contest_info)
        # Move to the next Wednesday for the next iteration
        current_date += timedelta(weeks=1)  # Increment by 1 week

    return contest_details

def generate_leetcode_contests(contest_type, num_days, start_date, contest_num):
    contest_details = []
    current_date = start_date
    for i in range(num_days):
        # Generate the contest name and URL based on contest type
        if contest_type == "weekly":
            start_time = current_date.replace(hour=2, minute=30, second=0, microsecond=0, tzinfo=timezone.utc)
            contest_name = f"Weekly Contest {contest_num + i}"
            contest_url = f"https://leetcode.com/contest/weekly-contest-{contest_num + i}/"

        elif contest_type == "biweekly":
            start_time = current_date.replace(hour=14, minute=30, second=0, microsecond=0, tzinfo=timezone.utc)
            contest_name = f"Biweekly Contest {contest_num + i}"
            contest_url = f"https://leetcode.com/contest/biweekly-contest-{contest_num + i}/"
        else:
            raise ValueError("Invalid contest type. Must be 'weekly' or 'biweekly'.")

        # Add 1.5 hours to the start time for the duration
        end_time = start_time + timedelta(hours=1, minutes=30)
        # Format start time and duration as ISO 8601 strings
        start_time_iso = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        duration_iso = "PT1H30M"  # Duration is 1.5 hours
        # Define the total number of questions
        total_questions = 4
        # Create contest details dictionary
        contest_info = {
            "title": contest_name,
            "url": contest_url,
            "platform": "leetcode",
            "start_time": start_time_iso,
            "duration": duration_iso,
            "total_questions": total_questions
        }
        # Append contest details to the list
        contest_details.append(contest_info)
        # Move to the next contest date for the next iteration
        current_date += timedelta(weeks=2) if contest_type == "biweekly" else timedelta(weeks=1)

    return contest_details


def getLeetcodecontests():
    biweekly_start_date = datetime(2024, 3, 16)
    weekly_start_date = datetime(2024, 3, 3)
    start_weekly_contest_num = 387
    start_biweekly_contest_num = 126
    current_date = datetime.now()

    weekly_contests_since_start = (current_date - weekly_start_date).days / 7
    # print(weekly_contests_since_start)
    biweekly_contests_since_start = (
        current_date - biweekly_start_date).days / 14

    current_weekly_contest_num = start_weekly_contest_num + weekly_contests_since_start+1
    current_biweekly_contest_num = start_biweekly_contest_num + \
        biweekly_contests_since_start+1

    next_weekly_start = current_date + \
        timedelta(days=(7-(current_date - weekly_start_date).days % 7))
    next_biweekly_start = current_date + \
        timedelta(days=(14-(current_date - biweekly_start_date).days % 14))

    weekly_contests = generate_leetcode_contests(
        "weekly", 5, next_weekly_start, int(current_weekly_contest_num))
    biweekly_contests = generate_leetcode_contests(
        "biweekly", 5, next_biweekly_start, int(current_biweekly_contest_num))

    return weekly_contests + biweekly_contests
