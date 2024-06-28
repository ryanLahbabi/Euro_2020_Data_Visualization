import plotly.express as px
import pandas as pd


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import environement


# Load the Excel file
file_path = environement.file_path

# Load the specific sheets into dataframes
""" sheet3_df = pd.read_excel("./EURO_2020_DATA.xlsx", sheet_name='Players stats')
# Display the first few rows and the column names
print("Column Names:", sheet3_df.columns) """

# Load specific columns from the "Players stats" sheet into a dataframe
columns = ['HomeTeamName', 'AwayTeamName', 'PlayerSurname', 'StatsName', 'Value']
sheet3_df = pd.read_excel(file_path, sheet_name='Players stats', usecols=columns)

# Specify the required stats
required_stats = [
    'Total Attempts','Goals scored in open play','Goals on set pieces','Played Time',
]

# Filter the stats within Sheet3 to keep only the required stats
filtered_stats_df = sheet3_df[sheet3_df['StatsName'].isin(required_stats)]

# Remove duplicates if any
filtered_stats_df = filtered_stats_df.drop_duplicates()

# Specify the countries we want to include
required_countries = ['Italy', 'England']

# Filtering the stats to keep only the required countries
filtered_stats_df = filtered_stats_df[filtered_stats_df['HomeTeamName'].isin(required_countries)]


# Convert Played Time to total minutes
def convert_to_minutes(time_obj):
    if pd.isna(time_obj):
        return 0
    return time_obj.hour * 60 + time_obj.minute + time_obj.second / 60

filtered_stats_df.loc[filtered_stats_df['StatsName'] == 'Played Time', 'Value'] = filtered_stats_df[filtered_stats_df['StatsName'] == 'Played Time']['Value'].apply(convert_to_minutes)

# Pivot the DataFrame to have stats as columns
pivot_df = filtered_stats_df.pivot(index=['HomeTeamName', 'AwayTeamName', 'PlayerSurname'],
                                   columns='StatsName',
                                   values='Value').reset_index().fillna(0)

# Filter out unnecessary columns
required_columns = ['HomeTeamName', 'PlayerSurname'] + required_stats
final_df = pivot_df[required_columns]

# Rename columns
final_df.columns = ['HomeTeamName', 'PlayerSurname'] + required_stats


def draw_figure(df, column):
    '''
        Draw a violin plot for a specific column in a dataframe

        Args:
            df: The dataframe to use for the figure
            column: The column used (Min or Age)
        Returns:
            figure based on the dataframe
    '''
    # Add a new column 'HoverInfo' for hover data in the plot
    df['HoverInfo'] = '<b>PlayerSurname:</b> ' + df['PlayerSurname'] + '<br>' + '<b>Total Attempts:</b> ' + df['Total Attempts'].astype(str) + '<br>' + '<b>Goals scored in open play:</b> ' + df['Goals scored in open play'].astype(str) + '<br>' + '<b>Played Time:</b> ' + df['Played Time'].astype(str)
    
    # Create a violin plot with hover info and return the figure
    fig = px.violin(df, color="HomeTeamName", x="HomeTeamName", y=column, box=True, points="all",
                 title=f"Violin Plot - {column} per Team", 
                 hover_data={"HoverInfo": "|%{customdata[0]}"})
    fig.update_traces(hovertemplate='<br>%{customdata[0]}<extra></extra>')
    fig.update_layout(height=600,
                      legend=dict(title='<span style="font-size: 18px"><b>Squad</b></span>',
                                  font_size=13)
    )
    return fig


def prep_data_violin():
    '''
        Prepare data for violin plot

        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    
    # Filtering out unnecessary columns
    required_columns = ['HomeTeamName', 'PlayerSurname'] + required_stats
    final_df = pivot_df[required_columns]

    final_df.columns = ['HomeTeamName', 'PlayerSurname'] + required_stats

    """  # Display the final DataFrame
    print('Data after selection of the required columns', final_df) """

    return final_df

 