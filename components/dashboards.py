from gc import callbacks
from tracemalloc import start
from turtle import width
from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
#from globals import *
from app import app

card_icon = {
    'color': 'white',
    'text-align': 'center', 
    'font-size': '30px',
    'margin':'auto',
}

# =========  Layout  =========== #
layout = dbc.Col([
       dbc.Row([
           
           # saldo-----
           dbc.Col([
               dbc.CardGroup([
                   dbc.Card([
                       html.Legend('Saldo'),
                       html.H5('R$ 5400', id='p-saldo-dashboards', style={})
                   ], style={'padding-left':'20px', 'padding-top':'10px'}),
                    dbc.Card(
                        html.Div(className='fa fa-university', style=card_icon),
                        color='warning',
                        style={'max-width':75, 'height': 100, 'margin-left':'-10px'}
                    )
               ])
           ], width=4),
           
           # receita -----
           dbc.Col([
               dbc.CardGroup([
                   dbc.Card([
                       html.Legend('Receita'),
                       html.H5('R$ 10000', id='p-receita-dashboards', style={})
                   ], style={'padding-left':'20px', 'padding-top':'10px'}),
                    dbc.Card(
                        html.Div(className='fa fa-smile-o', style=card_icon),
                        color='success',
                        style={'max-width':75, 'height': 100, 'margin-left':'-10px'}
                    )
               ])
           ], width=4),
           
           # despesa-----
           dbc.Col([
               dbc.CardGroup([
                   dbc.Card([
                       html.Legend('Despesa'),
                       html.H5('R$ 3500', id='p-despesa-dashboards', style={})
                   ], style={'padding-left':'20px', 'padding-top':'10px'}),
                    dbc.Card(
                        html.Div(className='fa fa-meh-o', style=card_icon),
                        color='danger',
                        style={'max-width':75, 'height': 100, 'margin-left':'-10px'}
                    )
               ])
           ], width=4),
       ], style={'margin':'10px'}),
       
       dbc.Row([
           dbc.Col([
               dbc.Card([
                   html.Legend('Filtrar lançamentos', className='card-title'),
                   html.Label('Categoria das Receitas'),
                   html.Div(
                       dcc.Dropdown(
                           id='dropdow-receita',
                           clearable=False,
                           style={'width': '100%'},
                           persistence=True,
                           persistence_type='session',
                           multi=True,
                       )
                    ),
                       
                    html.Label('Categoria das Despesas', style={'margin-top': '10px'}),
                    html.Div(
                        dcc.Dropdown(
                            id='dropdow-despesa',
                            clearable=False,
                            style={'width': '100%'},
                            persistence=True,
                            persistence_type='session',
                            multi=True,
                        )   
                    ),
                    
                    html.Legend('Período de Análise', style={'margin-top': '10px'}),
                    dcc.DatePickerRange(
                        month_format='Do MMM ,YY',
                        end_date_placeholder_text='data...',
                        start_date=datetime.today(),
                        end_date=datetime.today() + timedelta(days=31),
                        updatemode='singledate',
                        id='date-picker-config',
                        style={'z-index':'100'}
                    )
               ], style={'height':'100%', 'padding':'20px'})
           ], width=4),
           
           dbc.Col(
               dbc.Card(dcc.Graph(id='graph1'),style={'height':'100%', 'padding':'10px'}), width=8
            ),
       ], style={'margin':'10px'}),
       
       dbc.Row([
           dbc.Col(dbc.Card(dcc.Graph(id='graph2'),style={'padding':'10px'}), width=6),
           dbc.Col(dbc.Card(dcc.Graph(id='graph3'),style={'padding':'10px'}), width=3),
           dbc.Col(dbc.Card(dcc.Graph(id='graph4'),style={'padding':'10px'}), width=3),
       ], style={'padding':'10px'})
    ])



# =========  Callbacks  =========== #
@app.callback(
    [
        Output('dropdow-receita', 'options'),
        Output('dropdow-receita', 'value'),
        Output('p-receita-dashboards','children'),
    ],
    Input('store-receitas', 'data')   
)
def populateDropdownValues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()
    dReceitas = [{'label' : x, 'value': x} for x in val]
    return [dReceitas, val, f'R${valor:.2f}']

@app.callback(
    [
        Output('dropdow-despesa', 'options'),
        Output('dropdow-despesa', 'value'),
        Output('p-despesa-dashboards','children'),
    ],
    Input('store-despesas', 'data')   
)
def populateDropdownValues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()
    dReceitas = [{'label' : x, 'value': x} for x in val]
    return [dReceitas, val, f'R${valor:.2f}']


@app.callback(
    Output('p-saldo-dashboards', 'children'),
    [
        Input('store-despesas', 'data'),
        Input('store-receitas', 'data')
    ]
)
def saldoTotal(despesas, receitas):
    df_despesas = pd.DataFrame(despesas)
    df_receitas = pd.DataFrame(receitas)
    
    total = df_receitas['Valor'].sum() - df_despesas['Valor'].sum()
    
    return f'R${total:.2f}'