import requests
import json
import time
from datetime import datetime

# Your Chess.com username
USERNAME = "varshetaa"

def fetch_game_archives():
    """Get list of all months with games"""
    url = f"https://api.chess.com/pub/player/{USERNAME}/games/archives"
    print(f"Fetching game archives for {USERNAME}...")
    
    # Add headers to avoid 403 errors
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        archives = response.json()['archives']
        print(f"Found {len(archives)} months with games!")
        return archives
    except Exception as e:
        print(f"Error fetching archives: {e}")
        return []

def fetch_games_for_month(archive_url):
    """Fetch all games for a specific month"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(archive_url, headers=headers)
        response.raise_for_status()
        return response.json()['games']
    except Exception as e:
        print(f"Error fetching games from {archive_url}: {e}")
        return []

def fetch_all_games():
    """Fetch all games from all months"""
    archives = fetch_game_archives()
    all_games = []
    
    for i, archive_url in enumerate(archives, 1):
        # Extract year/month from URL for display
        parts = archive_url.split('/')
        year_month = f"{parts[-2]}/{parts[-1]}"
        
        print(f"Fetching games from {year_month} ({i}/{len(archives)})...")
        games = fetch_games_for_month(archive_url)
        all_games.extend(games)
        
        # Be nice to the API - wait a bit between requests
        time.sleep(0.5)
    
    print(f"\nTotal games fetched: {len(all_games)}")
    return all_games

def save_games(games):
    """Save games to a JSON file"""
    filename = f"{USERNAME}_games.json"
    with open(filename, 'w') as f:
        json.dump(games, f, indent=2)
    print(f"Games saved to {filename}")

def show_summary(games):
    """Display a quick summary of the games"""
    if not games:
        print("No games found!")
        return
    
    print("\n" + "="*50)
    print("GAME SUMMARY")
    print("="*50)
    
    # Count by time control
    time_controls = {}
    wins = 0
    losses = 0
    draws = 0
    
    for game in games:
        # Count time controls
        tc = game.get('time_class', 'unknown')
        time_controls[tc] = time_controls.get(tc, 0) + 1
        
        # Count results
        white = game.get('white', {})
        black = game.get('black', {})
        
        if white.get('username', '').lower() == USERNAME.lower():
            result = white.get('result', '')
            if result == 'win':
                wins += 1
            elif result in ['checkmated', 'resigned', 'timeout', 'abandoned']:
                losses += 1
            else:
                draws += 1
        elif black.get('username', '').lower() == USERNAME.lower():
            result = black.get('result', '')
            if result == 'win':
                wins += 1
            elif result in ['checkmated', 'resigned', 'timeout', 'abandoned']:
                losses += 1
            else:
                draws += 1
    
    print(f"\nTotal Games: {len(games)}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Draws: {draws}")
    
    if wins + losses > 0:
        win_rate = (wins / (wins + losses)) * 100
        print(f"Win Rate: {win_rate:.1f}%")
    
    print("\nGames by Time Control:")
    for tc, count in sorted(time_controls.items()):
        print(f"  {tc}: {count} games")

if __name__ == "__main__":
    print("Chess.com Game Fetcher")
    print("="*50)
    print()
    
    # Fetch all games
    games = fetch_all_games()
    
    # Save to file
    if games:
        save_games(games)
        show_summary(games)
    else:
        print("No games were fetched. Please check your username and internet connection.")
    
    print("\n" + "="*50)
    print("Done!")