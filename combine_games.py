import json
import glob

# Find all JSON game files
game_files = glob.glob("varshetaa_games_*.json")

print(f"Found {len(game_files)} game files:")
for file in game_files:
    print(f"  - {file}")

all_games = []

# Load and combine all games
for file in game_files:
    print(f"\nLoading {file}...")
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            games = data.get('games', [])
            all_games.extend(games)
            print(f"  ✅ Added {len(games)} games")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print(f"\n{'='*60}")
print(f"TOTAL GAMES COMBINED: {len(all_games)}")
print(f"{'='*60}")

# Save combined games
output_file = "all_games_combined.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({"games": all_games}, f, indent=2)

print(f"\n✅ All games saved to: {output_file}")