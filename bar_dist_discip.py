import pandas as pd
import plotly.express as px

required_stats_distribution = [
    'Passes attempted', 'Passes completed', 'Free kicks on goal ', 'Crosses attempted', 'Crosses completed',
]

required_stats_disciplinary = [
    'Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards'
]




file_path = "./EURO_2020_DATA.xlsx"
team_name = 'Austria'


def load_data(file_path):
    columns = ['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime', 'StatsName', 'Value']
    return pd.read_excel(file_path, sheet_name='Players stats', usecols=columns)

def filter_data_for_team_distribution(df, team_name, player_list):
    # Filter the stats within Sheet3 to keep only the required stats and for the specified team
    df = df[df['StatsName'].isin(required_stats_distribution) & df['PlayerSurname'].isin(player_list)]
    return df.drop_duplicates()

def filter_data_for_team_disciplinary(df, team_name, player_list):
    # Filter the stats within Sheet3 to keep only the required stats and for the specified team
    df = df[df['StatsName'].isin(required_stats_disciplinary) & df['PlayerSurname'].isin(player_list)]
    return df.drop_duplicates()

def pivot_data(df):
    pivot_df = df.pivot(index=['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime'],
                        columns='StatsName', values='Value').reset_index().fillna(0)
    return pivot_df

def prepare_data(df, team_name):
    # Assuming a dictionary mapping teams to players
    team_players = {
        'Austria': ['Baumgartner', 'Lainer', 'Gregoritsch', 'Sabitzer', 'Arnautovic', 'Kalajdzic', 'Trimmel', 'Alaba', 'Schlager', 'Dragovic'],
        'Belgium': ['Lukaku', 'Hazard', 'Vanaken', 'De Bruyne', 'Meunier', 'Mertens', 'Vertonghen', 'Vermaelen', 'Carrasco', 'Castagne'],
        'England': ['Kane', 'Sterling', 'Stones','Rice', 'Henderson', 'Grealish', 'Mount', 'Trippier', 'Phillips', 'Walker'],
        'Spain': ['Morata', 'Jordi Alba','Ferran Torres', 'Sergio Busquets','Sarabia','Laporte', 'Pedri', 'Koke', 'Gerard Moreno', 'Unai Simón'],
        'Italy': ['Bellotti', 'Barella', 'Jorginho','Insigne', 'Immobile', 'Bernardeschi', 'Verratti', 'Bonucci', 'Chiesa', 'Acerbi'],
        'Switzerland': ['Shaqiri', 'Seferovic', 'Gavranovic', 'Embolo', 'Zuber', 'Akanji', 'Xhaka', 'Mbabu', 'Sommer',
                        'Elvedi']
    }
    if team_name in team_players:
        player_list = team_players[team_name]

        df_distribution = filter_data_for_team_distribution(df, team_name, player_list)
        df_disciplinary = filter_data_for_team_disciplinary(df, team_name, player_list)

        return aggregate_data_distribution(pivot_data(df_distribution)), aggregate_data_disciplinary(pivot_data(df_disciplinary))
    return None


def aggregate_data_distribution(df):
    # Agréger les données par joueur
    aggregated_df = df.groupby('PlayerSurname').sum().reset_index()
    aggregated_df['Total'] = aggregated_df[required_stats_distribution].sum(axis=1)

    df_distribution = aggregated_df.sort_values('Total', ascending=False)
    df_distribution.drop('Total', axis=1, inplace=True)

    return df_distribution

def aggregate_data_disciplinary(df):
    # Agréger les données par joueur
    aggregated_df = df.groupby('PlayerSurname').sum().reset_index()
    aggregated_df['Total'] = aggregated_df[required_stats_disciplinary].sum(axis=1)

    df_distribution = aggregated_df.sort_values('Total', ascending=False)
    df_distribution.drop('Total', axis=1, inplace=True)

    return df_distribution


def create_plot(df, title, yaxis_title):
    df_melted = df.melt(id_vars=['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime'], var_name='StatsName', value_name='Value')
    fig = px.bar(data_frame=df_melted, x="PlayerSurname", y="Value", color="StatsName",
                 title=title, hover_data=['StatsName', 'Value'], text_auto=True)
    fig.update_layout(yaxis={'title': yaxis_title})
    return fig

def get_fig(team_name):
    df = load_data("./EURO_2020_DATA.xlsx")
    df_prepped_distribution, df_prepped_disciplinary = prepare_data(df, team_name)
    fig_distribution = create_plot(df_prepped_distribution, f"{team_name} Distribution", "Distribution Metrics")
    fig_disciplanary = create_plot(df_prepped_disciplinary, f"{team_name} Disciplinary", "Disciplinary Metrics")
    return fig_distribution, fig_disciplanary

