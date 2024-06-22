import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load the Excel file
file_path ="./EURO_2020_DATA.xlsx"

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
    'Passes attempted','Passes completed','Free kicks on goal ','Crosses attempted','Crosses completed',
]

# Filter the stats within Sheet3 to keep only the required stats
filtered_stats_df = sheet3_df[sheet3_df['StatsName'].isin(required_stats)]

# Remove duplicates if any
filtered_stats_df = filtered_stats_df.drop_duplicates()

# Specify the countries you want to include
required_countries = ['Spain']

# Filter the stats to keep only the required countries
filtered_stats_df = filtered_stats_df[filtered_stats_df['HomeTeamName'].isin(required_countries)]

# Display the filtered dataframe
print('-------------------------------------------')
print('Filtered part:')



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
print(final_df)



def prep_distribution_data(df):
    '''
        Processes the defense data.

        Args:
            df: dataframe to process
        Returns:
            A prepared pandas dataframe containing the offensive data.
    '''

    df = df.groupby('PlayerSurname')[['Passes attempted','Passes completed','Crosses attempted','Crosses completed','Free kicks on goal ']].sum().reset_index()
    df_distribution = df[df['PlayerSurname'].isin(['Morata', 'Jordi Alba','Ferran Torres', 'Sergio Busquets','Sarabia','Laporte', 'Pedri', 'Koke', 'Gerard Moreno', 'Unai Simón'])]


    #df_defense = df_defense(columns={'Recovered balls', "Tackles", 'Clearances', 'Blocks'})
    df_distribution['Total'] = df_distribution[['Passes attempted','Passes completed','Crosses attempted','Crosses completed','Free kicks on goal ']].sum(axis=1)

    df_distribution = df_distribution.sort_values('Total', ascending=False)
    df_distribution.drop('Total', axis=1, inplace=True)

    
    df_dist = pd.melt(df_distribution[['PlayerSurname','Passes attempted','Passes completed','Crosses attempted','Crosses completed','Free kicks on goal ']], id_vars=['PlayerSurname'], var_name='Distribution').copy()
    #df_def["percentages"] = ((df_def["value"] / df_def['value'].groupby(df_def['Player']).transform('sum'))*10000).astype(int) /100
    return df_dist
    

def prep_disciplanary_data(df):
    '''
        Processes the defense data.

        Args:
            df: dataframe to process
        Returns:
            A prepared pandas dataframe containing the offensive data.
    '''

    df = df.groupby('PlayerSurname')[['Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards']].sum().reset_index()
    df_disciplanary = df[df['PlayerSurname'].isin(['Morata', 'Jordi Alba','Ferran Torres', 'Sergio Busquets','Sarabia','Laporte', 'Pedri', 'Koke', 'Gerard Moreno', 'Unai Simón'])]


    df_disciplanary['Total'] = df_disciplanary[['Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards']].sum(axis=1)

    df_disciplanary = df_disciplanary.sort_values('Total', ascending=False)
    df_disciplanary.drop('Total', axis=1, inplace=True)

    
    df_discip = pd.melt(df_disciplanary[['PlayerSurname','Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards']], id_vars=['PlayerSurname'], var_name='Disciplanary').copy()
    #df_def["percentages"] = ((df_def["value"] / df_def['value'].groupby(df_def['Player']).transform('sum'))*10000).astype(int) /100
    return df_discip



    
def create_distribution_plot(df):
    '''
        Generates the barchart from the given offense data.

        Args:
            df: offense dataframe
        Returns:
            The defense figure to be displayed.
    '''
    
    fig = px.bar(data_frame=df, x="PlayerSurname", y="value", color="Distribution",
                title="Spain Distribution", 
                hover_data=["Distribution"],
                text_auto=True)
    

    fig.update_traces(hovertemplate="<b>Player:</b> %{x}<br><b>%{customdata[1]} Completed: </b>%{y} (%{customdata[0]}%)<extra></extra>") 
    fig.update_layout(yaxis={'title': "Distribution"},
                      height=660,
                      legend=dict(title='<span style="font-size: 18px"><b>Defensive Actions</b></span>',
                                  font_size=13)
    )    
    return fig

def create_disciplanary_plot(df):
    '''
        Generates the barchart from the given offense data.

        Args:
            df: offense dataframe
        Returns:
            The defense figure to be displayed.
    '''
    
    
    fig = px.bar(data_frame=df, x="PlayerSurname", y="value", color="Disciplanary",
                title="Spain Disciplinary", 
                hover_data=["Disciplanary"],
                text_auto=True)
    

    fig.update_traces(hovertemplate="<b>Player:</b> %{x}<br><b>%{customdata[1]} Completed: </b>%{y} (%{customdata[0]}%)<extra></extra>") 
    fig.update_layout(yaxis={'title': "Disciplanary"},
                      height=660,
                      legend=dict(title='<span style="font-size: 18px"><b>Disciplanary</b></span>',
                                  font_size=13)
    )    
    return fig


def get_fig():
    '''
        Prepares the data and gets the figures for offense and defense bar charts.

        Returns:
            The offense and defense figures to be displayed.
    '''


    df_distribution_prep =  prep_distribution_data(final_df)
    df_disciplanary_prep =  prep_disciplanary_data(final_df)
    fig_distribution = create_distribution_plot(df_distribution_prep)
    fig_disciplanary = create_disciplanary_plot(df_disciplanary_prep)
    return fig_distribution,fig_disciplanary

