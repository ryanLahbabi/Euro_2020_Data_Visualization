# line_up_chart.py

import pandas as pd
import plotly.graph_objects as go

def create_lineup_chart(team_name):
    file_path = 'EURO_2020_DATA.xlsx'
    xls = pd.ExcelFile(file_path)
    line_ups_df = pd.read_excel(xls, 'Line-ups')
    
    team_data = line_ups_df[line_ups_df['Country'] == team_name]
    
    fig = go.Figure()
    
    roles = ['goalkeepers', 'defenders', 'midfields', 'forwards']
    for role in roles:
        role_data = team_data[team_data['Role'] == role]
        for _, player in role_data.iterrows():
            fig.add_trace(go.Scatter(
                x=[role],
                y=[player['JerseyNumber']],
                text=player['JerseyName'],
                mode='markers+text',
                textposition='top center'
            ))

    fig.update_layout(title=f'{team_name} Lineup', xaxis_title='Role', yaxis_title='Jersey Number')
    return fig
