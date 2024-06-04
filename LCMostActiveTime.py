import requests
import datetime
import json

# Replace these with your actual LeetCode username and session cookie
username = "shivamanandbansal"

# GraphQL query to fetch user's most active day and month
query = """
query getUserProfileCalendar($username: String!) {
  matchedUser(username: $username) {
    userCalendar(year: 2023) {
      submissionCalendar
    }
  }
}
"""

# URL for the LeetCode GraphQL API endpoint
url = "https://leetcode.com/graphql"

# Define the variables for the GraphQL query
variables = {'username': username}

# Make the POST request to the GraphQL API
response = requests.post(url, json={'query': query, 'variables': variables})

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Extract the submission calendar
    submission_calendar_str = data.get('data', {}).get('matchedUser', {}).get('userCalendar', {}).get('submissionCalendar', '{}')
    # Parse the submission calendar string to a dictionary
    submission_calendar = json.loads(submission_calendar_str)
    # Convert the submission calendar to a list of (timestamp, submission count) tuples
    submission_list = [(int(timestamp), count) for timestamp, count in submission_calendar.items()]
    # Find the timestamp corresponding to the maximum submission count
    max_timestamp = None
    max_count = 0
    for timestamp, count in submission_list:
        if count > max_count:
            max_count = count
            max_timestamp = timestamp
    if max_timestamp is not None:
        max_date = datetime.datetime.fromtimestamp(max_timestamp)
        # Print the result
        print("Timestamp with maximum submission count:", max_date)
        print("Maximum submission count:", max_count)
    else:
        print("No data found in submission list.")
else:
    print("Failed to fetch data. Status code:", response.status_code)
