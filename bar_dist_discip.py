import pandas as pd
import plotly.express as px
import environement
import json
import numpy as np
import os

required_stats_distribution = [
    'Passes attempted', 'Passes completed', 'Free kicks on goal ', 'Crosses attempted', 'Crosses completed',
]

required_stats_disciplinary = [
    'Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards'
]

file_path = environement.file_path

def load_data(file_path):
    columns = ['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime', 'StatsName', 'Value']
    return pd.read_excel(file_path, sheet_name='Players stats', usecols=columns)

def filter_data_for_team_distribution(df, team_name, player_list):
    df = df[df['StatsName'].isin(required_stats_distribution) & df['PlayerSurname'].isin(player_list)]
    return df.drop_duplicates()

def filter_data_for_team_disciplinary(df, team_name, player_list):
    df = df[df['StatsName'].isin(required_stats_disciplinary) & df['PlayerSurname'].isin(player_list)]
    return df.drop_duplicates()

def pivot_data(df):
    pivot_df = df.pivot(index=['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime'],
                        columns='StatsName', values='Value').reset_index().fillna(0)
    return pivot_df

def aggregate_data_distribution(df):
    aggregated_df = df.groupby('PlayerSurname').sum().reset_index()
    aggregated_df['Total'] = aggregated_df[required_stats_distribution].sum(axis=1)
    df_distribution = aggregated_df.sort_values('Total', ascending=False)
    df_distribution.drop('Total', axis=1, inplace=True)
    return df_distribution

def aggregate_data_disciplinary(df):
    aggregated_df = df.groupby('PlayerSurname').sum().reset_index()
    aggregated_df['Total'] = aggregated_df[required_stats_disciplinary].sum(axis=1)
    df_distribution = aggregated_df.sort_values('Total', ascending=False)
    df_distribution.drop('Total', axis=1, inplace=True)
    return df_distribution

def create_plot(df, title, yaxis_title):
   # df = df.drop(columns=['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayedTime'])
    df_melted = df.melt(id_vars=['PlayerSurname'], var_name='StatsName', value_name='Value')
    fig = px.bar(data_frame=df_melted, x="PlayerSurname", y="Value", color="StatsName",
                 title=title, hover_data={'StatsName': True, 'Value': True, 'PlayerSurname': False}, text_auto=True)
    fig.update_layout(yaxis={'title': yaxis_title})
    return fig

def convert_ndarray_to_list(fig_dict):
    if isinstance(fig_dict, dict):
        for key, value in fig_dict.items():
            if isinstance(value, np.ndarray):
                fig_dict[key] = value.tolist()
            elif isinstance(value, dict):
                convert_ndarray_to_list(value)
            elif isinstance(value, list):
                for item in value:
                    convert_ndarray_to_list(item)
    return fig_dict

team_players = {
    'Austria': ['Baumgartner', 'Lainer', 'Gregoritsch', 'Sabitzer', 'Arnautovic', 'Kalajdzic', 'Trimmel', 'Alaba', 'Schlager', 'Dragovic'],
    'Belgium': ['Lukaku', 'Hazard', 'Vanaken', 'De Bruyne', 'Meunier', 'Mertens', 'Vertonghen', 'Vermaelen', 'Carrasco', 'Castagne'],
    'England': ['Kane', 'Sterling', 'Stones','Rice', 'Henderson', 'Grealish', 'Mount', 'Trippier', 'Phillips', 'Walker'],
    'Spain': ['Morata', 'Jordi Alba','Ferran Torres', 'Sergio Busquets','Sarabia','Laporte', 'Pedri', 'Koke', 'Gerard Moreno', 'Unai Simón'],
    'Italy': ['Bellotti', 'Barella', 'Jorginho','Insigne', 'Immobile', 'Bernardeschi', 'Verratti', 'Bonucci', 'Chiesa', 'Acerbi'],
    'Switzerland': ['Shaqiri', 'Seferovic', 'Gavranovic', 'Embolo', 'Zuber', 'Akanji', 'Xhaka', 'Mbabu', 'Sommer', 'Elvedi']
}

df = load_data(file_path)

for team_name, players in team_players.items():
    df_distribution = filter_data_for_team_distribution(df, team_name, players)
    df_disciplinary = filter_data_for_team_disciplinary(df, team_name, players)

    df_distribution = aggregate_data_distribution(pivot_data(df_distribution))
    df_disciplinary = aggregate_data_disciplinary(pivot_data(df_disciplinary))

    fig_distribution = create_plot(df_distribution, f"{team_name} Distribution", "Distribution Metrics")
    fig_disciplinary = create_plot(df_disciplinary, f"{team_name} Disciplinary", "Disciplinary Metrics")

    fig_distribution_dict = fig_distribution.to_dict()
    fig_disciplinary_dict = fig_disciplinary.to_dict()

    # Convert any numpy ndarrays to lists
    fig_distribution_dict = convert_ndarray_to_list(fig_distribution_dict)
    fig_disciplinary_dict = convert_ndarray_to_list(fig_disciplinary_dict)

    file_path_dist_r = f'Euro_2020_Data_Visualization/assets/{team_name}_distribution.json'
    file_path_discip_r = f'Euro_2020_Data_Visualization/assets/{team_name}_disciplinary.json'
    file_path_dist= os.path.abspath(file_path_dist_r)
    file_path_discip = os.path.abspath(file_path_discip_r)
    

    with open(f'f{file_path_dist}', 'w') as f:
        json.dump(fig_distribution_dict, f)
    with open(f'f{file_path_discip}', 'w') as f:
        json.dump(fig_disciplinary_dict, f)
