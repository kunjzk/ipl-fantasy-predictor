import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from ipl_fantasy_predictor.replacement import (
    create_my_team,
    preprocess_points_df,
    create_player_points_df,
    replace_players,
)

player_points_df = preprocess_points_df(create_player_points_df())
player_names = player_points_df["Player"].tolist()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
KUNAL_PLAYERS = [
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
MAMA_PLAYERS = [
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
app.layout = html.Div(
    [
        html.H1("IPL Fantasy Team Optimizer"),
        html.Div(
            [
                dbc.Row(
                    children=[
                        dbc.Col(
                            # html.H3("Select 11 players"),
                            dcc.Dropdown(
                                id="player-dropdown",
                                options=[
                                    {"label": name, "value": name}
                                    for name in player_names
                                ],
                                multi=True,
                                placeholder="Select 11 players",
                            ),
                            width=8,
                        ),
                        dbc.Col(
                            dbc.Checkbox(
                                id="kunal-team",
                                label="Use Kunal Team",
                            ),
                            width=1,
                        ),
                        dbc.Col(
                            dbc.Checkbox(
                                id="mama-team",
                                label="Use Mama Team",
                            ),
                            width=1,
                        ),
                        dbc.Col(
                            dbc.Button(
                                id="submit-button",
                                color="success",
                                className="me-1",
                                children="Submit",
                                n_clicks=0,
                            ),
                            width=1,
                        ),
                    ]
                )
            ]
        ),
        html.Br(),
        html.Div(id="output"),
    ]
)


@app.callback(
    Output("output", "children"),
    [Input("submit-button", "n_clicks")],
    [
        State("player-dropdown", "value"),
        State("kunal-team", "value"),
        State("mama-team", "value"),
    ],
)
def update_output(n_clicks, selected_players, kunal_team, mama_team):
    if n_clicks > 0:
        if kunal_team and mama_team:
            return html.Div("Select only one team between Kunal and Mama and retry")
        if kunal_team:
            selected_players = KUNAL_PLAYERS
        elif mama_team:
            selected_players = MAMA_PLAYERS
        if len(selected_players) != 15:
            return html.Div("Please select exactly 15 players and retry")
        else:
            current_team = create_my_team(selected_players, player_points_df)
            current_team_points = sum(current_team["Pts"])
            replacements = replace_players(selected_players, player_points_df)
            replacements_points = sum(
                [replacement["player_in_points"] for replacement in replacements]
            )
            players_out_points = sum(
                [replacement["player_out_points"] for replacement in replacements]
            )
            new_team_points = (
                current_team_points - players_out_points + replacements_points
            )
            return html.Div(
                [
                    html.H3(f"Curent points: {current_team_points}"),
                    html.H3("Replace these players:"),
                    html.Ul(
                        [
                            html.Li(
                                f'{replacement["player_out"]} ({replacement["player_out_points"]} points) for {replacement["player_in"]} ({replacement["player_in_points"]} points)'
                            )
                            for replacement in replacements
                        ]
                    ),
                    html.H3(f"New points: {new_team_points}"),
                ]
            )
    else:
        return html.Div("Select players and click submit.")


if __name__ == "__main__":
    app.run_server(debug=True)
