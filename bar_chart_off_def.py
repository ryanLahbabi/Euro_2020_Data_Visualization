import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

required_stats = [
    'Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards', 'Goals conceded',
    'Own-goals', 'Saves on penalty', 'Saves', 'Punches', 'Tackles', 'Tackles lost', 'Blocks',
    'Recovered balls', 'Assists', 'Dribbling', 'Corners', 'Offsides', 'Clearances', 'Goals scored on penalty ',
    'Passes attempted', 'Passes completed', 'Free kicks on goal ', 'Crosses attempted', 'Crosses completed',
]
# Load the Excel file
file_path = "./EURO_2020_DATA.xlsx"

# Load the specific sheets into dataframes
""" sheet3_df = pd.read_excel("./EURO_2020_DATA.xlsx", sheet_name='Players stats')
# Display the first few rows and the column names
print("Column Names:", sheet3_df.columns) """

# Load specific columns from the "Players stats" sheet into a dataframe
columns = ['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime', 'StatsName', 'Value']
sheet3_df = pd.read_excel(file_path, sheet_name='Players stats', usecols=columns)

# Specify the required stats
required_stats = [
    'Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards', 'Goals conceded',
    'Own-goals', 'Saves on penalty', 'Saves', 'Punches', 'Tackles', 'Tackles lost', 'Blocks',
    'Recovered balls', 'Assists', 'Dribbling', 'Corners', 'Offsides', 'Clearances', 'Goals scored on penalty ',
    'Passes attempted', 'Passes completed', 'Free kicks on goal ', 'Crosses attempted', 'Crosses completed'
]

# Filter the stats within Sheet3 to keep only the required stats
filtered_stats_df = sheet3_df[sheet3_df['StatsName'].isin(required_stats)]

# Remove duplicates if any
filtered_stats_df = filtered_stats_df.drop_duplicates()

# Specify the countries you want to include
required_countries = ['Austria', 'Belgium', 'England', 'Italy', 'Spain', 'Switzerland' ]

# Filter the stats to keep only the required countries
filtered_stats_df = filtered_stats_df[filtered_stats_df['HomeTeamName'].isin(required_countries)]

# Display the filtered dataframe
print('-------------------------------------------')
print('Filtered part mon garsssss:')

# Display the filtered dataframe
print(filtered_stats_df)

# Pivot the DataFrame to have stats as columns
pivot_df = filtered_stats_df.pivot(index=['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime'],
                                   columns='StatsName',
                                   values='Value').reset_index().fillna(0)


# Filter out unnecessary columns
required_columns = ['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime'] + required_stats
final_df = pivot_df[required_columns]


# Rename columns
final_df.columns = ['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime'] + required_stats

# Display the final DataFrame
print("WSHHH")
print(final_df)

def prep_offense_data(df, team_name):
    '''
        Processes the offense data for a specific team.

        Args:
            df: DataFrame to process.
            team_name: Name of the team to filter the data for.

        Returns:
            A prepared pandas DataFrame containing the offensive data for the specified team.
    '''
    # Team players mapping
    team_players = {
        'Austria': ['Baumgartner', 'Lainer', 'Gregoritsch', 'Sabitzer', 'Arnautovic', 'Kalajdzic', 'Trimmel', 'Alaba',
                    'Schlager', 'Dragovic'],
        'Belgium': ['Lukaku', 'Hazard', 'Vanaken', 'De Bruyne', 'Meunier', 'Mertens', 'Vertonghen', 'Vermaelen',
                    'Carrasco', 'Castagne'],
        'England': ['Kane', 'Sterling', 'Stones', 'Rice', 'Henderson', 'Grealish', 'Mount', 'Trippier', 'Phillips',
                    'Walker'],
        'Italy': ['Bellotti', 'Barella', 'Jorginho', 'Insigne', 'Immobile', 'Bernardeschi', 'Verratti', 'Bonucci',
                  'Chiesa', 'Acerbi'],
        'Spain': ['Morata', 'Jordi Alba', 'Ferran Torres', 'Sergio Busquets', 'Sarabia', 'Laporte', 'Pedri', 'Koke',
                  'Gerard Moreno', 'Unai Simón'],
        'Switzerland': ['Shaqiri', 'Seferovic', 'Gavranovic', 'Embolo', 'Zuber', 'Akanji', 'Xhaka', 'Mbabu', 'Sommer',
                        'Elvedi']
    }

    # Check if the team is in the dictionary
    if team_name not in team_players:
        return pd.DataFrame()  # Return empty DataFrame if the team is not found

    # Filter data for the selected team
    players = team_players[team_name]
    df_offense = df[df['PlayerSurname'].isin(players)]

    # Group by PlayerSurname and calculate sums for the offensive stats
    df_offense = df_offense.groupby('PlayerSurname')[['Assists', 'Corners', 'Offsides']].sum().reset_index()

    # Calculate total offensive actions
    df_offense['Total'] = df_offense[['Assists', 'Corners', 'Offsides']].sum(axis=1)

    # Melt the DataFrame for easier plotting/analysis later
    df_melted = pd.melt(df_offense, id_vars='PlayerSurname', var_name='Offensive Types', value_name='Value')

    # Calculate percentages for each offensive type per player
    total_values = df_melted.groupby('PlayerSurname')['Value'].transform('sum')
    df_melted['Percentage'] = (df_melted['Value'] / total_values) * 100

    return df_melted

