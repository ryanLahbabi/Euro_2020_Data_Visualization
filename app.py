import dash
from dash import html, dcc, Input, Output
from flask import Flask, render_template

server = Flask(__name__)  # Create a Flask instance
app = Flask(__name__)

import violon_team
import bar_chart_off_def
import bar_dist_discip

import radar_chart_goal_goalKeeping_team
import radar_chart_off_def_team
import radar_chart_dist_discip_team
from line_up_chart import create_lineup_chart  # Import the create_lineup_chart function




app = dash.Dash(__name__)
app.title = 'Project_Viz'
server = app.server



def get_team_figures(team_name):
    # Cette fonction appelle une fonction générique qui renvoie les figures pour l'équipe spécifiée.
    # Vous devez adapter vos fonctions `get_fig` pour qu'elles acceptent un nom d'équipe.
    fig_offense, fig_defense = bar_chart_off_def.get_fig(team_name)
    #fig_dist, fig_discip = bar_dist_discip.get_fig(team_name)
    return fig_offense, fig_defense#, fig_dist, fig_discip




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

app.layout = html.Div(
    style={
    'font-family': 'Arial',
    'color': '#00008B',  # Dark blue text color
    'backgroundColor': 'rgb(173, 216, 230)'  # Light blue background color
},
    className='content',
    children=[
    html.Header(style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center','backgroundColor': '#4F7942','margin':'0px','borderRadius': '5px'}, children=[
        html.H1("Euro 2020: A Happy Outcome in Pandemics", 
                style={'font-size': '3em', 'marginBottom': '5px', 'font-weight': 'bold', 'color': 'white'}),
        html.Img(src=image2, style={'height': '500px', 'marginLeft': '20px', 'borderRadius': '8px'}),
        html.P("Italy against UK in the finals: Won only at Penalty round!. \
               Was it only luck or a building-up work? Why teams such as Belgium and Spain saw their hopes broken?. \
               To  reply to these legitimate questions, we aim at investigating different impacting factors such as performance at the team level, at the player level, accuracy and determination, flops and correctins which made the differences between the teams and lead to Italy' victory! . \
               \
               MATCHES ARE NOT PLAYED, THEY ARE WON!.", 
               style={'font-size': '1.3em', 'marginBottom': '20px', 'marginLeft': '30px', 'text-align': 'center', 'color': 'white'})
    ]),

    html.Div(style={'padding': '0 30px', 'backgroundColor': 'rgb(59, 59, 59)'}, children=[
            html.Div(style={'backgroundColor': '#4F7942','font-size': '1.5em','borderRadius': '5px'}, children=[
                html.H2('Lineup Chart'),
            ]),
            html.Div([
                dcc.Dropdown(
                    id='lineup-team-selector',
                    options=[
                        {'label': team, 'value': team} for team in ['Italy', 'England', 'Spain', 'Belgium', 'Austria', 'Switzerland']
                    ],
                    value='Italy'  # Default value
                ),
                html.Div(id='lineup-graph'), # Div to insert the lineup chart
            ]),
        ]),

    #------- OFFENSE DEFENSE 
    

    html.Div(style={'padding': '0 30px', 'backgroundColor': 'rgb(59, 59, 59)'}, children=[


        html.Div(style={'backgroundColor': '#4F7942','font-size': '1.5em','borderRadius': '5px'}, children=[
            html.H2('Player Evaluation'),
        ]),
        
        html.Div(style={'marginBottom': '60px'}, children=[

            html.H2('Defense and Offense'),
            html.P("Now we will go inot depth with all the metrics associated with players in the 6 teams of interest to us: Italy, England, Belgium, Spain, Austria and Switzerland.\
                    Italy: Tournament winner, England: Final's representative, Spain: semi-finals representative, Belgium: quarter-finals representative, Austria: eighth finals representative, and Switzerland: round of 16 representative.   \
                   We're using stacked bar charts to get a clear view of how players perform in 6 different areas. \
                   1) Defense Metrics: Recovered balls, Tackles, Clearances, Blocks. 2) Offense Metrics: Assists, Corners, Offsides. \
                   3) Defense Metrics: Passes attempted, Passes Completed, Crosses Attempted, Crosses Completed, Free-Kicks on Goal \
                   5) Goals Metrics: Goals scored, Goals scored in open play, Goals scored on penalty, Goals scored on corner, Goals scored on penalty phase, and Goals on set pieces\
                   6) Goal Keeping Metrics: Saves, Goals conceded, Own goals, Saves from penalty, Punches\
                    For each team,  each player's performance is compared in terms of all metrics. An option to select/deselect a metric is enabled by clicking on the legend.\
                    The hovering utility gives the percentage of the metric. Hence, we can easily identify where weaknesses and strengths lie.")
        ]),
        html.Div([
            dcc.Dropdown(
                id='team-selector',
                options=[
                    {'label': team, 'value': team} for team in ['Italy', 'England', 'Spain', 'Belgium', 'Austria', 'Switzerland']
                ],
                value='Italy'  # Valeur par défaut
            ),
            html.Div(id='team-graphs'), # Div pour insérer les graphiques
        ]),


        
        #--------------DISTRIBUTION 


        html.Div(style={'marginBottom': '60px'}, children=[
            html.H2('Distribution'),

            '''
            add_graph(id='barchart-distrib_italy', figure=fig_dist_Italy),
            add_graph(id='barchart-distrib_england', figure=fig_dist_England),
            add_graph(id='barchart-distrib_spain', figure=fig_dist_Spain),
             add_graph(id='barchart-distrib_belgium', figure=fig_dist_Belgium),
            add_graph(id='barchart-distrib_austria', figure=fig_dist_Austria),
'''
            
            
        ]),

        #--------------- DISCIPLINARY ------------
'''
        html.Div(style={'marginBottom': '60px'}, children=[
            html.H2('Disciplinary'),
            add_graph(id='barchart-discip_italy', figure=fig_discip_Italy),
            add_graph(id='barchart-discip_england', figure=fig_discip_England),
            add_graph(id='barchart-discip_spain', figure=fig_discip_Spain),
            add_graph(id='barchart-discip_belgium', figure=fig_discip_Belgium),
            add_graph(id='barchart-discip_austria', figure=fig_discip_Austria),

        ]),
''',
        

    #--------------------------------------------------------------------TEAM EVALUATION : RADAR CHART--------------------------------------------------------------------------------------------

        #-------OffENSE ----------

        
        html.Div(style={'backgroundColor': '#4F7942','font-size': '1.5em','borderRadius': '5px'}, children=[
            html.H2('Team Evaluation'),
        ]),
        
            html.Div(style={'marginBottom': '60px'}, children=[
            html.H2('Dissecting The Teams''Performance'),
            html.P("Let us visit again the previous performance aspects for the teams!. For that we will rely on a radar chart, which is quite good for performing cross comparison. \
                   Again we dive into the defense, offense, distribution, disciplinary, goals and gols keeping  profiles of the teams, through exploiting pertinent spatics pertaining to those. \
                   All the displayed values correspond to the total per team. We do not want winners devoid of sportsmanship; this is why we are scrutinizing the disciplinary aspects of the competitors!"),

            html.H2('Offensive Team Analysis'),
            html.Div(style={'width': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'flexDirection' : 'row'}, children=[
                html.Div(style={'width': '60%', 'padding': '10px'}, children=[
                    add_graph(id='radar-chart_offense', figure=fig_offense_team)
                ]),
                html.Div(style={'width': '35%', 'padding': '10px'}, children=[
                    html.Table(children=[
                        html.Thead(children=html.Tr(children=[
                            html.Th('Name'),
                            html.Th('Description')
                        ])
                        ),

                        
                        html.Tr(children=[
                                html.Td('Recovered balls'),
                                html.Td('When a player regains possession of the ball from the opposing team. ')
                            ]),

                            html.Tr(children=[
                                html.Td('Tackles'),
                                html.Td('When a player uses their feet to challenge an opponent for the ball.')
                            ]),

                            html.Tr(children=[
                                html.Td('Clearances'),
                                html.Td('When a player kicks the ball away from their goal area to prevent the opposing team from scoring.')
                            ]),

                            html.Tr(children=[
                                html.Td('Blocks'),
                                html.Td('When a player stops the ball from advancing, typically a shot or pass, by using their body.')
                            ]),



                        ])
                    ])
                ])
            ])
        ]),


        

        # -------DEFENSE ----------"""






        html.Div(style={'marginBottom': '60px'}, children=[
            html.H2('Defensive Team analysis'),
            
            html.Div(style={'width': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'flexDirection' : 'row'}, children=[
                
                html.Div(style={'width': '60%', 'padding': '10px'}, children=[
                    add_graph(id='radar-chart_defense', figure=fig_defense_team)
                ]),

                html.Div(style={'width': '35%', 'padding': '10px'}, children=[
                    
                    html.Table(children=[
                        html.Thead(children=html.Tr(children=[
                            html.Th('Name'),
                            html.Th('Description')
                        ])
                        ),

                    

                        html.Tbody(children=[

                           html.Tbody(children=[

                            html.Tr(children=[
                                html.Td('Assist'),
                                html.Td('Final pass or touch leading directly to a goal. ')
                            ]),

                            html.Tr(children=[
                                html.Td('Corner'),
                                html.Td('Kick awarded to an attacking team when the ball goes over the goal line after last being touched by a defending player.')
                            ]),

                            html.Tr(children=[
                                html.Td('Offside'),
                                html.Td('violation occurring when an attacking player is positioned nearer to the opponent goal line when the ball is passed to him.')
                            ]),

                        ])

                    ])

                ])


            ])



        ]),

        
    



 #-------DISTRIBUTION----------"""

        html.Div(style={'marginBottom': '60px'}, children=[
            html.H2('Distribution Team analysis'),
            
            html.Div(style={'width': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'flexDirection' : 'row'}, children=[
                
                html.Div(style={'width': '60%', 'padding': '10px'}, children=[
                    add_graph(id='radar-chart_distribution', figure=fig_dist_team)
                ]),

                html.Div(style={'width': '35%', 'padding': '10px'}, children=[
                    
                    html.Table(children=[
                        html.Thead(children=html.Tr(children=[
                            html.Th('Name'),
                            html.Th('Description')
                        ])
                        ),

                    

                        html.Tbody(children=[

                            html.Tr(children=[
                                html.Td('Passes attempted'),
                                html.Td('Total number of attempts a player made kicking, heading, or moving the ball to a teammate. ')
                            ]),

                            html.Tr(children=[
                                    
                                html.Td('Passes completed'),
                                html.Td('Number of passes that successfully reach a teammate.')
                            ]),

                            html.Tr(children=[
                                html.Td('Crosses attempted'),
                                html.Td('Number of times a player attempts to send the ball from the wide areas to the penalty area of opponent .')
                            ]),

                            html.Tr(children=[
                                html.Td('Crosses completed'),
                                html.Td('Number of successful crosses that reach a teammate.')
                            ]),

                            html.Tr(children=[
                                html.Td('Free kicks on goal'),
                                html.Td('Restarting play after a foul or other infringement has occurred with the intention of scoring a goal.')
                            ]),







                        ])

                    ])

                ])


            ])



        ]),

    

     #-------DISCIPLINARY ----------"""



        html.Div(style={'marginBottom': '60px'}, children=[
            html.H2('Disciplinary Team analysis'),
            
            html.Div(style={'width': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'flexDirection' : 'row'}, children=[
                
                html.Div(style={'width': '60%', 'padding': '10px'}, children=[
                    add_graph(id='radar-chart_discipline', figure=fig_discip_team)
                ]),

                html.Div(style={'width': '35%', 'padding': '10px'}, children=[
                    
                    html.Table(children=[
                        html.Thead(children=html.Tr(children=[
                            html.Th('Name'),
                            html.Th('Description')
                        ])
                        ),

                        html.Tbody(children=[

                            html.Tr(children=[
                                html.Td('Fouls committed'),
                                html.Td('Number of times a player breaks the rules resulting in a free kick or penalty for the opposing team ')
                            ]),

                            html.Tr(children=[
                                html.Td('Yellow cards'),
                                html.Td('Cautions given to a player by the referee for serious fouls or misconduct')
                            ]),

                            html.Tr(children=[
                                html.Td('Fouls suffered'),
                                html.Td('Numberz of times a player is fouled by an opponent.')
                            ]),

                            html.Tr(children=[
                                html.Td('Red cards'),
                                html.Td('Send-off given to players for serious fouls or misconduct, resulting in their removal from the game')
                            ]),






                        ])

                    ])

                ])


            ])



        ]),


        #-------Goals----------"""

        html.Div(style={'marginBottom': '60px'}, children=[
            html.H2('Goals Team Performance'),
            
            html.Div(style={'width': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'flexDirection' : 'row'}, children=[
                
                html.Div(style={'width': '60%', 'padding': '10px'}, children=[
                    add_graph(id='radar-chart_goals', figure=fig_goals)
                ]),

                html.Div(style={'width': '35%', 'padding': '10px'}, children=[
                    
                    html.Table(children=[
                        html.Thead(children=html.Tr(children=[
                            html.Th('Name'),
                            html.Th('Description')
                        ])
                        ),

                        html.Tbody(children=[

                            html.Tr(children=[
                                html.Td('Goals scored'),
                                html.Td('Total number of goals a player or team scores')
                            ]),

                            html.Tr(children=[
                                html.Td('Goals scored in open play'),
                                html.Td('Goals scored during the normal course of the game, not from set-pieces or penalties')
                            ]),

                            html.Tr(children=[
                                html.Td('Goals scored on penalty'),
                                html.Td('Goals scored directly from a corner kick or resulting from the play immediately following a corner')
                            ]),

                            html.Tr(children=[
                                html.Td('Goals scored on corner'),
                                html.Td('Distance Covered by Forward Carries / Total Distance Covered by Carries')
                            ]),
                            
                            html.Tr(children=[
                                html.Td('Goals scored on penalty phase'),
                                html.Td('Goals scored during the penalty phase, which includes penalty shootouts or the immediate play following a penalty')
                            ]),

                            html.Tr(children=[
                                html.Td('Goals on set pieces'),
                                html.Td('Goals scored from set-pieces such as free kicks, corners, or throw-ins')
                            ]),


                            

                        ])

                    ])

                ])


            ])



        ]),

    

        
        #-------Goals Keeping----------"""

        html.Div(style={'marginBottom': '60px'}, children=[
            html.H2('Goals Keeping Team Performance'),
            
            html.Div(style={'width': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'flexDirection' : 'row'}, children=[
                
                html.Div(style={'width': '60%', 'padding': '10px'}, children=[
                    add_graph(id='radar-chart_goals_keep', figure=fig_goals_keep)
                ]),

                html.Div(style={'width': '35%', 'padding': '10px'}, children=[
                    
                    html.Table(children=[
                        html.Thead(children=html.Tr(children=[
                            html.Th('Name'),
                            html.Th('Description')
                        ])
                        ),

                        html.Tbody(children=[

                            html.Tr(children=[
                                html.Td('Saves'),
                                html.Td('When a goalkeeper successfully stops the ball from entering the goal ')
                            ]),

                            html.Tr(children=[
                                html.Td('Goals conceded'),
                                html.Td('Number of goals a team allows the opposing team to score')
                            ]),

                            html.Tr(children=[
                                html.Td('Own goals'),
                                html.Td('Goals scored accidentally by a player into the goal of his own team')
                            ]),

                            html.Tr(children=[
                                html.Td('Saves from penalty'),
                                html.Td('When a goalkeeper prevents a goal from being scored during a penalty kick')
                            ]),
                            html.Tr(children=[
                                html.Td('Punches'),
                                html.Td('When a goalkeeper uses his fists to clear the ball away from the goal area')
                            ]),


                        ])

                    ])

                ])


            ])



        ]),

    

    

        #--------------------------------------------------------------------OTHER CHARACTERISTICS : VIOLON CHART--------------------------------------------------------------------------------------------"""

        
        html.Div(style={'marginBottom': '60px'}, children=[
            html.H2('Additional Analysis'),
            html.P("We're turning to the trusty violin plot to shed some light on hidden yet key factors which made the difference between the two teams having competed for the title at the finals: the distribution of the playing time on the pitch per player , \
                   and the distribution of the attempts across the matches per player within the squads. \
                   Compared to England, it is observed that Italian players exhibit a more uniform playing time, showing that all had spent a close time on the field. \
                   Furthermore, the number of attempts is close among the Italian players, since most have performed either 1 or 2. \
                   Apparently the Italian team was coherent and well-synchronized, and this made the difference!"),
            add_graph(id='violin-attempts', figure=violon_team.draw_figure(df=violon_team.prep_data_violin(), column="Total Attempts")),
            add_graph(id='violin-played_time', figure=violon_team.draw_figure(df=violon_team.prep_data_violin(), column="Played Time")),
            """  add_graph(id='violin-goals_op', figure=violon_team.draw_figure(df=violon_team.prep_data_violin(), column="Goals scored in open play")),
            add_graph(id='violin-goals_set_pieces', figure=violon_team.draw_figure(df=violon_team.prep_data_violin(), column="Goals on set pieces")), """

        ]),
  ])
])


@app.callback(
    Output('team-graphs', 'children'),
    [Input('team-selector', 'value')]
)

def update_graphs(selected_team):
    fig_offense, fig_defense = get_team_figures(selected_team)
    print("je update")
    return [
        add_graph(id='barchart-offense', figure=fig_offense),
        add_graph(id='barchart-defense', figure=fig_defense)
    ]

@app.callback(
    Output('lineup-graph', 'children'),
    [Input('lineup-team-selector', 'value')]
)
def update_lineup_chart(selected_team):
    fig_lineup = create_lineup_chart(selected_team)
    return add_graph(id='lineup-chart', figure=fig_lineup)

@server.route('/index')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run_server(debug=True)
