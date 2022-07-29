from ast import In
import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd

from globals import *


# ========= Layout ========= #
layout = dbc.Col([
                html.H1('MyFinanc.', className='text-primary'),
                html.P('by cleiton', className='text-info'),
                html.Hr(),
                
                # secção perfil --------
                dbc.Button(id='botao-avatar',
                           children=[html.Img(src='/assets/img_hom.png', id='avatar_change', alt='Avatar', className='perfil_avatar')
                            ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
                
                # secção novo--------
                dbc.Row([
                    dbc.Col([
                        dbc.Button(color='success',id='open-novo-receita',
                                   children=['+ Receita'])
                    ], width=6),
                    dbc.Col([
                        dbc.Button(color='danger',id='open-novo-despesa',
                                   children=['- Despesa'])
                    ], width=6)
                ]),
                # modal receita --------
                dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle('Adicionar receita')),
                    dbc.ModalBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Descrição: '),
                                dbc.Input(placeholder='Ex: dividendos da bolsa, hereança...', id='txt-receita')
                            ], width=6),
                            
                            dbc.Col([
                                dbc.Label('Valor: '),
                                dbc.Input(placeholder='R$100', id='valor-receita', value='')
                            ], width=6),
                        ]),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Data: '),
                                dcc.DatePickerSingle(id='date-receitas',
                                                    min_date_allowed=date(2020, 1, 1),
                                                    max_date_allowed=date(2030, 12, 31),
                                                    date=datetime.today(),
                                                    style={'width':'100%'}
                                                    ),
                            ], width=4),
                            
                            dbc.Col([
                                dbc.Label('Extras'),
                                dbc.Checklist(
                                    options=[
                                        {'label': 'Recebido', 'value': 1 },
                                        {'label': 'Recorente', 'value': 2 }
                                        ],
                                    value=[1],
                                    id='switches-input-receita',
                                    switch=True
                                )
                            ], width=4),
                            
                            dbc.Col([
                                html.Label('Categoria de Receita'),
                                dbc.Select(id='select_receita',
                                           options=[{'label' : i, 'value' : i} for i in cat_receita],
                                           value=[cat_receita[0]]
                                           )
                            ], width=4)
                        ], style={'margin-top':'25px'}),
                        
                        dbc.Row([
                            dbc.Accordion([
                                dbc.AccordionItem(children=[
                                    dbc.Row([
                                        dbc.Col([
                                            html.Legend('Adicionar Cattegoria', style={'color':'green'}),
                                            dbc.Input(type='text', placeholder='Nova Categoria..', id='input-add-receita', value=''),
                                            html.Br(),
                                            dbc.Button('Adicionar', className='btn btn-success', id='add-category-receita', style={'margin-top':'20px'}),
                                            html.Br(),
                                            html.Div(id='category-div-add-receita', style={})
                                        ], width=6),
                                        
                                        dbc.Col([
                                            html.Legend('Excluir Categoria', style={'color': 'red'}),
                                            dbc.Checklist(
                                                id='checklist-select-style-receita',
                                                options=[{'label' : i, 'value' : i} for i in cat_receita],
                                                value=[],
                                                label_checked_style={'color': 'red'},
                                                input_checked_style={'color': 'orange'}
                                            ),
                                            dbc.Button('Remover', color='danger', id='remove-category-receita', style={'margin-top':'20px'}),
                                        ], width=6, style={'padding-left' : '20px'})
                                    ])
                                ], title='Adicionar/Remover Categoria')
                            ], flush=True, start_collapsed=True, id='accordion-receita '),
                            
                            html.Div(id='id_teste_receita', style={'padding-top':'20px'}),
                            dbc.ModalFooter([
                                dbc.Button('Adicionar Receita', id='salvar_receita', color='success'),
                                dbc.Popover(dbc.PopoverBody('Receita Salva'), target='salvar_receita', placement='left', trigger='click')
                            ], style={'margin-top':'20px'})
                        ])
                    ])
                ], id='modal-novo-receita'),
                
                # modal despesa --------
                dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle('Adicionar despesa')),
                    dbc.ModalBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Descrição: '),
                                dbc.Input(placeholder='Ex: dividendos da bolsa, hereança...', id='txt-despesa')
                            ], width=6),
                            
                            dbc.Col([
                                dbc.Label('Valor: '),
                                dbc.Input(placeholder='R$100', id='valor-despesa', value='')
                            ], width=6),
                        ]),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Label('Data: '),
                                dcc.DatePickerSingle(id='date-despesas',
                                                    min_date_allowed=date(2020, 1, 1),
                                                    max_date_allowed=date(2030, 12, 31),
                                                    date=datetime.today(),
                                                    style={'width':'100%'}
                                                    ),
                            ], width=4),
                            
                            dbc.Col([
                                dbc.Label('Extras'),
                                dbc.Checklist(
                                    options=[
                                        {'label': 'Pago', 'value': 1 },
                                        {'label': 'Recorente', 'value': 2 }
                                        ],
                                    value=[1],
                                    id='switches-input-despesa',
                                    switch=True
                                )
                            ], width=4),
                            
                            dbc.Col([
                                html.Label('Categoria de Despesa'),
                                dbc.Select(id='select_despesa',
                                           options=[{'label' : i, 'value' : i} for i in cat_despesa],
                                           value=[cat_despesa[0]]
                                           )
                            ], width=4)
                        ], style={'margin-top':'25px'}),
                        
                        dbc.Row([
                            dbc.Accordion([
                                dbc.AccordionItem(children=[
                                    dbc.Row([
                                        dbc.Col([
                                            html.Legend('Adicionar Cattegoria', style={'color':'green'}),
                                            dbc.Input(type='text', placeholder='Nova Categoria..', id='input-add-despesa', value=''),
                                            html.Br(),
                                            dbc.Button('Adicionar', className='btn btn-success', id='add-category-despesa', style={'margin-top':'20px'}),
                                            html.Br(),
                                            html.Div(id='category-div-add-despesa', style={})
                                        ], width=6),
                                        
                                        dbc.Col([
                                            html.Legend('Excluir Categoria', style={'color': 'red'}),
                                            dbc.Checklist(
                                                id='checklist-select-style-despesa',
                                                options=[{'label' : i, 'value' : i} for i in cat_despesa],
                                                value=[],
                                                label_checked_style={'color': 'red'},
                                                input_checked_style={'color': 'orange'}
                                            ),
                                            dbc.Button('Remover', color='danger', id='remove-category-despesa', style={'margin-top':'20px'}),
                                        ], width=6, style={'padding-left':'20px'})
                                    ])
                                ], title='Adicionar/Remover Despesa')
                            ], flush=True, start_collapsed=True, id='accordion-despesa '),
                            
                            html.Div(id='id_teste_despesa', style={'padding-top':'20px'}),
                            dbc.ModalFooter([
                                dbc.Button('Adicionar Despesa', id='salvar_despesa', color='success'),
                                dbc.Popover(dbc.PopoverBody('Despesa Salva'), target='salvar_despesa', placement='left', trigger='click')
                            ], style={'margin-top':'20px'})
                        ])
                    ])
                ], id='modal-novo-despesa'),
                
                #secção nav ------
                html.Hr(),
                dbc.Nav([
                    dbc.NavLink('Dashboard', href='/dashboards', active='exact'),
                    dbc.NavLink('Extratos', href='/extratos', active='exact'),
                ], vertical=True, pills=True, id='nav_buttons', style={'margin-button':'50px'}),
                
            ], id='sidebar-completa')



# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    Output('modal-novo-receita', 'is_open'), # saida do modal (aonde vai sair..)
    Input('open-novo-receita', 'n_clicks'), # botão do modal
    State('modal-novo-receita', 'is_open') 
)
def openModal(n1, is_open):
    '''n1= Input , is_open=State (precisa ser sempre na ordem delacara no callback'''
    
    if n1:
        return not is_open
    
# Pop-up despesa
@app.callback(
    Output('modal-novo-despesa', 'is_open'), # saida do modal (aonde vai sair..)
    Input('open-novo-despesa', 'n_clicks'), # botão do modal
    State('modal-novo-despesa', 'is_open') 
)
def openModal(n1, is_open):
    '''n1= Input , is_open=State (precisa ser sempre na ordem delacara no callback'''
    
    if n1:
        return not is_open

@app.callback(
    Output('store-receitas', 'data'),
    
    Input('salvar_receita','n_clicks'),
    [
        State('txt-receita', 'value'),
        State('valor-receita', 'value'),
        State("date-receitas", "date"),
        State('switches-input-receita', 'value'),
        State('select_receita', 'value'),
        State('store-receitas', 'data')      
    ]
    
)

def salveFormReceita(n, descricao, valor, date, switches, categoria, dictReceitas):
    #import pdb
    #pdb.set_trace()
    
    df_receitas = pd.DataFrame(dictReceitas)
    
    if n and not (valor == '' or valor==None):
        valor = round(float(valor),2)
        date = pd.to_datetime(date).date()
        categoria = categoria[0] if type(categoria) == list else categoria
        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0
        
        df_receitas.loc[df_receitas.shape[0]] = [valor, recebido, fixo, date, categoria, descricao ]
        df_receitas.to_csv('df_receitas.csv')
        
    data_return = df_receitas.to_dict()
    return data_return


