import dash
from dash import html, dcc, Input, Output
from flask import Flask, render_template
import json
import plotly.graph_objs as go
import os


server = Flask(__name__)  # Create a Flask instance
app = Flask(__name__)

import violon_team
import bar_chart_off_def
import bar_dist_discip
import radar_chart_goal_goalKeeping_team
import radar_chart_off_def_team
import radar_chart_dist_discip_team
import brackets
from line_up_chart import create_lineup_chart  # Import the create_lineup_chart function




app = dash.Dash(__name__)
app.title = 'Project_Viz'
server = app.server

def load_figure_from_json(file_path):
    with open(file_path, 'r') as f:
        fig_dict = json.load(f)
    return go.Figure(fig_dict)



def get_team_figures_off_def(team_name):
    fig_offense, fig_defense = bar_chart_off_def.get_fig(team_name)
    return fig_offense, fig_defense



def get_team_figures_dist_discip(team_name):
    fig_dist, fig_discip = bar_dist_discip.get_fig(team_name)
    return fig_dist, fig_discip



fig_goals, fig_goals_keep=radar_chart_goal_goalKeeping_team.get_fig()
fig_offense_team, fig_defense_team=radar_chart_off_def_team.get_fig()
fig_dist_team, fig_discip_team=radar_chart_dist_discip_team.get_fig()

def add_graph(id, figure):
    '''
        Adds a dcc.Graph with the corresponding id and based on the figure.

        Args:
            id: id of the dcc.Graph
            figure: figure of the dcc.Graph
        Returns:
            A html.Div(dcc.Graph) with figure and the id.
    '''
    graph = html.Div(dcc.Graph(
                id=id,
                className='graph',
                figure=figure,
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False, 
                    displayModeBar=False
                )
            ), style={'borderRadius': '8px', 'overflow': 'hidden'})
    return graph


image2 = "https://wallpapercave.com/wp/wp9488231.jpg" 

