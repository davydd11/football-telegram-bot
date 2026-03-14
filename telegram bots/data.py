import logging 

logger = logging.getLogger(__name__)

"""
Data module.

Handles:
- loading players from JSON
- searching players
- saving new players
"""


import json
from modules import Player

DATA_FILE = "data.json"


def get_top_players():
    players = load_players()

    sorted_players = sorted(
        players,
        key=lambda player: player.goals,
        reverse=True
    )

    return sorted_players[:5]


def load_players():

    """
    Load all players from json file.

    Returns:
        list[Player]: players are becoming objects.
    """

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
        return [Player(**player) for player in data]


def find_player_by_name(name: str):

    """
    Search players by name.

    Arguments:
        name (str): name or part of a name entered by the user.
    """
    
    players = load_players()
    found_players = []

    for player in players:
        if name.lower() in player.name.lower():
            found_players.append(player)

    return found_players



def save_player_to_file(player: Player):

    """
    Save a new player to the JSON file.

    Args:
        player (Player): Player object that will be saved to the file.
    """

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(player.model_dump())

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        logging.info("player saved to file.")
