import json
from collections import Counter, defaultdict

# Your downloaded file name
GAME_FILE = "varshetaa_games_nov2024.json"
USERNAME = "varshetaa"

def load_games():
    """Load games from the JSON file"""
    print(f"Loading games from {GAME_FILE}...")
    try:
        with open(GAME_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            games = data.get('games', [])
            print(f"✅ Loaded {len(games)} games!")
            return games
    except FileNotFoundError:
        print(f"❌ Error: Could not find {GAME_FILE}")
        print("Make sure the file is in the same folder as this script!")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error: {GAME_FILE} is not valid JSON")
        return []

def extract_opening(pgn, eco_url):
    """Extract opening name from PGN or ECO URL"""
    if eco_url and 'openings/' in eco_url:
        opening = eco_url.split('openings/')[-1]
        opening = opening.replace('-', ' ').title()
        # Remove trailing numbers and clean up
        opening = opening.split('...')[0].strip()
        return opening
    return "Unknown"

def analyze_games(games):
    """Analyze all games and generate report"""
    
    if not games:
        print("No games to analyze!")
        return
    
    # Stats tracking
    total_wins = 0
    total_losses = 0
    total_draws = 0
    
    white_games = 0
    white_wins = 0
    black_games = 0
    black_wins = 0
    
    openings_as_white = Counter()
    openings_as_black = Counter()
    
    opening_results = defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0, 'as_white': 0, 'as_black': 0})
    
    time_controls = Counter()
    
    print("\n" + "="*60)
    print("ANALYZING YOUR CHESS GAMES - VARSHETAA")
    print("="*60)
    
    for game in games:
        # Determine your color
        white_player = game.get('white', {}).get('username', '').lower()
        black_player = game.get('black', {}).get('username', '').lower()
        
        playing_white = (white_player == USERNAME.lower())
        playing_black = (black_player == USERNAME.lower())
        
        if not (playing_white or playing_black):
            continue
        
        # Get result
        if playing_white:
            result = game.get('white', {}).get('result', '')
            white_games += 1
        else:
            result = game.get('black', {}).get('result', '')
            black_games += 1
        
        # Count results
        if result == 'win':
            total_wins += 1
            if playing_white:
                white_wins += 1
        elif result in ['checkmated', 'resigned', 'timeout', 'abandoned', 'lose']:
            total_losses += 1
        else:
            total_draws += 1
        
        # Extract opening
        eco_url = game.get('eco', '')
        pgn = game.get('pgn', '')
        opening = extract_opening(pgn, eco_url)
        
        # Track openings by color
        if playing_white:
            openings_as_white[opening] += 1
            opening_results[opening]['as_white'] += 1
        else:
            openings_as_black[opening] += 1
            opening_results[opening]['as_black'] += 1
        
        # Track opening results
        if result == 'win':
            opening_results[opening]['wins'] += 1
        elif result in ['checkmated', 'resigned', 'timeout', 'abandoned', 'lose']:
            opening_results[opening]['losses'] += 1
        else:
            opening_results[opening]['draws'] += 1
        
        # Time controls
        time_class = game.get('time_class', 'unknown')
        time_controls[time_class] += 1
    
    total_games = len(games)
    
    # Print results
    print(f"\n📊 OVERALL STATISTICS")
    print(f"   Total Games: {total_games}")
    print(f"   Wins: {total_wins} ({total_wins/total_games*100:.1f}%)")
    print(f"   Losses: {total_losses} ({total_losses/total_games*100:.1f}%)")
    print(f"   Draws: {total_draws} ({total_draws/total_games*100:.1f}%)")
    
    if total_wins + total_losses > 0:
        win_rate = (total_wins / (total_wins + total_losses)) * 100
        print(f"   Win Rate: {win_rate:.1f}%")
    
    print(f"\n♟️  PERFORMANCE BY COLOR")
    if white_games > 0:
        print(f"   As White: {white_games} games, {white_wins} wins ({white_wins/white_games*100:.1f}%)")
    if black_games > 0:
        black_wins_total = total_wins - white_wins
        print(f"   As Black: {black_games} games, {black_wins_total} wins ({black_wins_total/black_games*100:.1f}%)")
    
    print(f"\n⏱️  TIME CONTROLS")
    for tc, count in time_controls.most_common():
        print(f"   {tc.title()}: {count} games")
    
    print(f"\n📖 TOP 5 OPENINGS AS WHITE")
    for opening, count in openings_as_white.most_common(5):
        stats = opening_results[opening]
        white_total = stats['as_white']
        if white_total > 0:
            wr = (stats['wins'] / (stats['wins'] + stats['losses'] + stats['draws']) * 100) if (stats['wins'] + stats['losses'] + stats['draws']) > 0 else 0
            print(f"   {opening}: {count} games (Win rate: {wr:.1f}%)")
    
    print(f"\n📖 TOP 5 OPENINGS AS BLACK")
    for opening, count in openings_as_black.most_common(5):
        stats = opening_results[opening]
        black_total = stats['as_black']
        if black_total > 0:
            wr = (stats['wins'] / (stats['wins'] + stats['losses'] + stats['draws']) * 100) if (stats['wins'] + stats['losses'] + stats['draws']) > 0 else 0
            print(f"   {opening}: {count} games (Win rate: {wr:.1f}%)")
    
    print(f"\n🎯 HOW YOU LOSE")
    loss_methods = Counter()
    for game in games:
        white_player = game.get('white', {}).get('username', '').lower()
        black_player = game.get('black', {}).get('username', '').lower()
        
        if white_player == USERNAME.lower():
            result = game.get('white', {}).get('result', '')
        elif black_player == USERNAME.lower():
            result = game.get('black', {}).get('result', '')
        else:
            continue
            
        if result in ['checkmated', 'resigned', 'timeout', 'abandoned']:
            loss_methods[result] += 1
    
    for method, count in loss_methods.most_common():
        print(f"   {method.title()}: {count} times")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    games = load_games()
    analyze_games(games)
    print("\n✅ Analysis complete!")