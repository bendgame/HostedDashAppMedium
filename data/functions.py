import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import dash_bootstrap_components as dbc

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
from data import transforms
df = transforms.df
top_df = transforms.top_df
bottom_df = transforms.bottom_df

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

def card1():
    card = dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Percent of Records", className="card-title"),
                        html.Div(id = 'piegraph-child')       
    
                    ]
                )
            )
    return card

def cardDeck():
    cards = dbc.CardDeck(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Avg Price", className="card-title"),
                        html.P( id = "avg-price",
                            className="card-text",
                        )
    
                    ]
                )
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Avg Rating", className="card-title"),
                        html.P(
                             id = 'avg-rating'   
                            ,className="card-text"
                        )
    
                    ]
                )
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Records", className="card-title"),
                        html.P(id ='records'
                            
                            ,className="card-text"
                        )

                    ]
                )
            ),
        ]
    )
    return cards


def graph():
    graph =  dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=['Day 1','Day 2','Day 3','Day 4','Day 5','Day 6','Day 7'
                        ,'Day 8','Day 9','Day 10','Day 11','Day 12','Day 13',],
                    y=[1, 0, .5, 2, 0, 0, 2.5, 0, 0, .5,
                    .5, 0, 1, 0 ],
                    name='My Daily Wine Consumption (Glasses)',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ),
                dict(
                    x=['Day 1','Day 2','Day 3','Day 4','Day 5','Day 6','Day 7'
                        ,'Day 8','Day 9','Day 10','Day 11','Day 12','Day 13',],
                    y=[1.5, .5, 0, 1, 0, 0, 2, 0, .5, 0,
                    .5, 0, .5, .5 ],
                    name='Wife Daily Wine Consumption (Glasses)',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title='Daily Wine Consumption (Me v.s. Wife)',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph'
    ) 
    return graph


def top_table():
    table = dbc.Table.from_dataframe(top_df, striped=True, bordered=True, hover=True, responsive = 'xl')
    return table
def bottom_table():
    table = dbc.Table.from_dataframe(bottom_df, striped=True, bordered=True, hover=True, responsive = 'xl')
    return table