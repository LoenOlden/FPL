from sorted_players_data import (
    goalkeepers_sorted,
    defenders_sorted,
    midfielders_sorted,
    forwards_sorted,
)

output_file = "sortedplayersbycost.py"

def add_xPperCost_and_sort(player_list):
    for player in player_list:
        player["xPperCost"] = round(player["xP"] / player["cost"], 3)
    return sorted(player_list, key=lambda p: p["xPperCost"], reverse=True)

# Process all player lists
goalkeepers_sorted = add_xPperCost_and_sort(goalkeepers_sorted)
defenders_sorted = add_xPperCost_and_sort(defenders_sorted)
midfielders_sorted = add_xPperCost_and_sort(midfielders_sorted)
forwards_sorted = add_xPperCost_and_sort(forwards_sorted)

def format_player(player):
    return (
        f'{{ "id": "{player["id"]}", "name": "{player["name"]}", '
        f'"position": "{player["position"]}", "team": {player["team"]}, '
        f'"cost": {player["cost"]}, "xP": {player["xP"]}, '
        f'"xPperCost": {player["xPperCost"]} }}'
    )

def format_list(name, players):
    lines = [format_player(p) for p in players]
    return f"{name} = [\n    " + ",\n    ".join(lines) + "\n]\n"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("# Auto-generated file: sorted by xPperCost\n\n")
    f.write(format_list("goalkeepers_sorted", goalkeepers_sorted))
    f.write("\n")
    f.write(format_list("defenders_sorted", defenders_sorted))
    f.write("\n")
    f.write(format_list("midfielders_sorted", midfielders_sorted))
    f.write("\n")
    f.write(format_list("forwards_sorted", forwards_sorted))

print(f"✅ Created '{output_file}' in original format with UTF-8 encoding.")
