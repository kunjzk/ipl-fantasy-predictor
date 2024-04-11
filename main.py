import pandas as pd


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


def main():
    # my_players = [
    #     "Andre Russell",
    #     "Rohit Sharma",
    #     "Rachin Ravindra",
    #     "Wriddhiman Saha",
    #     "Jasprit Bumrah",
    #     "Ravindra Jadeja",
    #     "MS Dhoni",
    #     "Ravichandran Ashwin",
    #     "Heinrich Klaasen",
    #     "Shubman Gill",
    #     "Mohit Sharma",
    #     "Virat Kohli",
    #     "Kuldeep Yadav",
    #     "Nicholas Pooran",
    #     "Harpreet Brar",
    # ]
    my_players = [
        "Andre Russell",
        "Sanju Samson",
        "Rohit Sharma",
        "MS Dhoni",
        "K L Rahul",
        "Umesh Yadav",
        "Mitchell Marsh",
        "Faf du Plessis",
        "Azmatullah Omarzai",
        "Harshal Patel",
        "Harshit Rana",
        "Jasprit Bumrah",
        "Anuj Rawat",
        "Mayank Markande",
        "Abishek Porel",
    ]
    player_points_df = pd.read_csv("points.txt", sep="\t")
    player_points_df = preprocess_points_df(player_points_df)
    my_team = player_points_df.loc[player_points_df["Player"].isin(my_players)]
    remaining_players = player_points_df.loc[
        player_points_df["Player"].isin(my_players) == False
    ]
    my_team_points = sum(my_team["Pts"])
    print(f"My team points: {my_team_points}")
    my_bottom_3 = my_team.sort_values(by="Pts").head(3)
    print("Bottom 3 players:")
    for _, player in my_bottom_3.iterrows():
        print(f"{player['Player']}: {player['Pts']}")
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
            print(f"Replaced {player['Player']} with {best_player['Player'].values[0]}")
            print(f"Points gained: {best_player['Pts'].values[0] - player['Pts']}")
        else:
            players_left = remaining_players_choices.loc[
                remaining_players_choices["Player"].isin(my_players) == False
            ]
            best_player = players_left.sort_values(by="Pts", ascending=False).head(1)
            print(f"Replaced {player['Player']} with {best_player['Player'].values[0]}")
            print(f"Points gained: {best_player['Pts'].values[0] - player['Pts']}")
        points_gained = best_player["Pts"].values[0] - player["Pts"]
        my_team_points += points_gained
        remaining_players = remaining_players.loc[
            remaining_players["Player"] != best_player["Player"].values[0]
        ]
        print()

    print(f"My team points after replacements: {my_team_points}")


if __name__ == "__main__":
    main()
