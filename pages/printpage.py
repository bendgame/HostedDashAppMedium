import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
#import praw
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
#from config import cid, csec, uag

from data import functions, transforms

from pages import navbar


navbar = navbar.navbar()

card = functions.card1()
cards = functions.cardDeck()
graph = functions.graph()
top_table = functions.top_table()
bottom_table = functions.bottom_table()
df = transforms.df




def print_layout():
    layout = html.Div([ dbc.Row(html.P(' '))
            
            , dbc.Row([dbc.Col(width = 1)
            ,dbc.Col([
                html.Div([html.H5("Variety")
                        ]) #end div
                , html.P(dcc.Dropdown(id = 'variety-drop'
                        , options=[{
                            'label': c
                            ,'value': c}
                        for c in sorted(transforms.variety)]
                            , value="Chardonnay"
                    ))
                , html.Div(card)
                , html.Div(html.P(" "))
                , html.Div(cards)
                , html.Div(html.P(" "))
                , html.Div(top_table)
                , dbc.Row(html.P(' '))
                , html.Div(bottom_table)
                , dbc.Row(html.P(' '))
                , html.Div(graph)
        
        
            ], width = 5)# End Col
            ])#End row

    ]) #end div
    return layout
