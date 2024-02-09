# Import packages
from dash import Dash, html, dcc, dash_table, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
#import geobr

# Incorporate data
std = pd.read_csv('Estados_Siglas_Num.csv', sep=';')
std1 = std.loc[:,["COD_UF","NAME_UF"]]
std1["COD_UF"] = std1["COD_UF"].astype(str)
std1 = std1.sort_values(by=["NAME_UF"])
states = dict(std1.values.tolist())
#states = munic["UF"].unique()
munic = pd.read_csv('https://mipconsult.com.br/simula/database/MUNIC_IBGE.csv', sep=';')
dados = pd.read_csv('cl_Dados_2010_21.csv')
#
#brmunic = geobr.read_municipality(code_muni="all", year=2010)

# Initialize the app
app = Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])# MINTY

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.H2("PIB dos Municípios Brasileiros", className="display-3"),
        html.Hr(className="my-2")
    ], className="bg-primary text-center"),
    #
    dbc.Row([ # linha 1
        #
        dbc.Col([ # coluna 1
            dbc.Row([
                # SELEÇÃO DO ESTADO
                html.Div(children='Selecione o Estado:'),#searchable=False
                dcc.Dropdown(states,"41", id="statesSelect"),
                html.Br(),
                # SELEÇÃO DO MUNICÍPIO
                html.Div(children='Selecione o Município:'),
                dcc.Dropdown(searchable=False, id="municSelect"),
                html.Br(),
                html.Div(id='dd-output-container'),
                html.Hr(className="my-2"),
                html.Br(),
                # MAPA DO BRASIL COM DESTAQUE PARA O ESTADO
                html.Div(children="Mapa do Brasil"),
                dcc.Graph(id='mapa_BR'),
                html.Br(),
                # MAPA DO ESTADO COM DESTAQUE O MUNICÍPIO
                html.Div(children="Mapa do Estado"),
                dcc.Graph(id='mapa_est')
            ])

        ],width=4,style={'background-color':'#ADD8E6'}), # fim da coluna 1
        #
        dbc.Col([ # coluna 2
            dbc.Row([
                dash_table.DataTable(data=munic.to_dict('records'), page_size=10),
                html.Br(),
                dcc.Graph(id='plot_pie')
            ])

        ],width=8,style={'background-color':'#ADD8FF'}) # Fim da coluna 2

    ]) # fim da linha 1

],fluid=True) # fim do container
#
@callback(
    Output('municSelect', 'options'),
    Input('statesSelect', 'value')
)
def update_output(value):
    selec = munic[munic["COF_UF"] == int(value)] # selecionando o estado
    select1 = selec.loc[:,["COD_MUNIC","NOME_MUNIC"]] # selecionando as colunas
    #select1 = select1.values.tolist() # convertendo para lista
    select = dict(select1.values.tolist()) # convertendo para dictionary1
    #if not value:
    #    raise PreventUpdate
    #return [o for o in options if value in o['label']]
    return select


@callback(
    Output('dd-output-container', 'children'),
    Input('municSelect', 'value'),
    Input('statesSelect', 'value')
)
def update_output(municSelect,statesSelect):
    est = std[std['COD_UF']==int(statesSelect)].iloc[0,1]
    selec = munic[munic["COD_MUNIC"] == int(municSelect)].iloc[0,4]
    return f'Você selecionou: {selec} - {est}'

# construção do mapa
#@callback(
#     Output('plot_maps','figure'),
#     Input('statesSelect', 'value'),
#     Input('municSelect', 'value')
#)
# def namefunction():
# statemap = brmunic.query("code_state == 41")
# return figure


# gráfico do pib
#@callback(
#     Output('plot_pie','figure'),
#     Input('municSelect', 'value')
#)
#def plotpie(value):
#    munic_serie = Dados_Geral[Dados_Geral["COD_Munic"] == int(value)]
#    Dados_VA = munic_serie.iloc[11,9:13]
#    labels = ['Agropecuária','Indústria','Serviços','Adm. Pública']
#    fig = px.pie(data_frame=Dados_VA, names=labels)
#    return fig


if __name__ == '__main__':
    app.run(debug=True)