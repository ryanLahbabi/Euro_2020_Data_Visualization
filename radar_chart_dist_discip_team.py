import plotly.graph_objects as go
import pandas as pd
import template
import environement


# DATA LOADING AND PROCESSING

# Load the Excel file
file_path = environement.file_path

# Variable definitions


# Specify the countries we want to include
teams = ['Italy', 'England', 'Spain', 'Belgium', 'Austria', 'Switzerland']


# Load specific columns from the "Players stats" sheet into a dataframe
columns = ['MatchID','TeamName', 'StatsName', 'Value']
sheet4_df = pd.read_excel(file_path, sheet_name='Match Stats', usecols=columns)

# Specifying the required stats


required_stats = [
    'Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards', 'Goals conceded', 
    'Own-goals', 'Saves on penalty', 'Saves', 'Punches', 'Tackles', 'Tackles lost', 'Blocks',
    'Recovered balls', 'Assists', 'Dribbling', 'Corners', 'Offsides', 'Clearances', 'Goals scored on penalty ', 
    'Passes attempted','Passes completed','Free kicks on goal ','Crosses attempted','Crosses completed'
]


categories_dist= ['Passes attempted','Passes completed','Crosses attempted','Crosses completed','Free kicks on goal ']
categories_discip= ['Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards']
                                  
# Filter the stats to keep only the required countries
filtered_stats_df = sheet4_df[sheet4_df['TeamName'].isin(teams)]


# Pivot the DataFrame to have stats as columns
pivot_df = filtered_stats_df.pivot(index=['MatchID','TeamName'],
                                   columns='StatsName',
                                   values='Value').reset_index().fillna(0)

# Filter out unnecessary columns
required_columns = ['MatchID', 'TeamName'] + required_stats
final_df = pivot_df[required_columns]

# Renaming columns
final_df.columns = ['MatchID', 'TeamName'] + required_stats




def prep_data_distribution(final_df):
    '''
        From the two defensive datasets, calculate the six defensives stats used for the radar chart
        Args:
            dfmisc: the dataset of miscellaneous stats
            df_def: the dataset of the defensive stats
        Returns:
            A dictionnary containing the name of the country as a key and the corresponding defensive stats used in the defensive radarchart
    '''
    
    passes_at=final_df.groupby('TeamName')['Passes attempted'].sum().to_list()
    passes_cp=final_df.groupby('TeamName')['Passes completed'].sum().to_list()
    crosses_at=final_df.groupby('TeamName')['Crosses attempted'].sum().to_list()
    crosses_cp=final_df.groupby('TeamName')['Crosses completed'].sum().to_list()
    free_kicks=final_df.groupby('TeamName')['Free kicks on goal '].sum().to_list()


    #Creation of the dictionary containing the stats for each team
    dict_country={}
    for i in range (len(teams)):
        country=teams[i]
        dict_country[country]=  [passes_at[i],passes_cp[i],crosses_at[i], crosses_cp[i],free_kicks[i]]
        
    
    # Custom sorting function to prioritize Italy
    def sort_key(item):
        return (item[0] != 'Italy', item[0])
    
    # Sort the dictionary to have Italy first
    dict_country_sorted = dict(sorted(dict_country.items(), key=sort_key))
    
    return dict_country_sorted


def prep_data_discip(final_df):
    '''
        From the three possession datasets, calculate the four possession stats used for the radar chart
        Args:
            df_passing: the dataset of passing stats
            df_possession: the dataset of the possession stats
            df_scorefixtures: the dataset of the scorefixtures stats
        Returns:
            A dictionnary containing the name of the country as a key and the corresponding stats used in the possession radarchart
    '''
    

    categories_discip= ['Fouls committed', 'Yellow cards', 'Fouls suffered', 'Red cards']


    Fouls_com=final_df.groupby('TeamName')['Fouls committed'].sum().to_list()
    Yellow_c=final_df.groupby('TeamName')['Yellow cards'].sum().to_list()
    Fouls_s=final_df.groupby('TeamName')['Fouls suffered'].sum().to_list()
    Red_c=final_df.groupby('TeamName')['Red cards'].sum().to_list()
    

    dict_country={}
    for i in range (len(teams)):
        country = teams[i]
        dict_country[country] = [Fouls_com[i],Yellow_c[i],Fouls_s[i],Red_c[i]]
        
    # Custom sorting function to prioritize Italy
    def sort_key(item):
        return (item[0] != 'Italy', item[0])
    
    # Sort the dictionary to have Italy first
    dict_country_sorted = dict(sorted(dict_country.items(), key=sort_key))
    
    return dict_country_sorted


def get_radar_figure(team_data,categories,type):

    """
    Create the radar chart (defense or possession) from the dictionnary created above, it fills only Morocco ont the radar
        Args:
            categories: List of the corresponding categories for the radar chart (defense or possession)
            type: defense or possession
            team_data: Dictionary with team names as keys and corresponding data as values

        Returns:
            A plotly Figure with the radar chart
    """
    fig = go.Figure()
    default_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3']

    for i, team_name in enumerate(team_data.keys()):
        hovertemplate = '<span style="color: white"><b>{}</b><br>{}: {}</span><extra></extra>'.format(team_name, '%{theta}', '%{r}')
        trace = go.Scatterpolar(
            r=team_data[team_name] + [team_data[team_name][0]],
            theta=categories + [categories[0]],
            fill=('toself' if team_name == 'Italy' else 'none'),
            hoveron='points+fills',
            line=dict(
                shape='spline',
                width=3,
            ),
            hoverlabel=dict(
                bgcolor=default_colors[i % len(default_colors)]
            ),
            name=team_name,
            marker=dict(size=8),
            hovertemplate=hovertemplate,
        )
        fig.add_trace(trace)

    fig.update_layout(
        title=("Total Team Distribution Actions"if type=='distribution' else "Total Team Disciplinary"),
        polar=dict(
            radialaxis=dict(visible=True,linecolor='rgba(0,0,0,0.4)',gridcolor='rgba(0,0,0,0.1)')
        ),
        hovermode='closest',
        legend=dict(
            title='<span style="font-size: 18px"><b>Teams</b></span> <br> (<span style="font-size: 14px"><i>Click on a team to select it or remove it</i>)</span>',
            orientation='v',
            yanchor='top',
            y=(1 if type=='defense' else 1.26),
            xanchor='right',
            x=(1 if type=='defense' else 1.7),
            font=dict(
                size=13  
            )
        )
    )

    fig.update_polars(bgcolor='rgba(0,0,0, 0.1)')
    fig.update_traces(hoveron="points")

    return fig




def get_fig():
  # Preprocess and create the radar figure
  dict_country_dist= prep_data_distribution(final_df)
  dict_country_disc= prep_data_discip(final_df)
  fig_dist=get_radar_figure(dict_country_dist,categories_dist,'distribution')
  fig_disc=get_radar_figure(dict_country_disc,categories_discip,'discipline')
  return fig_dist,fig_disc
 