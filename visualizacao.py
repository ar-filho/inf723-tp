# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = Dash(__name__)


df = pd.read_csv("arquivos/09_visualizacao_15.csv")
df_ap = pd.read_csv('arquivos/01df_ap.csv')
df_client = pd.read_csv('arquivos/01df_client.csv')
df_recon = pd.read_csv('arquivos/01df_recon.csv')
df_recon.index = df_recon.index + 1
df_ap.index = df_ap.index + 1
df_client.index = df_client.index + 1
df_tmpmean = pd.read_csv('arquivos/01df_tmpmean.csv')
df_tmpmean.index = df_tmpmean.index + 1
df_tmpstd = pd.read_csv('arquivos/01df_tmpstd.csv')
df_tmpstd.index = df_tmpstd.index + 1
df_ap['recon_mean'] = df_recon.mean().values
df_ap['tmpmean'] = df_tmpmean.mean().values
df_ap['tmpstd'] = df_tmpstd.mean().values
df_client['mobilidade'] = np.where(df_client.radio_known==1, 1,
                               np.where((df_client.radio_known>=2) & (df_client.radio_known<=4), 2,
                                        np.where((df_client.radio_known>=5) & (df_client.radio_known<=12), 3,
                                                 np.where((df_client.radio_known>=13) & (df_client.radio_known<=28), 4, 5))))
df_recon2 = df_recon.T
df_client['recon_mean'] = df_recon2.mean().values
df_recon2 = []
df_recon2 = df_tmpmean.T
df_client['tmpmean'] = df_recon2.mean().values
df_recon2 = []
df_recon2 = df_tmpstd.T
df_client['tmpstd'] = df_recon2.mean().values
df_recon2 = []

histograma = px.histogram(df, x="hora", color="mobilidade", color_discrete_sequence=px.colors.qualitative.Set1,)
histograma.update_layout( bargap = 0.2, legend_title_text='Mobilidade', xaxis = dict(tickmode = 'linear')) #tick0 = 0.5, dtick = 0.75
newnames = {'1': 'Fixo', '2': 'Baixa', '3': 'Média-Baixa', '4' : 'Média-Alta', '5' : 'Alta'}
histograma.for_each_trace(lambda t: t.update(name = newnames[t.name]))

