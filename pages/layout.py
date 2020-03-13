import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_table 
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import urllib

from data import functions, transforms

from pages import navbar
#from index import app, server

navbar = navbar.navbar()

card = functions.card1()
cards = functions.cardDeck()
graph = functions.graph()
top_table = functions.top_table()
bottom_table = functions.bottom_table()
df = transforms.df

PAGE_SIZE = 50

def home_layout():

    layout = html.Div([navbar 
            , html.Div(html.P())
            , dbc.Row([
            dbc.Col([ dbc.Card(dbc.CardBody([
            html.Div([html.H5("Variety")
                ,html.P(dcc.Dropdown(id = 'variety-drop'
                        ,options=[{
                    'label': c
                    ,'value': c}
                    for c in sorted(transforms.variety)]
                        ,value="Chardonnay"
            ))])
            ]))#end card
        ], width = 4)#end col

        , dbc.Col([cards], width= 7, align="center")


        ], justify = 'center')#end row 1
        , html.Div(html.P())
        , dbc.Row([html.Div(html.P(' '))
            
            , dbc.Col([card], width = 4) #end col 
            , dbc.Col([dbc.Card(dbc.CardBody(graph))],width = 7)
            ], justify = 'center')#end row 2

        , html.Div(html.P(" "))
        , dbc.Row(html.P(" "))
        ,dbc.Row([html.Div(html.P(" ")) ,dbc.Col(dbc.Container([ html.H5("Most Reviewed Wines")
        , top_table

        ]), width = 5)
        , dbc.Col(dbc.Container([ html.H5("Least Reviewed Wines")
        , bottom_table

        ]), width = 5)
        ], justify = 'center')
        ,html.Div(html.P(' '))
        , dbc.Row(html.P(" "))
        , dbc.Row([html.Div(html.P(' ')), html.Div(html.P(' ')), html.Div(html.P(' '))

                ], justify = 'center')
        , dbc.Row(html.P(' '))
        , dbc.Row(html.P(' '))
        , dbc.Container(dbc.Card(dbc.CardBody([html.H3('Raw Data')
            , html.H5('Sort and filter Data Table. Export as needed.')
            , html.A('Download CSV', id='my-link', download="data.csv",
            href="",
            target="_blank")
            , dash_table.DataTable(
            id='full-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            page_current= 0,
            page_size= PAGE_SIZE,
            page_action='custom',

            filter_action='custom',
            filter_query='',

            sort_action='custom',
            sort_mode='multi',
            sort_by=[]
        )])
        )#end card
        )#end container


        ])# end div
    return layout