
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re

# Initialize Flask app
app = Flask(__name__)

class GoldrateScraper:
    def __init__(self):
        self.__headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
        }
        self.url = "https://www.thehindubusinessline.com/gold-rate-today/Chennai/"

    def get_gold_rates(self):
        """Scrape gold rates using requests and BeautifulSoup."""
        # Send HTTP request to fetch the webpage content
        response = requests.get(self.url, headers=self.__headers)
        if response.status_code != 200:
            print("Failed to retrieve the webpage.")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for divs that contain "22ct" and "24ct" in the text
        gold_22ct = soup.find('div', class_=re.compile('status1'))
        gold_24ct = soup.find('div', class_=re.compile('status2'))

        if not gold_22ct or not gold_24ct:
            print("Could not find the gold rate elements.")
            return None

        # Extract the text and clean it
        rate_22ct = gold_22ct.find('b').text.strip() if gold_22ct else 'N/A'
        rate_24ct = gold_24ct.find('b').text.strip() if gold_24ct else 'N/A'

        # Create a dictionary with the results
        data = {
            '22ct_gold_rate': rate_22ct,
            '24ct_gold_rate': rate_24ct
        }

        return data

# Define the route for the API
@app.route('/api/gold-rates', methods=['GET'])
def gold_rates():
    scraper = GoldrateScraper()
    data = scraper.get_gold_rates()
    
    if data:
        return jsonify(data), 200  # Return the data as JSON
    else:
        return jsonify({"error": "Failed to retrieve gold rates"}), 500

if __name__ == "__main__":
    app.run(debug=True)