semanal = px.histogram(df, x="semana",color="mobilidade", color_discrete_sequence=px.colors.qualitative.Set1,)
semanal.update_layout( bargap = 0.2, legend_title_text='Mobilidade', xaxis = dict(tickmode = 'array',tickvals = [0, 1, 2, 3, 4, 5, 6],ticktext = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']))
newnames = {'1': 'Fixo', '2': 'Baixa', '3': 'Média-Baixa', '4' : 'Média-Alta', '5' : 'Alta'}
semanal.for_each_trace(lambda t: t.update(name = newnames[t.name]))

ap1=21
ap2=13
x0 = df[(df['radio'] == ap1) ]['hora'].values
x1 = df[(df['radio'] == ap2) ]['hora'].values
compare = go.Figure()
compare.add_trace(go.Histogram(name="AP " +str(ap1),x=x0))
compare.add_trace(go.Histogram(name="AP " +str(ap2),x=x1))
compare.update_layout(barmode='overlay')
compare.update_traces(opacity=0.75)
compare.update_layout(
    bargap = 0.2,
    xaxis = dict(tickmode = 'linear'))

clients = px.histogram(df_client, x="quant_req", log_y=True)

radios = px.histogram(df_ap, x="quant_req", log_y=True)

quant = 10
df_ap_top = df_ap.nlargest(quant, 'quant_req').sort_values(by='quant_req', ascending=False)
top_ap = px.bar(df_ap_top, x='quant_req', y=list(map(str, df_ap_top.ap)), orientation='h', labels={ "y": "AP"})
top_ap.update_layout(title_text='Top '+ str(quant) + ' Aps em Quantidade de Requisições', title_x=0.5)

radio = list(df['radio'].unique())
radio.append('Todos os Radios')
client = list(df['client'].unique())
client.append('Todos os Client')
dia = list(df['dia'].unique())
client.append('Todos os Clients')
client_colunas = list(df_client.columns)
radio_colunas = list(df_ap.columns)

app.layout = html.Div(children=[
    html.H1(children='INF 723 - Visualização de Dados'),


    html.H2(children='Caracterização dos Dados'),
    html.H2(children='Gráficos para entendimento do comportamento dos dados do dataset'),
    html.Div(children='Esse dataset será disponibilizado para a comunidade acadêmica, '
                      'e aqui apresentamos a base de dados e sua caracterização.'),

    html.H3(children='Histograma Solicitações por hora'),
    dcc.Graph(
        id='grafico_histograma',
        figure=histograma
    ),


    html.H3(children='Histograma Solicitações por dia da semana'),
    dcc.Graph(
            id='grafico_semanal',
            figure=semanal
        ),

    html.H3(children='Histograma Clients por Caracteristica do Dataset'),
    dcc.Dropdown(
        client_colunas,
        value='quant_req',
        id='client-coluna'),
    dcc.Graph(
        id='grafico_clients',
        figure=clients
    ),


    html.H3(children='Histograma Radios por Caracteristica do Dataset'),
    dcc.Dropdown(
        radio_colunas,
        value='quant_req',
        id='radio-coluna'),
    dcc.Graph(
        id='grafico_radios',
        figure=radios
    ),


    html.H3(children='Top Pontos de Acessos em Quantidade de Requisições'),
    dcc.Slider(2, 50, 1,
               value=10,
               id='top_ap_slider'
               ),
    dcc.Graph(
        id='grafico_top_ap',
        figure=top_ap
    ),



    html.H3(children='Histograma Comparação entre dois Pontos de Acessos'),
    html.Div(children='Primeiro AP'),
    dcc.Slider(1, 108, 1,
               value=21,
               id='compare1'
               ),
    html.Div(children='Segundo AP'),
    dcc.Slider(1, 108, 1,
               value=13,
               id='compare2'
               ),
    dcc.Graph(
        id='grafico_compara',
        figure=compare
    ),
])

@app.callback(
    Output('grafico_compara', 'figure'),
    Input('compare1', 'value'),
    Input('compare2', 'value')
)
def update_output(compare1, compare2):
    ap1 = compare1
    ap2 = compare2
    x0 = df[(df['radio'] == ap1)]['hora'].values
    x1 = df[(df['radio'] == ap2)]['hora'].values
    compare = go.Figure()
    compare.add_trace(go.Histogram(name="AP " + str(ap1), x=x0))
    compare.add_trace(go.Histogram(name="AP " + str(ap2), x=x1))
    compare.update_layout(barmode='overlay')
    compare.update_traces(opacity=0.75)
    compare.update_layout(
        bargap=0.2,
        xaxis=dict(tickmode='linear'))
    return compare

@app.callback(
    Output('grafico_clients', 'figure'),
    Input('client-coluna', 'value')
)
def update_output(value):
    if value == "quant_req":
        clients = px.histogram(df_client, x="quant_req", log_y=True)
    else:
        clients = px.histogram(df_client, x=value, log_y=True)
    return clients

@app.callback(
    Output('grafico_radios', 'figure'),
    Input('radio-coluna', 'value')
)
def update_output(value):
    if value == "quant_req":
        radios = px.histogram(df_ap, x="quant_req", log_y=True)
    else:
        radios = px.histogram(df_ap, x=value, log_y=True)
    return radios

@app.callback(
    Output('grafico_top_ap', 'figure'),
    Input('top_ap_slider', 'value'))
def update_output(value):
    if value == 10:
        quant = value
        df_ap_top = df_ap.nlargest(quant, 'quant_req').sort_values(by='quant_req', ascending=False)
        top_ap = px.bar(df_ap_top, x='quant_req', y=list(map(str, df_ap_top.ap)), orientation='h', labels={"y": "AP"})
        top_ap.update_layout(title_text='Top ' + str(quant) + ' Aps em Quantidade de Requisições', title_x=0.5)
    else:
        quant = value
        df_ap_top = df_ap.nlargest(quant, 'quant_req').sort_values(by='quant_req', ascending=False)
        top_ap = px.bar(df_ap_top, x='quant_req', y=list(map(str, df_ap_top.ap)), orientation='h', labels={"y": "AP"})
        top_ap.update_layout(title_text='Top ' + str(quant) + ' Aps em Quantidade de Requisições', title_x=0.5)
    return top_ap

if __name__ == '__main__':
    app.run_server(debug=True)