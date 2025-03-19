import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import time

TOURNAMENT_ID="littlecup"
PLACEHOLDER_PLAYER="nobody" # when someone gets a "bye", we use this as a dummy player name they have beaten

def get_round_data(round_number):
    """Collects the results of every match into an array"""
    url = f"https://play.limitlesstcg.com/tournament/{TOURNAMENT_ID}/pairings?round={round_number}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch round {round_number}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if not table:
        print("No table found")
        return []

    matches = []
    for tr in table.find_all('tr'):
        match_id = tr.get('data-match')
        winner_id = tr.get('data-winner')  # 0 if havent played yet -1 if cancelled, player name otherwise

        players = tr.find_all('td', class_=['player', 'player unl', 'player winner', 'player tie'])
        if len(players) == 1: # len = 1 means a bye
            player1 = {
                'id': players[0].get('data-id'),
                'wins': int(players[0].get('data-wins', 0)),
                'losses': int(players[0].get('data-losses', 0)),
                'ties': int(players[0].get('data-ties', 0))
            }

            player2 = {
                'id': PLACEHOLDER_PLAYER,
                'wins': 0,
                'losses': 0,
                'ties': 0
            }

            matches.append({
                'match_id': match_id,
                'winner_id': winner_id,
                'players': [player1, player2]
            })
        elif len(players) == 2:
            player1 = {
                'id': players[0].get('data-id'),
                'wins': int(players[0].get('data-wins', 0)),
                'losses': int(players[0].get('data-losses', 0)),
                'ties': int(players[0].get('data-ties', 0))
            }

            player2 = {
                'id': players[1].get('data-id'),
                'wins': int(players[1].get('data-wins', 0)),
                'losses': int(players[1].get('data-losses', 0)),
                'ties': int(players[1].get('data-ties', 0))
            }

            print(f"Match {match_id}: {player1['id']} vs {player2['id']}")

            matches.append({
                'match_id': match_id,
                'winner_id': winner_id,
                'players': [player1, player2]
            })
        else: # empty row in table, or more commonly empty table for unavailable rounds
            print(f"Unexpected number of players in match {match_id}")

    print(f"Scraped {len(matches)} matches from round {round_number}")
    return matches

# get player scores out of the collected match data
def analyze_tournament_data(tournament_data):
    """Get player scores out of the collected match data.
    Unplayed matches are treated the same as ties initially, and then ties in the most recent round are changed to unplayed.
    """
    player_stats = defaultdict(lambda: {"wins": 0, "losses": 0, "unplayed": 0, "ties": 0, "games_played": 0, "opponents": []})
    
    # Process match results
    counter = 0
    for round_data in tournament_data.values():
        counter += 1
        for match in round_data:
            players = match["players"]
            winner_id = match["winner_id"]
            
            p1, p2 = players[0]["id"], players[1]["id"]
            player_stats[p1]["games_played"] += 1
            player_stats[p2]["games_played"] += 1
            player_stats[p1]["opponents"].append(p2)
            player_stats[p2]["opponents"].append(p1)
            
            if winner_id == "0":  # Tie
                if counter == len(tournament_data):
                    player_stats[p1]["games_played"] -= 1
                    player_stats[p2]["games_played"] -= 1
                    player_stats[p1]["unplayed"] += 1
                    player_stats[p2]["unplayed"] += 1
                else:
                    player_stats[p1]["ties"] += 1
                    player_stats[p2]["ties"] += 1
            elif winner_id == p1:
                player_stats[p1]["wins"] += 1
                player_stats[p2]["losses"] += 1
            elif winner_id == p2:
                player_stats[p2]["wins"] += 1
                player_stats[p1]["losses"] += 1
    
    # Compute winrates
    for player, stats in player_stats.items():
        # Compute player winrate
        played = stats["games_played"]
        wins = stats["wins"]
        if played > 0:
            stats["winrate"] = max(wins / played, 0.25)
        else:
            stats["winrate"] = 0.25 # winrate has a lower bound of 0.25 for droppers
        
        # Compute opponent winrates
        min_opponent_winrates = []
        max_opponent_winrates = []
        for opp in stats["opponents"]:
            if opp != PLACEHOLDER_PLAYER:
                opp_played = player_stats[opp]["games_played"]
                opp_wins = player_stats[opp]["wins"]
                opp_unplayed = player_stats[opp]["unplayed"]
                min_opponent_winrates.append(max(opp_wins / (opp_played+opp_unplayed), 0.25))
                max_opponent_winrates.append(max((opp_wins+opp_unplayed) / (opp_played+opp_unplayed), 0.25))
        stats["min_opp_winrate"] = sum(min_opponent_winrates) / max(len(min_opponent_winrates), 1)
        stats["max_opp_winrate"] = sum(max_opponent_winrates) / max(len(max_opponent_winrates), 1)
    
    return player_stats

def save_to_csv(player_database, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Player ID", "Wins", "Losses", "Ties", "Games Played", "Winrate", "Min Opp Win%", "Max Opp Win%"])
        
        for player, stats in player_database.items():
            writer.writerow([player, stats["wins"], stats["losses"], stats["ties"], stats["games_played"], 
                             stats["winrate"], stats["min_opp_winrate"], stats["max_opp_winrate"]])

def scrape_and_analyze_tournament(output_file):
    print(f"Scraping tournament data for {TOURNAMENT_ID}...")
    tournament_data = {}
    
    round_number = 1
    scraped_round_data = [{}]
    # scrape data for every round until we run into a round that has no available data
    while scraped_round_data != []:
        print(f"Scraping round {round_number}...")
        scraped_round_data = get_round_data(round_number)
        if scraped_round_data != []:
            tournament_data[f'Round {round_number}'] = scraped_round_data
            time.sleep(1)
            round_number += 1
    
    print("Analyzing tournament data...")
    player_database = analyze_tournament_data(tournament_data)
    
    print(f"Saving results to {output_file}...")
    save_to_csv(player_database, output_file)

# Run the script
if __name__ == "__main__":
    scrape_and_analyze_tournament("tournament_results.csv")