import plotly.graph_objects as go
import plotly.io as pio

# Define the matches and results
matches = [
    {"round": "Round of 16", "team1": "CRO", "score1": 3, "team2": "ESP", "score2": 5},
    {"round": "Round of 16", "team1": "FRA", "score1": 3, "team2": "SUI", "score2": 3, "penalties": "(4) - (5)"},
    {"round": "Round of 16", "team1": "ITA", "score1": 2, "team2": "AUT", "score2": 1},
    {"round": "Round of 16", "team1": "BEL", "score1": 1, "team2": "POR", "score2": 0},
    {"round": "Round of 16", "team1": "WAL", "score1": 0, "team2": "DEN", "score2": 4},
    {"round": "Round of 16", "team1": "NED", "score1": 0, "team2": "CZE", "score2": 2},
    {"round": "Round of 16", "team1": "ENG", "score1": 2, "team2": "GER", "score2": 0},
    {"round": "Round of 16", "team1": "SWE", "score1": 1, "team2": "UKR", "score2": 2},

    {"round": "Quarter-finals", "team1": "SUI", "score1": 1, "team2": "ESP", "score2": 1, "penalties": "(1) - (3)"},
    {"round": "Quarter-finals", "team1": "BEL", "score1": 1, "team2": "ITA", "score2": 2},
    {"round": "Quarter-finals", "team1": "CZE", "score1": 1, "team2": "DEN", "score2": 2},
    {"round": "Quarter-finals", "team1": "UKR", "score1": 0, "team2": "ENG", "score2": 4},

    {"round": "Semi-finals", "team1": "ITA", "score1": 1, "team2": "ESP", "score2": 1, "penalties": "(4) - (2)"},
    {"round": "Semi-finals", "team1": "ENG", "score1": 2, "team2": "DEN", "score2": 1},

    {"round": "Final", "team1": "ITA", "score1": 1, "team2": "ENG", "score2": 1, "penalties": "(3) - (2)"}
]

# Create the plot
fig = go.Figure()

# Path to the directory containing flag images
flag_dir = "/path/to/flag_images/"
background_image = './euro_background.png'

# Define the coordinates for the matches
coordinates = {
    "Round of 16": 1,
    "Quarter-finals": 2,
    "Semi-finals": 3,
    "Final": 4
}

# Assign y coordinates to each match manually
y_coords = {
    "Round of 16": [1, 2, 3, 4, 5, 6, 7, 8],
    "Quarter-finals": [1, 3, 5, 7],
    "Semi-finals": [2, 6],
    "Final": [4]
}

# Add matches to the plot
for match in matches:
    x = coordinates[match["round"]]
    y = y_coords[match["round"]].pop(0)

    fig.add_trace(go.Scatter(
        x=[x],
        y=[y],
        text=f"{match['team1']} {match['score1']} - {match['score2']} {match['team2']}",
        mode='markers+text',
        textposition='top center',
        marker=dict(size=15, opacity=0)
    ))

    fig.add_layout_image(
        dict(
         #   source=f"{flag_dir}{match['team1']}.png",
            xref="x",
            yref="y",
            x=x - 0.1,
            y=y,
            sizex=0.1,
            sizey=0.1,
            xanchor="center",
            yanchor="middle"
        )
    )

    fig.add_layout_image(
        dict(
          #  source=f"{flag_dir}{match['team2']}.png",
            xref="x",
            yref="y",
            x=x + 0.1,
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
    yaxis_title="Matchs",
    xaxis=dict(
        tickmode='array',
        tickvals=list(coordinates.values()),
        ticktext=list(coordinates.keys())
    ),
    yaxis=dict(
        tickmode='linear',
        tick0=1,
        dtick=1,
        range=[0.5, 8.5] 
    ),
        images=[dict(
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
    )],
    showlegend=False
)
fig.update_layout(template="plotly_white")


fig.show()
pio.show(background_image)
