import pandas as pd
import plotly.graph_objects as go
import environement

def create_lineup_chart(team_name, selected_roles):
    file_path = environement.file_path
    xls = pd.ExcelFile(file_path)
    line_ups_df = pd.read_excel(xls, 'Line-ups')
    
    is_pitch_filter = line_ups_df['IsPitch']
    
    if team_name == 'Italy':
        match_filter = ((line_ups_df['HomeTeamName'] == 'Italy') & (line_ups_df['AwayTeamName'] == 'England')) | \
                       ((line_ups_df['HomeTeamName'] == 'England') & (line_ups_df['AwayTeamName'] == 'Italy'))
        opponent = 'England'
    else:
        match_filter = ((line_ups_df['HomeTeamName'] == 'Italy') | (line_ups_df['AwayTeamName'] == 'Italy')) & \
                       ((line_ups_df['HomeTeamName'] == team_name) | (line_ups_df['AwayTeamName'] == team_name))
        opponent = 'Italy'
    
    team_data = line_ups_df[match_filter & is_pitch_filter & (line_ups_df['Country'] == team_name) & (line_ups_df['Role'].isin(selected_roles))]
    
    fig = go.Figure()
    
    roles = ['goalkeepers', 'defenders', 'midfielders', 'forwards']
    role_colors = {
        'goalkeepers': 'rgba(216, 191, 216, 0.6)',
        'defenders': 'rgba(173, 216, 230, 0.6)',
        'midfielders': 'rgba(144, 238, 144, 0.5)',
        'forwards': 'rgba(255, 0, 0, 0.6)'
    }
    
    role_positions = {role: idx*2 for idx, role in enumerate(roles, 1)}
    max_y_pos = 0

    for role in roles:
        role_data = team_data[team_data['Role'] == role]
        num_players = len(role_data)

        if num_players > 0:
            y_positions = [i*5 for i in range(num_players)]
            y_mid = (max(y_positions) + min(y_positions)) / 2
            y_positions = [y - y_mid for y in y_positions]
            max_y_pos = max(max_y_pos, max(y_positions, default=0))

        
            for y_pos, (_, player) in zip(y_positions, role_data.iterrows()):
                player_name = player['JerseyName']
                if player['IsCaptain'] == True:
                    player_name += " (C.)"
                fig.add_trace(go.Scatter(
                    x=[role_positions[role]],
                    y=[y_pos],
                    text=str(int(player['JerseyNumber'])),
                    mode='markers+text',
                    textposition='middle center',
                    marker=dict(
                        size=40,
                        color=role_colors[role],
                        line=dict(width=2, color='white')
                    ),
                    hovertemplate=f'<b>Player:</b> {player["OfficialName"]} {player["JerseyName"]}<br><b>Jersey Number:</b> {int(player["JerseyNumber"])}<extra></extra>'
                ))
                fig.add_annotation(
                    x=role_positions[role],
                    y=y_pos - 2.5,
                    text=player_name,
                    showarrow=False,
                    font=dict(size=12, color='black'),
                    align='center'
                )

    fig.update_layout(
        plot_bgcolor='green'
    )

    fig.update_layout(
        title=f'{team_name} Lineup vs {opponent}', 
        xaxis=dict(title='Role', tickvals=list(role_positions.values()), ticktext=roles, range=[0, max(role_positions.values()) + 2]),
        yaxis=dict(title='Players', tickvals=[], showgrid=False, range=[-max_y_pos-3, max_y_pos+3]),
        showlegend=False,
        images=[dict(
            source='https://i.pinimg.com/736x/5f/ec/fb/5fecfb401295071c3b8bab2477999f96.jpg',
            xref="x",
            yref="y",
            x=0,
            y=max_y_pos + 5,
            sizex=max(role_positions.values()) + 2,
            sizey=(max_y_pos + 5) * 2,
            sizing="stretch",
            opacity=0.5,
            layer="below"
        )]
    )
    return fig

