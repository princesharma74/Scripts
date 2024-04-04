import requests

# GraphQL query
query = """
{
  matchedUser(username: "ShivamBedar") {
    username
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }
  }
}
"""

# GraphQL endpoint
url = 'https://leetcode.com/graphql'

# Make the POST request to the GraphQL API
response = requests.post(url, json={'query': query})

# Check if the request was successful (status code 200)

if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Extract and process the data from the response
    matched_user = data['data']['matchedUser']
    username = matched_user['username']
    submit_stats = matched_user['submitStats']
    ac_submission_num = submit_stats['acSubmissionNum']
    
    # Print the extracted data
    print("Username:", username)
    print("AC Submission Stats:")
    for submission in ac_submission_num:
        print("Difficulty:", submission['difficulty'])
        print("Count:", submission['count'])
        print("Submissions:", submission['submissions'])
        print("-" * 50)
else:
    # Print an error message if the request was unsuccessful
    print("Error fetching data. Status code:", response.status_code)




