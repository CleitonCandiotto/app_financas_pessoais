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
from globals import *
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


@app.callback(
    Output('graph1', 'figure'),
    [
        Input('store-receitas', 'data'),
        Input('store-despesas', 'data'),
        Input('dropdow-receita', 'value'),
        Input('dropdow-despesa', 'value'),
    ]
)
def update_output(data_receita, data_despesa, despesa, receita):
    #import pdb
    #pdb.set_trace()
    grap_margin = dict(l=25, r=25, t=25, b=0)
    
    df_receitas = pd.DataFrame(data_receita).set_index('Data')[['Valor']]
    df_rc = df_receitas.groupby('Data').sum().rename(columns={'Valor':'Receitas'})
    
    df_despesas = pd.DataFrame(data_despesa).set_index('Data')[['Valor']]
    df_ds = df_despesas.groupby('Data').sum().rename(columns={'Valor':'Despesas'})
    
    df_acum = df_rc.join(df_ds, how='outer').fillna(0)
    
    df_acum['Acum'] = df_acum['Receitas'] - df_acum['Despesas']
    df_acum['Acum'] = df_acum['Acum'].cumsum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Fluxo de Caixa', x=df_acum.index, y=df_acum['Acum'], mode='lines'))
    fig.update_layout(margin=grap_margin)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    return fig


@app.callback(
    Output('graph2','figure'),
    [
        Input('store-receitas', 'data'),
        Input('store-despesas', 'data'),
        Input('dropdow-receita', 'value'),
        Input('dropdow-despesa', 'value'),
        Input('date-picker-config', 'start_date'),
        Input('date-picker-config', 'end_date')
    ]
)
def graph2_show(data_receita, data_despesa, receita, despesa, start_date, end_date):
    
    grap_margin = dict(l=25, r=25, t=25, b=0)

    df_rc = pd.DataFrame(data_receita)
    df_ds = pd.DataFrame(data_despesa)
    
    df_rc['Output'] = 'Receitas'
    df_ds['Output'] = 'Despesas'
    df_final = pd.concat([df_rc, df_ds])
    df_final['Data'] = pd.to_datetime(df_final['Data'])
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    #passando filtros
    df_final = df_final[(df_final['Data'] >= start_date) & (df_final['Data'] <= end_date)]
    df_final = df_final[(df_final['Categoria'].isin(receita)) | (df_final['Categoria'].isin(despesa))]
    
    fig = px.bar(df_final, x='Data', y='Valor', color='Output', barmode='group')
    fig.update_layout(margin=grap_margin, height=350)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    return fig


@app.callback(
    Output('graph3', 'figure'),
    [
        Input('store-receitas', 'data'),
        Input('dropdow-receita', 'value'),
    ]   
)
def pie_receita(data_receita, receita):
    grap_margin = dict(l=25, r=25, t=25, b=0)
    
    df = pd.DataFrame(data_receita)
    df = df[df['Categoria'].isin(receita)]
    
    fig = px.pie(df, values=df['Valor'], names=df['Categoria'], hole=.2 )
    fig.update_layout(title={'text':'Receitas'})
    fig.update_layout(margin=grap_margin, height=350)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig


@app.callback(
    Output('graph4', 'figure'),
    [
        Input('store-despesas', 'data'),
        Input('dropdow-despesa', 'value'),
    ]   
)
def pie_receita(data_despesa, despesa):
    grap_margin = dict(l=25, r=25, t=25, b=0)
    
    df = pd.DataFrame(data_despesa)
    df = df[df['Categoria'].isin(despesa)]
    
    fig = px.pie(df, values=df['Valor'], names=df['Categoria'], hole=.2 )
    fig.update_layout(title={'text':'Despesas'})
    fig.update_layout(margin=grap_margin, height=350)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig