def average_level(team_members: list, level_data: dict) -> float:
    total = sum(level_data[member] for member in team_members)
    return total / len(team_members)

def is_whitelisted(team_members: list, level_data: dict) -> bool:
    return average_level(team_members, level_data) >= 2