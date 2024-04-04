import requests

# GraphQL query
url = "https://leetcode.com/graphql"
query_submission = """
    query RecentAcSubmissions($username: String!, $limit: Int) {
        recentAcSubmissionList(username: $username, limit: $limit) {
            id
            status
            timestamp
            url
            titleSlug
            title
        }
    }
"""

variables = {'username': 'ShivamBedar', 'limit': 1}

response = requests.post(
    url, json={'query': query_submission, 'variables': variables})

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Extract and process the data from the response
    ac_submissions = data['data']['recentAcSubmissionList']
    # Print the extracted data
    for submission in ac_submissions:
        print("Title:", submission['title'])
        print("Title Slug:", submission['titleSlug'])
        print("Timestamp:", submission['timestamp'])
        print("url:", submission['url'])
        print("-" * 50)
else:
    # Print an error message if the request was unsuccessful
    print("Error fetching data. Status code:", response.status_code)
