import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import environement


# DATA LOADING AND PROCESSING

# Load the Excel file
file_path = environement.file_path

# Variable definitions


# Specify the countries you want to include
teams = ['Italy', 'England', 'Spain', 'Belgium', 'Austria', 'Switzerland']


# Load specific columns from the "Players stats" sheet into a dataframe
columns = ['MatchID','TeamName', 'StatsName', 'Value']
sheet4_df = pd.read_excel(file_path, sheet_name='Match Stats', usecols=columns)


# Specify the required stats
required_stats = [
    'Goals scored', 'Goals scored in open play', 'Goals on penalty phase', 'Goals on set pieces', 'Goals on corner ', 
    'Goals scored on penalty ', 'Saves', 'Goals conceded', 'Own-goals', 'Saves on penalty', 'Punches',
]




categories_goal = ['Goals scored','Goals scored in open play','Goals on penalty phase','Goals on set pieces','Goals on corner ','Goals scored on penalty ' ]
categories_goal_keep= ['Saves', 'Goals conceded', 'Own-goals', 'Saves on penalty', 'Punches' ]
                                  
# Filter the stats to keep only the required countries
filtered_stats_df = sheet4_df[sheet4_df['TeamName'].isin(teams)]



# Pivot the DataFrame to have stats as columns
pivot_df = filtered_stats_df.pivot(index=['MatchID','TeamName'],
                                   columns='StatsName',
                                   values='Value').reset_index().fillna(0)

# Filter out unnecessary columns
required_columns = ['MatchID', 'TeamName'] + required_stats
final_df = pivot_df[required_columns]

# Rename columns
final_df.columns = ['MatchID', 'TeamName'] + required_stats


def prep_data_goal(df_goal):
    '''
        From the goals datasets, calculate the six goals-related stats used for the radar chart
        Args:
            df_goal: the dataset of the goals stats
        Returns:
            A dictionnary containing the name of the country as a key and the corresponding goals stats used in the goals radarchart
    '''
    
    goals_scored=df_goal.groupby('TeamName')['Goals scored'].sum().to_list()
    goals_open_play=df_goal.groupby('TeamName')['Goals scored in open play'].sum().to_list()
    goals_penalty_phase=df_goal.groupby('TeamName')['Goals on penalty phase'].sum().to_list()
    goals_set_pieces=df_goal.groupby('TeamName')['Goals on set pieces'].sum().to_list()
    goals_corner=df_goal.groupby('TeamName')['Goals on corner '].sum().to_list()
    goals_penalty=df_goal.groupby('TeamName')['Goals scored on penalty '].sum().to_list()



   
    #int_game,tkl_game,clr_game,fouls_game,recov_game,aerial_game=divide_playingtime(inter),divide_playingtime(tkl),divide_playingtime(clr),divide_playingtime(fouls),divide_playingtime(recoveries),divide_playingtime(aerialsDuelswon)

    #Creation of the dictionary containing the stats for each team
    dict_country={}
    for i in range (len(teams)):
        country=teams[i]
        dict_country[country]=  [goals_scored[i],goals_open_play[i],goals_penalty_phase[i],goals_set_pieces[i],goals_corner[i],goals_penalty[i]]
        
    #Sort the dictionnary to have Morocco first
    #dict_country_sorted = dict(sorted(dict_country.items(), key=lambda x: x[0], reverse=True))
    
    # Custom sorting function to prioritize Italy
    def sort_key(item):
        return (item[0] != 'Italy', item[0])
    
    # Sort the dictionary to have Italy first
    dict_country_sorted = dict(sorted(dict_country.items(), key=sort_key))
    
    return dict_country_sorted


def prep_data_goalKeeping(df_goal):
    '''
        From the goals datasets, calculate the six goals-related stats used for the radar chart
        Args:
            df_goal: the dataset of the goals stats
        Returns:
            A dictionnary containing the name of the country as a key and the corresponding goals stats used in the goals radarchart
    '''
    
    saves=df_goal.groupby('TeamName')['Saves'].sum().to_list()
    goals_conced=df_goal.groupby('TeamName')['Goals conceded'].sum().to_list()
    own_goals=df_goal.groupby('TeamName')['Own-goals'].sum().to_list()
    saves_penalty=df_goal.groupby('TeamName')['Saves on penalty'].sum().to_list()
    punches=df_goal.groupby('TeamName')['Punches'].sum().to_list()
    
   
    #int_game,tkl_game,clr_game,fouls_game,recov_game,aerial_game=divide_playingtime(inter),divide_playingtime(tkl),divide_playingtime(clr),divide_playingtime(fouls),divide_playingtime(recoveries),divide_playingtime(aerialsDuelswon)

    #Creation of the dictionary containing the stats for each team
    dict_country={}
    for i in range (len(teams)):
        country=teams[i]
        dict_country[country]=  [saves[i],goals_conced[i],own_goals[i],saves_penalty[i],punches[i]]
        
    #Sort the dictionnary to have Morocco first
    #dict_country_sorted = dict(sorted(dict_country.items(), key=lambda x: x[0], reverse=True))
    
    # Custom sorting function to prioritize Italy
    def sort_key(item):
        return (item[0] != 'Italy', item[0])
    
    # Sort the dictionary to have Italy first
    dict_country_sorted = dict(sorted(dict_country.items(), key=sort_key))
    
    return dict_country_sorted



def get_radar_figure(team_data, categories, type):
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
        title=("Goals performance" if type == 'goals' else "Goals keeping performance"),
        polar=dict(
            radialaxis=dict(visible=True, linecolor='rgba(0,0,0,0.4)', gridcolor='rgba(0,0,0,0.1)')
        ),
        hovermode='closest',
        legend=dict(
            title='<span style="font-size: 18px"><b>Teams</b></span> <br> (<span style="font-size: 14px"><i>Click on a team to select it or remove it</i>)</span>',
            orientation='v',
            yanchor='top',
            y=(1 if type == 'goals' else 1.26),
            xanchor='right',
            x=(1 if type == 'goals' else 1.7),
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
 dict_country_goal = prep_data_goal(final_df)
 dict_country_goal_keep = prep_data_goalKeeping(final_df)
 fig_goal = get_radar_figure(dict_country_goal, categories_goal, 'goals')
 fig_goal_keep = get_radar_figure(dict_country_goal_keep, categories_goal_keep, 'goals_keep')
 return fig_goal, fig_goal_keep


