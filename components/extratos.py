from turtle import width
import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from app import app

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        html.Legend('Tabela de Despesas'),
        html.Div(id='tabela-despesas', className='dbc')
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph', style={'margin-right': '20px'}),
        ], width=9),
        
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4('Despesas'),
                    html.Legend('R$ 4400', id='valor_despesas_card', style={'font-size':'60px'}),
                    html.H6('Total despesas')
                ], style={'text-align':'center', 'padding-top':'30px'})
            )
        ],width=3)
    ])
], style={'padding':'10px',} )

# =========  Callbacks  =========== #
# Tabela
@app.callback(
    Output('tabela-despesas', 'children'),
    Input('store-despesas', 'data')
)
def imprimir_tabela(data):
    df = pd.DataFrame(data)
    df['Data'] = pd.to_datetime(df['Data']).dt.date
    df = df.fillna('-')
    df.sort_values(by='Data', ascending=False)
    figure = app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    return figure


@app.callback(
    Output('bar-graph', 'figure'),
    Input('store-despesas', 'data')
)
def bar_chart(data):
    df = pd.DataFrame(data)
    dfGrouped = df.groupby('Categoria').sum()[['Valor']].reset_index()
    graph = px.bar(dfGrouped, x='Categoria', y='Valor', title='Despesas Gerais')
    graph.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return graph
    

@app.callback(
    Output('valor_despesas_card', 'children'),
    Input('store-despesas', 'data')
)
def valor_card_despesa(data):
    df = pd.DataFrame(data)
    Valor = df['Valor'].sum()
    return f'R${Valor}'
