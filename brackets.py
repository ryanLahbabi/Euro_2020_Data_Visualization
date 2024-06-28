import plotly.graph_objects as go
import pandas as pd
import environement
from datetime import datetime
from constants import (AUSTRIA_IMAGE, ITALY_IMAGE, SPAIN_IMAGE, BELGIUM_IMAGE, SWITZERLAND_IMAGE, GERMANY_IMAGE, CZE_REPUBLIC_IMAGE,
                       DENMARK_IMAGE, WALES_IMAGE, PORTUGAL_IMAGE, FRANCE_IMAGE, CROATIA_IMAGE, NETHERLANDS_IMAGE, UKRAINE_IMAGE, SWEDEN_IMAGE, ENGLAND_IMAGE, BACKGROUND_IMAGE)

FILE_PATH = environement.file_path

card_data = {
    ("FRA", "SWI"): {"yellow1": 3, "yellow2": 4, "red1": 0, "red2": 0},
    ("CRO", "SPA"): {"yellow1": 2, "yellow2": 0, "red1": 0, "red2": 0},
    ("BEL", "POR"): {"yellow1": 2, "yellow2": 3, "red1": 0, "red2": 0},
    ("ITA", "AUS"): {"yellow1": 2, "yellow2": 3, "red1": 0, "red2": 0},
    ("WAL", "DEN"): {"yellow1": 4, "yellow2": 0, "red1": 1, "red2": 0},
    ("NET", "CZE"): {"yellow1": 2, "yellow2": 1, "red1": 1, "red2": 0},
    ("SWE", "UKR"): {"yellow1": 2, "yellow2": 2, "red1": 1, "red2": 0},
    ("ENG", "GER"): {"yellow1": 3, "yellow2": 2, "red1": 0, "red2": 0},
    ("SWI", "SPA"): {"yellow1": 2, "yellow2": 1, "red1": 1, "red2": 0},
    ("BEL", "ITA"): {"yellow1": 1, "yellow2": 2, "red1": 0, "red2": 0},
    ("CZE", "DEN"): {"yellow1": 2, "yellow2": 0, "red1": 0, "red2": 0},
    ("UKR", "ENG"): {"yellow1": 0, "yellow2": 0, "red1": 0, "red2": 0},
    ("ITA", "SPA"): {"yellow1": 2, "yellow2": 1, "red1": 0, "red2": 0, "penalty1": 4, "penalty2": 2},
    ("ENG", "DEN"): {"yellow1": 1, "yellow2": 1, "red1": 0, "red2": 0},
    ("ITA", "ENG"): {"yellow1": 5, "yellow2": 1, "red1": 0, "red2": 0,  "penalty1": 3, "penalty2": 2},
}


columns = [ 'MatchMinute', 'DateandTimeCET', 'HomeTeamName', 'AwayTeamName', 'ScoreHome', 'ScoreAway', 'RoundName']

sheet3_df = pd.read_excel(FILE_PATH, sheet_name='Match information', usecols=columns)

for column in columns:
    if column not in sheet3_df.columns:
        raise KeyError(f"Column '{column}' not found in the Excel sheet")
filtered_stats_df = sheet3_df[sheet3_df['RoundName'] != 'final tournament']

filtered_stats_df = filtered_stats_df.drop_duplicates()


def acronym_to_full_name(acronym):
    # Dictionary mapping acronyms to full country names
    country_names = {
        "FRA": "France",
        "SWI": "Switzerland",
        "CRO": "Croatia",
        "SPA": "Spain",
        "BEL": "Belgium",
        "POR": "Portugal",
        "ITA": "Italy",
        "AUS": "Austria",
        "WAL": "Wales",
        "DEN": "Denmark",
        "NET": "Netherlands",
        "CZE": "Czech Republic",
        "SWE": "Sweden",
        "UKR": "Ukraine",
        "ENG": "England",
        "GER": "Germany"
    }

    # Return the full country name or the original acronym if not found
    return country_names.get(acronym, acronym)


