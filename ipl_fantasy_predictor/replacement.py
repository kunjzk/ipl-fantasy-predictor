from typing import Dict, List
import pandas as pd


def create_player_points_df() -> pd.DataFrame:
    """Read points.txt and generate a DataFrame.

    Returns:
        player_points_df: DataFrame containing the points of all players.
    """
    player_points_df = pd.read_csv("points.txt", sep="\t")
    return player_points_df


def preprocess_points_df(player_points_df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the points dataframe to make it easier to work with.

    Args:
        player_points_df: DataFrame containing the points of all players.

    Returns:
        player_points_df: Preprocessed DataFrame.
    """
    player_points_df.loc[
        player_points_df["Foreigner(Y/N)"].isna(), "Foreigner(Y/N)"
    ] = "N"
    player_points_df.drop(columns=["Error"], inplace=True)
    player_points_df.rename(
        columns={
            "IPL Player Name": "Player",
            "Foreigner(Y/N)": "Overseas",
            "Snapshot": "Pts",
        },
        inplace=True,
    )
    return player_points_df


def create_my_team(my_players: List, player_points_df: pd.DataFrame) -> pd.DataFrame:
    """Create a DataFrame containing only my team players.

    Args:
        my_players: List of players in my team.
        player_points_df: DataFrame containing the points of all players.

    Returns:
        my_team: DataFrame containing only my team players.
    """
    my_team = player_points_df.loc[player_points_df["Player"].isin(my_players)]
    return my_team


def replace_players(my_players: List, player_points_df: pd.DataFrame) -> List:
    """Replace the bottom 3 players in my team with better players.

    Args:
        my_players: List of players in my team.
        player_points_df: DataFrame containing the points of all players.

    Returns:
        players_to_replace: List of dictionaries containing the players to replace.
    """
    my_team = create_my_team(my_players, player_points_df)
    remaining_players = player_points_df.loc[
        player_points_df["Player"].isin(my_players) == False
    ]
    # print(f"My team points: {my_team_points}")
    my_bottom_3 = my_team.sort_values(by="Pts").head(3)
    # print("Bottom 3 players:")
    players_to_replace = []
    for _, player in my_bottom_3.iterrows():
        # print(f"{player['Player']}: {player['Pts']}")
        # Is there another player from the same team, in my team?
        need_same_team = False
        if len(my_team.loc[my_team["Team"] == player["Team"]]) == 1:
            need_same_team = True
        if player["Overseas"] == "N":
            remaining_players_choices = remaining_players.loc[
                remaining_players["Overseas"] == "N"
            ]
        if need_same_team:
            remaining_players_team = remaining_players_choices.loc[
                remaining_players_choices["Team"] == player["Team"]
            ]
            best_player = remaining_players_team.sort_values(
                by="Pts", ascending=False
            ).head(1)
            # print(f"Replaced {player['Player']} with {best_player['Player'].values[0]}")
            # print(f"Points gained: {best_player['Pts'].values[0] - player['Pts']}")
        else:
            players_left = remaining_players_choices.loc[
                remaining_players_choices["Player"].isin(my_players) == False
            ]
            best_player = players_left.sort_values(by="Pts", ascending=False).head(1)
            # print(f"Replaced {player['Player']} with {best_player['Player'].values[0]}")
            # print(f"Points gained: {best_player['Pts'].values[0] - player['Pts']}")
        remaining_players = remaining_players.loc[
            remaining_players["Player"] != best_player["Player"].values[0]
        ]
        # print()
        replacement_dict = {
            "player_out": player["Player"],
            "player_out_points": player["Pts"],
            "player_in": best_player["Player"].values[0],
            "player_in_points": best_player["Pts"].values[0],
        }
        players_to_replace.append(replacement_dict)
    return players_to_replace


if __name__ == "__main__":
    my_players = [
        "Andre Russell",
        "Rohit Sharma",
        "Rachin Ravindra",
        "Wriddhiman Saha",
        "Jasprit Bumrah",
        "Ravindra Jadeja",
        "MS Dhoni",
        "Ravichandran Ashwin",
        "Heinrich Klaasen",
        "Shubman Gill",
        "Mohit Sharma",
        "Virat Kohli",
        "Kuldeep Yadav",
        "Nicholas Pooran",
        "Harpreet Brar",
    ]
    player_points_df = create_player_points_df()
    player_points_df = preprocess_points_df(player_points_df)
    my_team = create_my_team(my_players, player_points_df)
    replace_players(my_players, player_points_df)
