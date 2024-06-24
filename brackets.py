import plotly.graph_objects as go
import pandas as pd
import environement
from datetime import datetime




file_path = environement.file_path


# Define the matches and results
# Load specific columns from the "Players stats" sheet into a dataframe
columns = [ 'MatchMinute', 'DateandTimeCET', 'HomeTeamName', 'AwayTeamName', 'ScoreHome', 'ScoreAway', 'RoundName']

sheet3_df = pd.read_excel(file_path, sheet_name='Match information', usecols=columns)

for column in columns:
    if column not in sheet3_df.columns:
        raise KeyError(f"Column '{column}' not found in the Excel sheet")
# Filter the stats within Sheet3 to keep only the required stats
filtered_stats_df = sheet3_df[sheet3_df['RoundName'] != 'final tournament']

# Remove duplicates if any
filtered_stats_df = filtered_stats_df.drop_duplicates()


def generate_bracket():
    matches = []
    for _, row in filtered_stats_df.iterrows():
        match = {
            "round": row['RoundName'],
            "date": row['DateandTimeCET'],    
            "match duration": row['MatchMinute'],
            "team1": row['HomeTeamName'][:3].upper(),
            "score1": row['ScoreHome'],
            "team2": row['AwayTeamName'][:3].upper(),
            "score2": row['ScoreAway'],
        }
        matches.append(match)
    


    # Create the plot
    fig = go.Figure()

    # Path to the directory containing flag images
    flag_dir = "/path/to/flag_images/"
    background_image = './euro_background.png'

    # Define the coordinates for the matches
    coordinates = {
        "eighth finals": 1,
        "quarter finals": 2,
        "semi finals": 3,
        "final": 4
    }

    # Assign y coordinates to each match manually
    y_coords = {
        "eighth finals": [6, 4, 5, 3, 2, 1, 7, 8],  # Swapped positions of ITA-AUS and NET-CZE
        "quarter finals": [1, 3, 5, 7],
        "semi finals": [2, 6],
        "final": [4]
    }

    team_positions = {}
    # Add matches to the plot
    for match in matches:
        x = coordinates[match["round"]]
        y = y_coords[match["round"]].pop(0)
        hovertext = f"{match['round'].capitalize()}<br>{match['team1']} {match['score1']} - {match['score2']} {match['team2']}"
        if "penalties" in match:
            hovertext += f"<br>Penalties: {match['penalties']}"
        date = datetime.strptime(match['date'], '%Y-%m-%dT%H:%M:%S')
        hovertext += f"<br>Date: {date.strftime("%B %d, %Y, %H:%M")}"  
        hovertext += f"<br>Match Duration: {match['match duration']}"



        fig.add_shape(
            type="rect",
            x0=x - 0.2,
            y0=y - 0.2,
            x1=x + 0.2,
            y1=y + 0.2,
            line=dict(color="RoyalBlue"),
            fillcolor="LightSkyBlue",
            opacity=0.5  # Vous pouvez ajuster ce nombre entre 0 (transparent) et 1 (opaque)
        )

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            text=f"{match['team1']} {match['score1']} - {match['score2']} {match['team2']}",
            hovertemplate=hovertext,
            mode='text',
            textposition='top center',
            name= "",
            showlegend=False  

        ))

        # Add team positions for line drawing
        if match["team1"] not in team_positions:
            team_positions[match["team1"]] = []
        if match["team2"] not in team_positions:
            team_positions[match["team2"]] = []

        team_positions[match["team1"]].append((x, y))
        team_positions[match["team2"]].append((x, y))

    # Add lines between matches to show the progression of teams
    for team, positions in team_positions.items():
        for i in range(len(positions) - 1):
            x_start, y_start = positions[i]
            x_end, y_end = positions[i + 1]
            fig.add_trace(go.Scatter(
                x=[x_start + 0.2, x_end - 0.2],
                y=[y_start, y_end],
                mode='lines',
                line=dict(color="RoyalBlue"),
                showlegend=False,
                  name=f"{match['round']} - {match['team1']} vs {match['team2']}"  # Custom name

            ))

        fig.add_layout_image(
            dict(
                xref="x",
                yref="y",
                x=x - 0.3,
                y=y,
                sizex=0.1,
                sizey=0.1,
                xanchor="center",
                yanchor="middle"
            )
        )

        fig.add_layout_image(
            dict(
                xref="x",
                yref="y",
                x=x + 0.3,
                y=y,
                sizex=0.1,
                sizey=0.1,
                xanchor="center",
                yanchor="middle"
            )
        )

    # Add background image
    fig.add_layout_image(
        dict(
            source=background_image,
            xref="paper",
            yref="paper",
            x=0,
            y=1,
            sizex=1,
            sizey=1,
            xanchor="left",
            yanchor="top",
            layer="above"
        )
    )

    fig.update_layout(
        title="Tournament Bracket",
        xaxis_title="Round",
        yaxis_title="Matches",
        xaxis=dict(
            tickmode='array',
            tickvals=list(coordinates.values()),
            ticktext=[round.capitalize() for round in coordinates.keys()]
        ),
        yaxis=dict(
            tickmode='linear',
            tick0=1,
            dtick=1,
            range=[0.5, 8.5]
        ),
        showlegend=False
    )
    return fig

fig = generate_bracket()
fig.show()
