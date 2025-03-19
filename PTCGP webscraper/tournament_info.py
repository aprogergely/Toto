# decklist
import requests
from bs4 import BeautifulSoup
import csv

# Base URL of the website
BASE_URL = "https://play.limitlesstcg.com"
TOURNAMENT_ID = "sniperduel"

# Function to fetch and parse the HTML content of a URL
def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
        return None

# Function to extract player links from the main page
def get_player_links(main_page):
    player_links = []
    for a_tag in main_page.find_all("a", href=True):
        href = a_tag["href"]
        #print(a_tag)
        if href.startswith(f"/tournament/{TOURNAMENT_ID}/player/") and href.endswith("/decklist"):
            print(href)
            player_links.append(BASE_URL + href)
    return player_links

# Function to extract cards from a player's decklist page
def get_decklist(player_page):
    decklist = []
    for a_tag in player_page.find_all("a", href=True):
        href = a_tag["href"]
        if "cards/" in href:
            card_text = a_tag.text.strip()
            decklist.append(card_text)
    return decklist

# Main function to scrape and save data
def scrape_and_save():
    # Fetch and parse the main page
    main_page = fetch_page(f"{BASE_URL}/tournament/{TOURNAMENT_ID}/standings")
    if not main_page:
        return

    # Get player links
    player_links = get_player_links(main_page)

    # Prepare CSV file
    with open("decklists.csv", "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Player Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name", "Card Name"])

        # Visit each player's decklist page
        for player_link in player_links:
            cardlist = []
            player_page = fetch_page(player_link)
            if not player_page:
                continue

            # Extract player name from the URL
            player_name = player_link.split("/")[-2]

            # Get decklist
            decklist = get_decklist(player_page)

            # Write to CSV file
            for card in decklist:
                card_amount = card[0]  # First character is the card amount
                card = card[2:].strip()  # Rest is the card name and code
                for i in range(0, int(card_amount)):
                    cardlist.append(card)
            print(player_name)
            csvwriter.writerow([player_name, ", ".join(cardlist)])

    print("Scraping completed. Data saved to decklists.csv")

# Run the scraper
if __name__ == "__main__":
    scrape_and_save()