def generate_bracket(selected_team=None):
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
    


    fig = go.Figure()


    coordinates = {
        "eighth finals": 1,
        "quarter finals": 2,
        "semi finals": 3,
        "final": 4
    }

    y_coords = {
        "eighth finals": [6, 4, 5, 3, 2, 1, 7, 8],
        "quarter finals": [1, 3, 5, 7],
        "semi finals": [2, 6],
        "final": [4]
    }





    team_positions = {}

    for match in matches:
        x = coordinates[match["round"]]
        y = y_coords[match["round"]].pop(0)
        date = datetime.strptime(match['date'], '%Y-%m-%dT%H:%M:%S')
        
        hovertext = f"""
        <b>{match['round'].capitalize()}</b><br>
        <b>{acronym_to_full_name(match['team1'])}</b> {match['score1']} - {match['score2']} <b>{acronym_to_full_name(match['team2'])}</b><br>
        <b>Date:</b> {date.strftime('%B %d, %Y, %H:%M')}<br>
        <b>Match Duration:</b> {match['match duration']}<br>
        <b>Yellow Cards ({match['team1']}):</b> {card_data[(match['team1'], match['team2'])]['yellow1']} |
        <b>Yellow Cards ({match['team2']}):</b> {card_data[(match['team1'], match['team2'])]['yellow2']}<br>
        <b>Red Cards ({match['team1']}):</b> {card_data[(match['team1'], match['team2'])]['red1']} |
        <b>Red Cards ({match['team2']}):</b> {card_data[(match['team1'], match['team2'])]['red2']}
        """
        if "penalty1" in card_data.get((match['team1'], match['team2']), {}):
            hovertext += f"""
            <br><b>Penalties ({match['team1']}):</b> {card_data[(match['team1'], match['team2'])]['penalty1']}<br>
            <b>Penalties ({match['team2']}):</b> {card_data[(match['team1'], match['team2'])]['penalty2']}
            """






        fig.add_shape(
            type="rect",
            x0=x - 0.2,
            y0=y - 0.2,
            x1=x + 0.2,
            y1=y + 0.2,
            line=dict(color="RoyalBlue"),
            fillcolor="LightSkyBlue",
            opacity=0.5,
        )

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            text=hovertext,
            hoverinfo="text",
            mode='markers',
            marker=dict(
                size=60,
                opacity=0
            ),
            showlegend=False
        ))

        fig.update_layout(
            xaxis_showgrid=False,
            yaxis_showgrid=False,
        )

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            text=f"{match['team1']} {match['score1']} - {match['score2']} {match['team2']}",
            hovertemplate=hovertext,
            mode='text',
            textposition='top center',
            name= "",
            showlegend=False,
        )
        )

        if match["team1"] not in team_positions:
            team_positions[match["team1"]] = []
        if match["team2"] not in team_positions:
            team_positions[match["team2"]] = []

        team_positions[match["team1"]].append((x, y))
        team_positions[match["team2"]].append((x, y))

    for team, positions in team_positions.items():
        for i in range(len(positions) - 1):
            x_start, y_start = positions[i]
            x_end, y_end = positions[i + 1]
            line_color = "RoyalBlue"
            if selected_team and team == selected_team:
                line_color = "red"
            fig.add_trace(go.Scatter(
                x=[x_start + 0.2, x_end - 0.2],
                y=[y_start, y_end],
                mode='lines',
                line=dict(color=line_color),
                showlegend=False,
                name=f"{match['round']} - {match['team1']} vs {match['team2']}",
                hoverinfo='none'  # Disable hover for the lines
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

    fig.add_layout_image(
        dict(
            source= BACKGROUND_IMAGE,
            xref="paper",
            yref="paper",
            x=0,
            y=1.4,
            sizex=1,
            sizey=1.4,
            xanchor="left",
            yanchor="top",
            layer="below",
            opacity=0.3,
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
        showlegend=False,
    )
    '''
     Following code is to declare the flags and adjust their position
    '''
    # Round of 16
    fig.add_layout_image(
        dict(
            source=SWEDEN_IMAGE,
            x=0.015, y=0.95,
            sizex=0.02, sizey=0.02,
        )
    )


    fig.add_layout_image(
        dict(
            source=UKRAINE_IMAGE,
            x=0.1, y=0.95,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=ENGLAND_IMAGE,
            x=0.015, y=0.83,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=GERMANY_IMAGE,
            x=0.1, y=0.83,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=WALES_IMAGE,
            x=0.015, y=0.71,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=DENMARK_IMAGE,
            x=0.1, y=0.71,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=NETHERLANDS_IMAGE,
            x=0.015, y=0.58,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=CZE_REPUBLIC_IMAGE,
            x=0.1, y=0.58,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=ITALY_IMAGE,
            x=0.015, y=0.46,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=AUSTRIA_IMAGE,
            x=0.1, y=0.46,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=BELGIUM_IMAGE,
            x=0.015, y=0.33,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=PORTUGAL_IMAGE,
            x=0.1, y=0.33,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=SPAIN_IMAGE,
            x=0.1, y=0.21,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=CROATIA_IMAGE,
            x=0.015, y=0.21,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=FRANCE_IMAGE,
            x=0.015, y=0.08,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=SWITZERLAND_IMAGE,
            x=0.1, y=0.08,
            sizex=0.02, sizey=0.02,
        )
    )



    # Quarter-Finals
    fig.add_layout_image(
        dict(
            source=UKRAINE_IMAGE,
            x=0.3, y=0.83,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=ENGLAND_IMAGE,
            x=0.39, y=0.83,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=CZE_REPUBLIC_IMAGE,
            x=0.3, y=0.58,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=DENMARK_IMAGE,
            x=0.39, y=0.58,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=BELGIUM_IMAGE,
            x=0.31, y=0.33,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=ITALY_IMAGE,
            x=0.39, y=0.33,
            sizex=0.02, sizey=0.02,
        )
    )
    fig.add_layout_image(
        dict(
            source=SWITZERLAND_IMAGE,
            x=0.31, y=0.08,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=SPAIN_IMAGE,
            x=0.39, y=0.08,
            sizex=0.02, sizey=0.02,
        )
    )

    # Semi-Finals


    fig.add_layout_image(
        dict(
            source=DENMARK_IMAGE,
            x=0.68, y=0.71,
            sizex=0.02, sizey=0.02,
        ),
    )

    fig.add_layout_image(
        dict(
            source=ENGLAND_IMAGE,
            x=0.59, y=0.71,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=ITALY_IMAGE,
            x=0.59, y=0.21,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=SPAIN_IMAGE,
            x=0.68, y=0.21,
            sizex=0.02, sizey=0.7,
        )
    )

    # Final

    fig.add_layout_image(
        dict(
            source=ITALY_IMAGE,
            x=0.88, y=0.46,
            sizex=0.02, sizey=0.02,
        )
    )

    fig.add_layout_image(
        dict(
            source=ENGLAND_IMAGE,
            x=0.97, y=0.46,
            sizex=0.02, sizey=0.02,
        )
    )



    return fig