'''
    # Aggregate the data for each player across all matches
    df_offense = df_offense.groupby('PlayerSurname')[['Assists', 'Corners', 'Offsides']].sum().reset_index()


    # Sort and prepare for plotting
    df_offense['Total'] = df_offense[['Assists', 'Corners', 'Offsides']].sum(axis=1)
    df_offense = df_offense.sort_values('Total', ascending=False)
    df_offense.drop('Total', axis=1, inplace=True)

    df_off = pd.melt(df_offense, id_vars=['PlayerSurname'], var_name='Offensive Types').copy()
    return df_off
'''


def prep_defense_data(df):
    '''
        Processes the defense data.

        Args:
            df: dataframe to process
        Returns:
            A prepared pandas dataframe containing the offensive data.
    '''

    df = df.groupby('PlayerSurname')[['Recovered balls', "Tackles", 'Clearances', 'Blocks']].sum().reset_index()
    df_defense = df[df['PlayerSurname'].isin(
        ['Baumgartner', 'Lainer', 'Gregoritsch', 'Sabitzer', 'Arnautovic', 'Kalajdzic', 'Trimmel', 'Alaba', 'Schlager',
         'Dragovic'])]

    # df_defense = df_defense(columns={'Recovered balls', "Tackles", 'Clearances', 'Blocks'})
    df_defense['Total'] = df_defense[['Recovered balls', "Tackles", 'Clearances', 'Blocks']].sum(axis=1)

    df_defense = df_defense.sort_values('Total', ascending=False)
    df_defense.drop('Total', axis=1, inplace=True)

    df_def = pd.melt(df_defense[['PlayerSurname', 'Recovered balls', "Tackles", 'Clearances', 'Blocks']],
                     id_vars=['PlayerSurname'], var_name='Defensive Actions').copy()
    # ------------------------------------Calculate percentages
    total_values = df_def['value'].groupby(df_def['PlayerSurname']).transform('sum')

    non_zero_mask = total_values != 0

    df_def['percentages'] = 0.0
    df_def.loc[non_zero_mask, 'percentages'] = ((df_def['value'][non_zero_mask] / total_values[
        non_zero_mask]) * 10000).astype(int) / 100

    return df_def


def create_offense_plot(df):
    '''
        Generates the barchart from the given offense data.

        Args:
            df: offense dataframe
        Returns:
            The offense figure to be displayed.
    '''
    fig = go.Figure()

    fig = px.bar(data_frame=df, x="PlayerSurname", y="value", color="Offensive Types",
                 title="Austria Offensive Actions",
                 hover_data=["percentages", "Offensive Types"],
                 text_auto=True)

    fig.update_traces(
        hovertemplate="<b>Player:</b> %{x}<br><b>%{customdata[1]} Completed: </b>%{y} (%{customdata[0]}%)<extra></extra>")
    fig.update_layout(yaxis={'title': "Offensive Actions"},
                      height=600,
                      legend=dict(title='<span style="font-size: 18px"><b>Pass Types</b></span>',
                                  font_size=13)
                      )
    return fig


def create_defense_plot(df):
    '''
        Generates the barchart from the given offense data.

        Args:
            df: offense dataframe
        Returns:
            The defense figure to be displayed.
    '''
    """ fig = px.bar(data_frame=df, x="PlayerSurname", y="value", color="Defensive Actions",
                title="Defensive Actions", 
                hover_data=["percentages","Defensive Actions"],
                text_auto=True) """

    fig = px.bar(data_frame=df, x="PlayerSurname", y="value", color="Defensive Actions",
                 title="Austria Defensive Actions",
                 hover_data=["Defensive Actions"],
                 text_auto=True)

    fig.update_traces(
        hovertemplate="<b>Player:</b> %{x}<br><b>%{customdata[1]} Completed: </b>%{y} (%{customdata[0]}%)<extra></extra>")
    fig.update_layout(yaxis={'title': "Defensive Actions"},
                      height=660,
                      legend=dict(title='<span style="font-size: 18px"><b>Defensive Actions</b></span>',
                                  font_size=13)
                      )
    return fig



required_columns = ['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime'] + required_stats
final_df = pivot_df[required_columns]

# Rename columns
final_df.columns = ['MatchID', 'HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'PlayedTime'] + required_stats
def get_fig():
    '''
        Prepares the data and gets the figures for offense and defense bar charts.

        Returns:
            The offense and defense figures to be displayed.
    '''

    df_offense_prep = prep_offense_data(final_df)
    df_defense_prep = prep_defense_data(final_df)

    fig_offense = create_offense_plot(df_offense_prep)
    fig_defense = create_defense_plot(df_defense_prep)

    return fig_offense, fig_defense