home_layout = html.Div(
    style={
        'font-family': 'Roboto, sans-serif',
        'color': '#333333',
        'backgroundColor': '#F5F5F5'  
    },
    children=[
        # Header Section
        html.Div(
            style={
                'backgroundColor': '#2C3E50',
                'padding': '10px 20px',
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center',
                'borderRadius': '12px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'position': 'relative'  # Necessary for the hover effect
            },
            children=[
                html.H1(
                    "Euro 2020: A Happy Outcome in Pandemics",
                    style={
                        'font-size': '2em',
                        'color': '#ECF0F1',
                        'margin': '0',
                        'font-weight': 'bold',
                        'font-family': 'Montserrat, sans-serif'
                    }
                ),
                html.Nav(
                    style={'display': 'flex', 'gap': '25px'},
                    children=[
                        html.A("Home", href="/", style={
                            'color': '#ECF0F1',
                            'textDecoration': 'none',
                            'fontSize': '1.2em',
                            'fontWeight': 'bold',
                            'position': 'relative',
                            'padding': '5px 10px',
                            'borderRadius': '5px',
                            'transition': 'background-color 0.3s ease'
                        }),
                        html.A("Statistics", href="/statistics", style={
                            'color': '#ECF0F1',
                            'textDecoration': 'none',
                            'fontSize': '1.2em',
                            'fontWeight': 'bold',
                            'position': 'relative',
                            'padding': '5px 10px',
                            'borderRadius': '5px',
                            'transition': 'background-color 0.3s ease'
                        }),
                    ]
                )
            ]
        ),
        # Image as Wallpaper
        html.Div(
            style={
                'position': 'relative',
                'width': '100%',
                'height': '500px',
                'backgroundImage': f'url({image2})',
                'backgroundSize': 'cover',
                'backgroundPosition': 'center',
                'borderRadius': '12px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'marginTop': '20px'
            },
            children=[
                html.Div(
                    style={
                        'position': 'absolute',
                        'bottom': '20px',
                        'left': '20px',
                        'backgroundColor': 'rgba(44, 62, 80, 0.8)',  # Semi-transparent dark grey
                        'color': '#ECF0F1',
                        'padding': '20px',
                        'borderRadius': '12px',
                        'maxWidth': '70%',
                        'font-family': 'Lora, serif'
                    },
                    children=[
                        html.P(
                            "Italy against UK in the finals: Won only at Penalty round! "
                            "Was it only luck or a building-up work? Why teams such as Belgium and Spain saw their hopes broken? "
                            "To reply to these legitimate questions, we aim at investigating different impacting factors such as "
                            "performance at the team level, at the player level, accuracy and determination, flops and corrections "
                            "which made the differences between the teams and led to Italy's victory! MATCHES ARE NOT PLAYED, THEY ARE WON!",
                            style={
                                'font-size': '1.2em',
                                'lineHeight': '1.8',
                                'textShadow': '1px 1px 2px rgba(0, 0, 0, 0.8)'
                            }
                        )
                    ]
                )
            ]
        ),
        # Lineup Chart Section
        html.Div(
            style={
                'padding': '20px',
                'backgroundColor': '#ECF0F1',  
                'borderRadius': '12px',
                'marginTop': '20px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
            },
            children=[
                html.Div(
                    style={
                        'backgroundColor': '#2980B9', 
                        'font-size': '1.5em',
                        'borderRadius': '8px',
                        'padding': '15px',
                        'color': 'white',
                        'marginBottom': '20px',
                        'textAlign': 'center',
                        'fontWeight': 'bold',
                        'font-family': 'Montserrat, sans-serif'
                    },
                    children=[
                        html.H2('Lineup Chart', style={'margin': '0'})
                    ]
                ),
                html.Div(
                    style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '20px'},
                    children=[
                        dcc.Dropdown(
                            id='lineup-team-selector',
                            options=[
                                {'label': team, 'value': team} for team in ['Italy', 'England', 'Spain', 'Belgium', 'Austria', 'Switzerland']
                            ],
                            value='Italy',
                            style={'flex': '1', 'marginRight': '10px', 'color': '#333333'}
                        ),
                        dcc.Checklist(
                            id='role-selector',
                            options=[
                                {'label': 'Goalkeepers', 'value': 'goalkeepers'},
                                {'label': 'Defenders', 'value': 'defenders'},
                                {'label': 'Midfields', 'value': 'midfielders'},
                                {'label': 'Forwards', 'value': 'forwards'}
                            ],
                            value=['goalkeepers', 'defenders', 'midfielders', 'forwards'],
                            inline=True,
                            style={'flex': '2', 'display': 'flex', 'justifyContent': 'space-between', 'color': '#333333'}
                        )
                    ]
                ),
                html.Div(id='lineup-graph', style={'marginTop': '20px'})
            ]
        ),

        html.Div(
        style={
            'padding': '20px',
            'backgroundColor': '#ECF0F1', 
            'borderRadius': '12px',
            'marginTop': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        },
        children=[
            html.Div(
                style={
                    'backgroundColor': '#2980B9',  
                    'font-size': '1.5em',
                    'borderRadius': '8px',
                    'padding': '15px',
                    'color': 'white',
                    'marginBottom': '10px',
                    'textAlign': 'center',
                    'fontWeight': 'bold',
                    'font-family': 'Montserrat, sans-serif'
                },
                children=[
                    html.H2('Tournament Bracket', style={'margin': '0'})
                ]
            ),
            dcc.Graph(
                id='bracket-graph',
                figure= brackets.generate_bracket(),  # Call the function to generate the bracket figure
                style={'marginTop': '0', 'height': '1000px' }
            )
        ]
    )
]
)


