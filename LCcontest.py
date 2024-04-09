import requests

# GraphQL query
query = """
query getUserContestRanking ($username: String!) {
    userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        totalParticipants
        topPercentage
        badge {
            name
        }
    }
    userContestRankingHistory(username: $username) {
        attended
        rating
        ranking
        trendDirection
        problemsSolved
        totalProblems
        finishTimeInSeconds
        contest {
            title
            startTime
        }
    }
}
"""

# GraphQL endpoint
url = 'https://leetcode.com/graphql'

# Variables for the query
variables = {
    "username": "ShivamBedar"  # Replace 'your_username' with the desired username
}

# Make the POST request to the GraphQL API
response = requests.post(url, json={'query': query, 'variables': variables})

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Extract and process the data from the response
    user_contest_ranking = data['data']['userContestRanking']
    user_contest_ranking_history = data['data']['userContestRankingHistory']
    
    # Print the extracted data
    print("User Contest Ranking:")
    print("Attended Contests Count:", user_contest_ranking['attendedContestsCount'])
    print("Rating:", user_contest_ranking['rating'])
    print("Global Ranking:", user_contest_ranking['globalRanking'])
    print("Total Participants:", user_contest_ranking['totalParticipants'])
    print("Top Percentage:", user_contest_ranking['topPercentage'])
    badge = user_contest_ranking['badge']
    if badge:
        print("Badge:", badge['name'])
    
    print("\nUser Contest Ranking History:")
    for history in user_contest_ranking_history:
        print("Contest Title:", history['contest']['title'])
        print("Contest Start Time:", history['contest']['startTime'])
        print("Attended:", history['attended'])
        print("Rating:", history['rating'])
        print("Ranking:", history['ranking'])
        print("Trend Direction:", history['trendDirection'])
        print("Problems Solved:", history['problemsSolved'])
        print("Total Problems:", history['totalProblems'])
        print("Finish Time (Seconds):", history['finishTimeInSeconds'])
        print("-" * 50)
else:
    # Print an error message if the request was unsuccessful
    print("Error fetching data. Status code:", response.status_code)
