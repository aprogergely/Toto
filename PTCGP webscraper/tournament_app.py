from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = "https://play.limitlesstcg.com"

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        return None

def get_player_links(main_page):
    player_links = []
    for a_tag in main_page.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/tournament/") and href.endswith("/decklist"):
            player_links.append(BASE_URL + href)
    return player_links

def get_decklist(player_page):
    decklist = []
    for a_tag in player_page.find_all("a", href=True):
        href = a_tag["href"]
        if "cards/" in href:
            card_text = a_tag.text.strip()
            decklist.append(card_text)
    return decklist

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    link1 = data.get('link1')

    if not link1:
        return jsonify({"error": "No 'link1' provided"}), 400

    main_page = fetch_page(link1)
    if not main_page:
        return jsonify({"error": "Failed to fetch the main page"}), 500

    player_links = get_player_links(main_page)
    results = {}

    for player_link in player_links:
        player_page = fetch_page(player_link)
        if not player_page:
            continue

        player_name = player_link.split("/")[-2]
        decklist = get_decklist(player_page)
        cardlist = []

        for card in decklist:
            card_amount = card[0]
            card_details = card[2:].strip()
            for i in range(int(card_amount)):
                cardlist.append(card_details)

        results[player_name] = cardlist

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
