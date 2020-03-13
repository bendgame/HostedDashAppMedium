import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_table 
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import urllib


from data import functions, transforms

from pages import navbar, layout, printpage


navbar = navbar.navbar()
layout = layout.home_layout()
printpage = printpage.print_layout()

card = functions.card1()
cards = functions.cardDeck()
graph = functions.graph()
top_table = functions.top_table()
bottom_table = functions.bottom_table()
df = transforms.df

PAGE_SIZE = 50

app = dash.Dash(__name__, meta_tags=[{ "content": "width=device-width"}], external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
         return layout
    elif pathname == '/print':
         return printpage
    else:
        return layout


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


#######################################
## Call backs
#######################################

@app.callback(Output('avg-price', 'children'),
              [Input('variety-drop', 'value')])
def avgprice(variety):
    var = variety
    dff = transforms.df
    avgprice = dff[['variety', 'price']].groupby(['variety']).mean()
    avgprice = avgprice.reset_index()
    avgprice = avgprice.loc[avgprice['variety'] == var]
    
    return avgprice['price'].round(2)

@app.callback(Output('avg-rating', 'children'),
              [Input('variety-drop', 'value')])
def avgrating(variety):
    var = variety
    dff = transforms.df
    avgrating = dff[['variety', 'rating']].groupby(['variety']).mean()
    avgrating = avgrating.reset_index()
    avgrating = avgrating.loc[avgrating['variety'] == var]
    
    return avgrating['rating'].round(2)

@app.callback(Output('records', 'children'),
              [Input('variety-drop', 'value')])
def records(variety):
    var = variety
    dff = transforms.df
    records = dff.loc[dff['variety'] == var].count()
    
    return records['variety']

##############################################
## Pie graph
##############################################

@app.callback(Output('piegraph-child', 'children'),
            [Input('variety-drop', 'value')])
def make_pie(variety):
    dff = transforms.percent
    dff = dff.loc[dff['variety']== variety]
    dff = dff.reset_index()
    a = dff['contribution'].round(3)
    b = dff['remainder'].round(3)

    
    data = [
            {
                'values': [a[0], b[0]]
                ,'labels': [variety, 'Total']
                ,'type': 'pie'
                ,'hole':.3
            },
        ]
    piegraph =  dcc.Graph(
            id='piegraph',
            figure={
                'data': data,
                'layout': {
                      
                    'margin': {
                        'l': 20,
                        'r': 0,
                        'b': 20,
                        't': 0
                    },
                    'legend': {'x': variety, 'y': 'Total'}
                    
                }
            }
        )
    return piegraph

##############################################
## Data Table
##############################################



@app.callback(
    Output('full-table', 'data'),
    [Input('full-table', "page_current"),
     Input('full-table', "page_size"),
     Input('full-table', 'sort_by'),
     Input('full-table', 'filter_query')])
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = functions.split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')

@app.callback(Output('my-link', 'href')
            , [Input('full-table', "page_current"),
     Input('full-table', "page_size"),
     Input('full-table', 'sort_by'),
     Input('full-table', 'filter_query')])
def update_table2(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = functions.split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )


    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + urllib.parse.quote(csv_string)
    return csv_string

if __name__ == '__main__':
    app.run_server(debug=True)