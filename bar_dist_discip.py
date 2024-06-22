# import pandas as pd
# import plotly.express as px
#
# required_stats = [
#     'Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards', 'Goals conceded',
#     'Own-goals', 'Saves on penalty', 'Saves', 'Punches', 'Tackles', 'Tackles lost', 'Blocks',
#     'Recovered balls', 'Assists', 'Dribbling', 'Corners', 'Offsides', 'Clearances', 'Goals scored on penalty ',
#     'Passes attempted', 'Passes completed', 'Free kicks on goal ', 'Crosses attempted', 'Crosses completed',
# ]
# def load_data(file_path):
#     columns = ['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime', 'StatsName', 'Value']
#     return pd.read_excel(file_path, sheet_name='Players stats', usecols=columns)
#
# def filter_data_for_team(df, team_name, player_list):
#     # Filter the stats within Sheet3 to keep only the required stats and for the specified team
#     required_stats = [
#         'Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards', 'Goals conceded',
#         'Own-goals', 'Saves on penalty', 'Saves', 'Punches', 'Tackles', 'Tackles lost', 'Blocks',
#         'Recovered balls', 'Assists', 'Dribbling', 'Corners', 'Offsides', 'Clearances', 'Goals scored on penalty ',
#         'Passes attempted', 'Passes completed', 'Free kicks on goal ', 'Crosses attempted', 'Crosses completed',
#     ]
#     df = df[df['StatsName'].isin(required_stats) & df['PlayerSurname'].isin(player_list)]
#     return df.drop_duplicates()
#
# def pivot_data(df):
#     pivot_df = df.pivot(index=['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime'],
#                         columns='StatsName', values='MatchID').reset_index().fillna(0)
#     return pivot_df
#
# def prepare_data(df, team_name):
#     # Assuming a dictionary mapping teams to players
#     team_players = {
#         'Austria': ['Baumgartner', 'Lainer', 'Gregoritsch', 'Sabitzer', 'Arnautovic', 'Kalajdzic', 'Trimmel', 'Alaba', 'Schlager', 'Dragovic'],
#         'Belgium': ['Lukaku', 'Hazard', 'Vanaken', 'De Bruyne', 'Meunier', 'Mertens', 'Vertonghen', 'Vermaelen', 'Carrasco', 'Castagne'],
#         'England': ['Kane', 'Sterling', 'Stones','Rice', 'Henderson', 'Grealish', 'Mount', 'Trippier', 'Phillips', 'Walker'],
#         'Spain': ['Morata', 'Jordi Alba','Ferran Torres', 'Sergio Busquets','Sarabia','Laporte', 'Pedri', 'Koke', 'Gerard Moreno', 'Unai Simón'],
#         'Italy': ['Bellotti', 'Barella', 'Jorginho','Insigne', 'Immobile', 'Bernardeschi', 'Verratti', 'Bonucci', 'Chiesa', 'Acerbi'],
#         'Switzerland': ['Shaqiri', 'Seferovic', 'Gavranovic', 'Embolo', 'Zuber', 'Akanji', 'Xhaka', 'Mbabu', 'Sommer',
#                         'Elvedi']
#     }
#     if team_name in team_players:
#         player_list = team_players[team_name]
#         df = filter_data_for_team(df, team_name, player_list)
#         return pivot_data(df)
#     return None
#
# def create_plot(df, title, yaxis_title):
#     fig = px.bar(data_frame=df, x="PlayerSurname", y="MatchID", color="StatsName",
#                  title=title, hover_data=['StatsName', 'value'], text_auto=True)
#     fig.update_layout(yaxis={'title': yaxis_title})
#     return fig
#
# def get_figures(file_path, team_name):
#     df = load_data(file_path)
#     df_prepped = prepare_data(df, team_name)
#     if df_prepped is not None:
#         fig_distribution = create_plot(df_prepped, f"{team_name} Distribution", "Distribution Metrics")
#         fig_disciplanary = create_plot(df_prepped, f"{team_name} Disciplinary", "Disciplinary Metrics")
#         return fig_distribution, fig_disciplanary
#     return None, None
#
#
#
# # Example usage
# file_path = "./EURO_2020_DATA.xlsx"
# team_name = 'Austria'
# fig_distribution, fig_disciplanary = get_figures(file_path, team_name)
# if fig_distribution and fig_disciplanary:
#     fig_distribution.show()
#     fig_disciplanary.show()
#
