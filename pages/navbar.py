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

def navbar():
    navbar = dbc.Navbar([
        
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    #dbc.Col(html.Img(src=, height="30px")),
                    dbc.Col(dbc.NavbarBrand("   Wine Dashboard   ", className="ml-2")),
                ],
                align="right",
                no_gutters=True,
            ),
            href="/home",
        )
        ,  dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("Home", href="/home"),
                    dbc.DropdownMenuItem("Print", href="/print"),
                    
                ], style = {'list-style-type':'none'}
            )
        #dbc.NavbarToggler(id="navbar-toggler")
        #,
    ],
    color = '#F7E0FF',
    #'#92c83e',
    dark=False,
    )
    return navbar