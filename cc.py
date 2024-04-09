import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/<handle>')
def get_user_info(handle):
    try:
        response = requests.get(f'https://www.codechef.com/users/{handle}')
        soup = BeautifulSoup(response.text, 'html.parser')
        
        user_details = soup.select('.user-details-container')[0]
        profile = user_details.find('img')['src']
        name = user_details.find_all('div', class_='user-details')[0].find('a').text.strip()
        
        current_rating = int(soup.select_one('.rating-number').text)
        highest_rating = int(soup.select_one('.rating-number').parent.contents[4].text.split('Rating')[1])
        
        country_flag = soup.select_one('.user-country-flag')['src']
        country_name = soup.select_one('.user-country-name').text.strip()
        
        global_rank = int(soup.select('.rating-ranks')[0].find_all('td')[0].text)
        country_rank = int(soup.select('.rating-ranks')[0].find_all('td')[1].text)
        
        stars = soup.select_one('.rating').text.strip() if soup.select_one('.rating') else "unrated"
        
        return jsonify({
            "success": True,
            "profile": profile,
            "name": name,
            "currentRating": current_rating,
            "highestRating": highest_rating,
            "countryFlag": country_flag,
            "countryName": country_name,
            "globalRank": global_rank,
            "countryRank": country_rank,
            "stars": stars
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/')
def home():
    return "Hi you are at the right endpoint, just add /handle_of_user at the end of the URL. Thanks for ⭐️"

if __name__ == '__main__':
    app.run(debug=True, port=8800)