@app.callback(
    Output('store-despesas', 'data'),
    
    Input('salvar_despesa','n_clicks'),
    [
        State('txt-despesa', 'value'),
        State('valor-despesa', 'value'),
        State("date-despesas", "date"),
        State('switches-input-despesa', 'value'),
        State('select_despesa', 'value'),
        State('store-despesas', 'data')      
    ]
    
)

def salveFormDespesa(n, descricao, valor, date, switches, categoria, dictDespesas):
    #import pdb
    #pdb.set_trace()   
    df_despesas = pd.DataFrame(dictDespesas)
    
    if n and not (valor == '' or valor==None):
        valor = round(float(valor),2)
        date = pd.to_datetime(date).date()
        categoria = categoria[0]
        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0
        
        df_despesas.loc[df_despesas.shape[0]] = [valor, recebido, fixo, date, categoria, descricao ]
        df_despesas.to_csv('df_despesas.csv')
        
    data_return = df_despesas.to_dict()
    return data_return


@app.callback(
    [
        Output('select_despesa', 'options'),
        Output('checklist-select-style-despesa', 'options'),
        Output('checklist-select-style-despesa', 'value'),
        Output('store-cat-despesas', 'data')
    ],
    [
        Input('add-category-despesa', 'n_clicks'),
        Input('remove-category-despesa', 'n_clicks')
    ],
    [
        State('input-add-despesa', 'value'),
        State('checklist-select-style-despesa', 'value'),
        State('store-cat-despesas', 'data')
    ]
)
def addCategory(n, n2, txt, check_delete, data):
    #import pdb
    #pdb.set_trace()
    cat_despesa = list(data['Categoria'].values())
    
    if n and not (txt == '' or txt ==None):
        '''adicionado uma categoria na lista de categoria'''
        cat_despesa = cat_despesa + txt if txt not in cat_despesa else cat_despesa
        
    if n2:
        if len(check_delete) > 0:
            '''reiterando subre a lista de categoria ignorandao a categoria selecionada'''
            cat_despesa = [i for i in cat_despesa if i not in check_delete]
    
    opt_despesas = [{'label': i, 'value':i} for i in cat_despesa]
    df_cat_despesas = pd.DataFrame(cat_despesa, columns=['Categoria'])
    df_cat_despesas.to_csv('df_cat_despesas.csv')
    data_return = df_cat_despesas.to_dict()
    
    return [opt_despesas, opt_despesas, [], data_return]


@app.callback(
    [
        Output('select_receita', 'options'),
        Output('checklist-select-style-receita', 'options'),
        Output('checklist-select-style-receita', 'value'),
        Output('store-cat-receitas', 'data')
    ],
    [
        Input('add-category-receita', 'n_clicks'),
        Input('remove-category-receita', 'n_clicks')
    ],
    [
        State('input-add-receita', 'value'),
        State('checklist-select-style-receita', 'value'),
        State('store-cat-receitas', 'data')
    ]
)
def addCategory(n, n2, txt, check_delete, data):
    #import pdb
    #pdb.set_trace()
    cat_receita = list(data['Categoria'].values())
    
    if n and not (txt == '' or txt ==None):
        '''adicionado uma categoria na lista de categoria'''
        cat_receita = cat_receita + [txt] if txt not in cat_receita else cat_receita
        
    if n2:
        if len(check_delete) > 0:
            '''reiterando sobre a lista de categoria ignorandao a categoria selecionada'''
            cat_receita = [i for i in cat_receita if i not in check_delete]
    
    opt_receitas = [{'label': i, 'value':i} for i in cat_receita]
    df_cat_receitas = pd.DataFrame(cat_receita, columns=['Categoria'])
    df_cat_receitas.to_csv('df_cat_receitas.csv')
    data_return = df_cat_receitas.to_dict()
    return [opt_receitas, opt_receitas, [], data_return]
