import json
from smart_contracts.whitelist_logic import is_whitelisted

with open("data/player_levels.json") as f:
    level_data = json.load(f)

with open("data/teams.json") as f:
    teams = json.load(f)

for team_id, members in teams.items():
    if is_whitelisted(members, level_data):
        print(f"Team {team_id} is eligible")
    else:
        print(f"Team {team_id} is NOT eligible")