statistics_layout = html.Div(
    style={
        'font-family': 'Roboto, sans-serif',
        'color': '#333333',
        'backgroundColor': '#F5F5F5'  
    },
    children=[
        html.Div(
            style={
                'backgroundColor': '#2C3E50', 
                'padding': '10px 20px',
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center',
                'borderRadius': '12px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'position': 'relative'  
            },
            children=[
                html.H1(
                    "Euro 2020: A Happy Outcome in Pandemics",
                    style={
                        'font-size': '2em',
                        'color': '#ECF0F1',
                        'margin': '0',
                        'font-weight': 'bold',
                        'font-family': 'Montserrat, sans-serif'
                    }
                ),
                html.Nav(
                    style={'display': 'flex', 'gap': '15px'},
                    children=[
                        html.A("Home", href="/", style={
                            'color': '#ECF0F1',
                            'textDecoration': 'none',
                            'fontSize': '1.2em',
                            'fontWeight': 'bold',
                            'position': 'relative',
                            'padding': '5px 10px',
                            'borderRadius': '5px',
                            'transition': 'background-color 0.3s ease'}),
                        html.A("Statistics", href="/statistics", style={
                            'color': '#ECF0F1',
                            'textDecoration': 'none',
                            'fontSize': '1.2em',
                            'fontWeight': 'bold',
                            'position': 'relative',
                            'padding': '5px 10px',
                            'borderRadius': '5px',
                            'transition': 'background-color 0.3s ease'}),
                    ]
                )
            ]
        ),

        html.Div(
            style={
                'padding': '0 30px', 
                'backgroundColor': '#F5F5F5', 
                'color': '#333333', 
                'borderRadius': '8px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
                'marginBottom': '20px'
            },
            children=[
                html.Div(
                    style={
                        'backgroundColor': '#34495E',
                        'fontSize': '1.5em',
                        'borderRadius': '8px 8px 0 0',
                        'padding': '10px 20px',
                        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
                        'color': '#ECF0F1',
                        'marginTop': '20px'  

                    },
                    children=[
                        html.H2('Player Evaluation', style={'margin': '0', 'fontWeight': 'bold'})
                    ]
                ),
                html.Div(
                    style={
                        'padding': '20px',
                        'backgroundColor': '#ECF0F1',
                        'borderRadius': '0 0 8px 8px',
                        'marginBottom': '20px',
                    },
                    children=[
                        html.H2('Defense and Offense', style={'marginTop': '0'}),
                        html.P(
                            "Now we will go in-depth with all the metrics associated with players in the 6 teams of interest to us: "
                            "Italy, England, Belgium, Spain, Austria and Switzerland. "
                            "Italy: Tournament winner, England: Final's representative, Spain: semi-finals representative, Belgium: "
                            "quarter-finals representative, Austria: eighth finals representative, and Switzerland: round of 16 representative. "
                            "We're using stacked bar charts to get a clear view of how players perform in 6 different areas. "
                            "1) Defense Metrics: Recovered balls, Tackles, Clearances, Blocks. 2) Offense Metrics: Assists, Corners, Offsides. "
                            "3) Defense Metrics: Passes attempted, Passes Completed, Crosses Attempted, Crosses Completed, Free-Kicks on Goal "
                            "5) Goals Metrics: Goals scored, Goals scored in open play, Goals scored on penalty, Goals scored on corner, "
                            "Goals scored on penalty phase, and Goals on set pieces 6) Goal Keeping Metrics: Saves, Goals conceded, Own goals, "
                            "Saves from penalty, Punches. For each team, each player's performance is compared in terms of all metrics. "
                            "An option to select/deselect a metric is enabled by clicking on the legend. The hovering utility gives the "
                            "percentage of the metric. Hence, we can easily identify where weaknesses and strengths lie.",
                            style={'lineHeight': '1.6', 'textAlign': 'justify'}
                        ),
         
                    ]
                ),
                html.Div(
                    style={
                        'padding': '20px',
                        'backgroundColor': '#ECF0F1',
                        'borderRadius': '8px',
                        'marginBottom': '20px'
                    },
                    children=[
                        dcc.Dropdown(
                            id='team-selector',
                            options=[
                                {'label': team, 'value': team} for team in ['Italy', 'England', 'Spain', 'Belgium', 'Austria', 'Switzerland']
                            ],
                            value='Italy',  # Default value
                            style={'color': 'black'}  
                        ),
                        html.Div(id='team-graphs', style={'marginTop': '20px'})  # Div to insert the graphs
                    ]
                ),
        html.Div(
            style={
                'padding': '20px',
                'backgroundColor': '#ECF0F1',
                'borderRadius': '8px',
                'marginBottom': '20px'
            },
            children=[
                html.H2('Disciplinary & Distribution', style={'marginTop': '0'}),
                dcc.Dropdown(
                    id='team-selector-2',
                    options=[
                        {'label': team, 'value': team} for team in ['Italy', 'England', 'Spain', 'Belgium', 'Austria', 'Switzerland']
                    ],
                    value='Italy',  # Default value
                    style={'color': 'black'}  
                ),
                html.Div(id='team-graphs-2', style={'marginTop': '20px'}) 
            ]
        ),
                html.Div(
                    style={
                'marginBottom': '60px',
                'backgroundColor': '#333333',  
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                    },
                    children=[
                        html.H2('Team Evaluation', style={'color': 'white', 'marginBottom': '20px'}),
                        html.Div(
                            style={
                'marginBottom': '60px',
                'backgroundColor': '#333333',  
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                            },
                            children=[
                                html.H2('Dissecting The Teams\' Performance' , style={'color': 'white', 'marginBottom': '20px'}),
                                html.P(
                                    "Let us visit again the previous performance aspects for the teams! For that, we will rely on a radar chart, "
                                    "which is quite good for performing cross-comparison. Again, we dive into the defense, offense, distribution, "
                                    "disciplinary, goals, and goals keeping profiles of the teams, through exploiting pertinent statistics pertaining to those. "
                                    "All the displayed values correspond to the total per team. We do not want winners devoid of sportsmanship; this is why "
                                    "we are scrutinizing the disciplinary aspects of the competitors!",
                                    style={'color': 'white', 'fontSize': '1.1em', 'lineHeight': '1.6', 'marginBottom': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
                                ),
                                html.H2('Offensive Team Analysis',  style={'color': 'white', 'marginBottom': '20px'}),
                                html.Div(
                                    style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'},

                                    children=[
                                        html.Div(
                                            style={'width': '60%', 'padding': '10px'}, 
                                            children=[
                                                add_graph(id='radar-chart_offense', figure=fig_offense_team)
                                            ]
                                        ),
                                        html.Div(
                                            style={'width': '35%', 'padding': '20px', 'backgroundColor': '#444', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'color': 'white'}, 
                                            children=[
                                                html.Table(
                                                    style={'width': '100%', 'borderCollapse': 'collapse'},
                                                    children=[
                                                        html.Thead(
                                                            children=html.Tr(
                                                                children=[
                                                                    html.Th('Name', style={'padding': '10px', 'borderBottom': '2px solid #888'}),
                                                                    html.Th('Description', style={'padding': '10px', 'borderBottom': '2px solid #888'})
                                                                ]
                                                            )
                                                        ),
                                                        html.Tbody(
                                                            children=[
                                                                html.Tr(children=[html.Td('Recovered balls', style={'padding': '10px', 'borderBottom': '1px solid #888'}), html.Td('When a player regains possession of the ball from the opposing team.', style={'padding': '10px', 'borderBottom': '1px solid #888'})]),
                                                                html.Tr(children=[html.Td('Tackles', style={'padding': '10px', 'borderBottom': '1px solid #888'}), html.Td('When a player uses their feet to challenge an opponent for the ball.', style={'padding': '10px', 'borderBottom': '1px solid #888'})]),
                                                                html.Tr(children=[html.Td('Clearances', style={'padding': '10px', 'borderBottom': '1px solid #888'}), html.Td('When a player kicks the ball away from their goal area to prevent the opposing team from scoring.', style={'padding': '10px', 'borderBottom': '1px solid #888'})]),
                                                                html.Tr(children=[html.Td('Blocks', style={'padding': '10px', 'borderBottom': '1px solid #888'}), html.Td('When a player stops the ball from advancing, typically a shot or pass, by using their body.', style={'padding': '10px', 'borderBottom': '1px solid #888'})])
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
                html.Div(
            style={
                'marginBottom': '60px',
                'backgroundColor': '#333333',  
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'  
            },
            children=[
                html.H2('Defensive Team Analysis', style={'color': 'white', 'marginBottom': '20px'}),
                html.Div(
                    style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'},
                    children=[
                        html.Div(style={'width': '60%', 'padding': '10px'}, children=[
                            add_graph(id='radar-chart_defense', figure=fig_defense_team)
                        ]),
                        html.Div(
                            style={'width': '35%', 'padding': '20px', 'backgroundColor': '#444', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'color': 'white'}, 
                            children=[
                            html.Table(
                                style={'width': '100%', 'borderCollapse': 'collapse'},
                                children=[
                                    html.Thead(
                                        children=html.Tr(children=[
                                            html.Th('Name', style={'padding': '10px', 'borderBottom': '2px solid #888'}),
                                            html.Th('Description', style={'padding': '10px', 'borderBottom': '2px solid #888'})
                                        ])
                                    ),
                                    html.Tbody(
                                        children=[
                                            html.Tr(children=[
                                                html.Td('Assist', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Final pass or touch leading directly to a goal.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Corner', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Kick awarded to an attacking team when the ball goes over the goal line after last being touched by a defending player.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Offside', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Violation occurring when an attacking player is positioned nearer to the opponent goal line when the ball is passed to him.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ])
                                        ]
                                    )
                                ]
                            )
                        ])
                    ]
                )
            ]
        ),

        # -------DISTRIBUTION----------
        html.Div(
            style={
                'marginBottom': '60px',
                'backgroundColor': '#333333',  
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'  
            },
            children=[
                html.H2('Distribution Team Analysis', style={'color': 'white', 'marginBottom': '20px'}),
                html.Div(
                    style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'},
                    children=[
                        html.Div(style={'width': '60%', 'padding': '10px'}, children=[
                            add_graph(id='radar-chart_distribution', figure=fig_dist_team)
                        ]),
                        html.Div(
                            style={'width': '35%', 'padding': '20px', 'backgroundColor': '#444', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'color': 'white'}, 
                            children=[
                            html.Table(
                                style={'width': '100%', 'borderCollapse': 'collapse'},
                                children=[
                                    html.Thead(
                                        children=html.Tr(children=[
                                            html.Th('Name', style={'borderBottom': '2px solid #888', 'padding': '10px', 'textAlign': 'left'}),
                                            html.Th('Description', style={'borderBottom': '2px solid #888', 'padding': '10px', 'textAlign': 'left'})
                                        ])
                                    ),
                                    html.Tbody(
                                        children=[
                                            html.Tr(children=[
                                                html.Td('Passes attempted', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Total number of attempts a player made kicking, heading, or moving the ball to a teammate.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Passes completed', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Number of passes that successfully reach a teammate.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Crosses attempted', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Number of times a player attempts to send the ball from the wide areas to the penalty area of the opponent.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Crosses completed', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Number of successful crosses that reach a teammate.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Free kicks on goal', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Restarting play after a foul or other infringement has occurred with the intention of scoring a goal.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ])
                                        ]
                                    )
                                ]
                            )
                        ])
                    ]
                )
            ]
        ),

        # -------DISCIPLINARY----------
        html.Div(
            style={
                'marginBottom': '60px',
                'backgroundColor': '#333333',  
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'  
            },
            children=[
                html.H2('Disciplinary Team Analysis', style={'color': 'white', 'marginBottom': '20px'}),
                html.Div(
                    style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'},
                    children=[
                        html.Div(style={'width': '60%', 'padding': '10px'}, children=[
                            add_graph(id='radar-chart_discipline', figure=fig_discip_team)
                        ]),
                        html.Div(
                            style={'width': '35%', 'padding': '20px', 'backgroundColor': '#444', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'color': 'white'}, 
                            children=[
                            html.Table(
                                style={'width': '100%', 'borderCollapse': 'collapse'},
                                children=[
                                    html.Thead(
                                        children=html.Tr(children=[
                                            html.Th('Name', style={'borderBottom': '2px solid #888', 'padding': '10px', 'textAlign': 'left'}),
                                            html.Th('Description', style={'borderBottom': '2px solid #888', 'padding': '10px', 'textAlign': 'left'})
                                        ])
                                    ),
                                    html.Tbody(
                                        children=[
                                            html.Tr(children=[
                                                html.Td('Fouls committed', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Number of times a player breaks the rules resulting in a free kick or penalty for the opposing team.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Yellow cards', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Cautions given to a player by the referee for serious fouls or misconduct.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Fouls suffered', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Number of times a player is fouled by an opponent.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Red cards', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Send-off given to players for serious fouls or misconduct, resulting in their removal from the game.', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ])
                                        ]
                                    )
                                ]
                            )
                        ])
                    ]
                )
            ]
        ),
                # -------Goals----------
        html.Div(
            style={  
                'marginBottom': '60px',
                'backgroundColor': '#333333',  
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'  
                }, 
            children=[
                html.H2('Goals Team Performance', style={'color': 'white', 'fontSize': '2em', 'marginBottom': '20px'}),
                html.Div(
                    style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}, 
                    children=[
                        html.Div(
                            style={'width': '60%', 'padding': '20px', 'backgroundColor': '#f4f4f4', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}, 
                            children=[
                                add_graph(id='radar-chart_goals', figure=fig_goals)
                            ]
                        ),
                        html.Div(
                            style={'width': '35%', 'padding': '20px', 'backgroundColor': '#444', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'color': 'white'}, 
                            children=[
                                html.Table(
                                    style={'width': '100%', 'borderCollapse': 'collapse'}, 
                                    children=[
                                        html.Thead(children=html.Tr(children=[
                                            html.Th('Name', style={'borderBottom': '2px solid #888', 'padding': '10px', 'textAlign': 'left'}),
                                            html.Th('Description', style={'borderBottom': '2px solid #888', 'padding': '10px', 'textAlign': 'left'})
                                        ])),
                                        html.Tbody(children=[
                                            html.Tr(children=[
                                                html.Td('Goals scored', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Total number of goals a player or team scores', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Goals scored in open play', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Goals scored during the normal course of the game, not from set-pieces or penalties', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Goals scored on penalty', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Goals scored directly from a penalty kick or resulting from the play immediately following a penalty', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Goals scored on corner', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Goals scored directly from a corner kick or resulting from the play immediately following a corner', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Goals scored on penalty phase', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Goals scored during the penalty phase, including shootouts or the immediate play following a penalty', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Goals on set pieces', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Goals scored from set-pieces such as free kicks, corners, or throw-ins', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ])
                                        ])
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),

        # -------Goals Keeping----------
        html.Div(
            style={
                'marginBottom': '60px',
                'backgroundColor': '#333333',  
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'  
                }, 
            children=[
                html.H2('Goalkeeping Team Performance', style={'color': 'white', 'fontSize': '2em', 'marginBottom': '20px'}),
                html.Div(
                    style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}, 
                    children=[
                        html.Div(
                            style={'width': '60%', 'padding': '20px', 'backgroundColor': '#f4f4f4', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}, 
                            children=[
                                add_graph(id='radar-chart_goals_keep', figure=fig_goals_keep)
                            ]
                        ),
                        html.Div(
                            style={'width': '35%', 'padding': '20px', 'backgroundColor': '#444', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'color': 'white'}, 
                            children=[
                                html.Table(
                                    style={'width': '100%', 'borderCollapse': 'collapse'}, 
                                    children=[
                                        html.Thead(children=html.Tr(children=[
                                            html.Th('Name', style={'borderBottom': '2px solid #888', 'padding': '10px', 'textAlign': 'left'}),
                                            html.Th('Description', style={'borderBottom': '2px solid #888', 'padding': '10px', 'textAlign': 'left'})
                                        ])),
                                        html.Tbody(children=[
                                            html.Tr(children=[
                                                html.Td('Saves', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('When a goalkeeper successfully stops the ball from entering the goal', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Goals conceded', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Number of goals a team allows the opposing team to score', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Own goals', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('Goals scored accidentally by a player into the goal of his own team', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Saves from penalty', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('When a goalkeeper prevents a goal from being scored during a penalty kick', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ]),
                                            html.Tr(children=[
                                                html.Td('Punches', style={'padding': '10px', 'borderBottom': '1px solid #888'}),
                                                html.Td('When a goalkeeper uses his fists to clear the ball away from the goal area', style={'padding': '10px', 'borderBottom': '1px solid #888'})
                                            ])
                                        ])
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(style={
                'marginBottom': '60px',
                'backgroundColor': '#333333',  
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}, children=[
    html.H2('Additional Analysis', style={'color': 'white', 'fontSize': '2em', 'marginBottom': '20px'}),
    html.P("We're turning to the trusty violin plot to shed some light on hidden yet key factors which made the difference between the two teams having competed for the title at the finals: the distribution of the playing time on the pitch per player, and the distribution of the attempts across the matches per player within the squads. Compared to England, it is observed that Italian players exhibit a more uniform playing time, showing that all had spent a close time on the field. Furthermore, the number of attempts is close among the Italian players, since most have performed either 1 or 2. Apparently the Italian team was coherent and well-synchronized, and this made the difference!",
           style={'color': 'white', 'fontSize': '1.1em', 'lineHeight': '1.6', 'marginBottom': '20px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'flexWrap': 'wrap'}, children=[
        html.Div(style={'width': '90%', 'padding': '20px', 'backgroundColor': '#f4f4f4', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'marginBottom': '20px'}, children=[
            add_graph(id='violin-attempts', figure=violon_team.draw_figure(df=violon_team.prep_data_violin(), column="Total Attempts"))
        ]),
        html.Div(style={'width': '90%', 'padding': '20px', 'backgroundColor': '#f4f4f4', 'borderRadius': '8px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'marginBottom': '20px'}, children=[
            add_graph(id='violin-played_time', figure=violon_team.draw_figure(df=violon_team.prep_data_violin(), column="Played Time"))
        ])
    ])
]),

  ])


app.layout = html.Div(
    children=[
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ]
)

# Update the layout based on the URL
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/statistics':
        return statistics_layout
    else:
        return home_layout


        

@app.callback(
    Output('team-graphs', 'children'),
    [Input('team-selector', 'value')]
)

def update_graphs(selected_team):
    fig_offense, fig_defense = get_team_figures_off_def(selected_team)
    return [
        add_graph(id='barchart-offense', figure=fig_offense),
        add_graph(id='barchart-defense', figure=fig_defense),
    ]

@app.callback(
    Output('team-graphs-2', 'children'),
    [Input('team-selector-2', 'value')]
)
def update_graphs_2(selected_team):

    file_path_dist_r = f'Euro_2020_Data_Visualization/assets/{selected_team}_distribution.json'
    file_path_discip_r = f'Euro_2020_Data_Visualization/assets/{selected_team}_disciplinary.json'
    file_path_dist= os.path.abspath(file_path_dist_r)
    file_path_discip = os.path.abspath(file_path_discip_r)
    
    fig_dist = load_figure_from_json(f'{file_path_dist}')
    fig_discip = load_figure_from_json(f'{file_path_discip}')



    return [
        dcc.Graph(id='barchart-dist', figure=fig_dist),
        dcc.Graph(id='barchart-discip', figure=fig_discip)
    ]

# Callback for Lineup Chart
@app.callback(
    Output('lineup-graph', 'children'),
    [Input('lineup-team-selector', 'value'), Input('role-selector', 'value')]
)
def update_lineup_chart(selected_team, selected_roles):
    fig_lineup = create_lineup_chart(selected_team, selected_roles)
    return add_graph(id='lineup-chart', figure=fig_lineup)

@server.route('/index')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run_server(debug=True)
