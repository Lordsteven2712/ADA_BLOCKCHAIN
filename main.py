import requests
import json
from dash import Dash, html, dcc, Output, Input, State

"""
Proyecto Final – Interacción con una Blockchain

Grupo 1SF125

Integrantes:
- Steven Guerra         8-964-1219
- Juan Cortés           2-749-1568
- Abilio Ortega         8-999-1670
- Gabriel Cedeño        8-1001-1537
- José Palacio          E-8-189409

"""


# A - Función para verificar el acceso a la red
def verificar_acceso():
    username = 'jsgalan'
    token = '89600f38d62242540816d5dd1a7a043597e23187'

    response = requests.get(
        'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(
            username=username
        ),
        headers={'Authorization': 'Token {token}'.format(token=token)}
    )
    if response.status_code == 200:
        return f'CPU quota info: {response.content}'
    else:
        return 'Got unexpected status code {}: {!r}'.format(response.status_code, response.content)


# B - Función para verificar el estado de la cadena blockchain
def obtener_cadena():
    response = requests.get('http://jsgalan.pythonanywhere.com/chain')
    formatted_response = json.dumps(response.json(), indent=4)
    return formatted_response


# C - Función para crear mensaje
def crear_mensaje(sender, recipient, chat):
    data = {
        "sender": sender,
        "recipient": recipient,
        "chat": chat
    }
    response = requests.post('http://jsgalan.pythonanywhere.com/transactions/new', json=data)
    formatted_response = json.dumps(response.json(), indent=4)
    return formatted_response


# D - Función para sellar
def sellar_bloque(groupname, name):
    data = {
        "groupname": groupname,
        "name": name
    }
    response = requests.post('http://jsgalan.pythonanywhere.com/mine', json=data)
    formatted_response = json.dumps(response.json(), indent=4)
    return formatted_response


app = Dash(__name__)

# Diseño del Dash
app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='/assets/styles.css'
    ),
    html.H1(children='Interacción con la blockchain ADA_BLOCK', className='titulo-principal'),
    html.Div([
        html.H2(children='Verificar acceso'),
        html.Button(id='acceso-button', n_clicks=0, children='Verificar')
    ], className='acceso contenedor'),
    html.Div([
        html.H2(children='Crear un mensaje'),
        html.Label('Nombre del remitente:'),
        dcc.Input(id='sender-input', type='text', value=''),
        html.Label('Destinatario:'),
        dcc.Input(id='recipient-input', type='text', value=''),
        html.Label('Chat:'),
        dcc.Textarea(id='chat-input', value=''),
        html.Button(id='submit-button-state', n_clicks=0, children='Enviar')
    ], className='mensaje contenedor'),
    html.Div([
        html.H2(children='Obtener cadena'),
        html.Button(id='cadena-button', n_clicks=0, children='Obtener')
    ], className='cadena contenedor'),
    html.Div([
        html.H2(children='Sellar bloque'),
        html.Button(id='sellar-button', n_clicks=0, children='Sellar')
    ], className='sellar contenedor'),
    html.Pre(id='output-div', children='Salida:'),
], className='main')


@app.callback(
    Output(component_id='output-div', component_property='children', allow_duplicate=True),
    Input(component_id='submit-button-state', component_property='n_clicks'),
    State(component_id='sender-input', component_property='value'),
    State(component_id='recipient-input', component_property='value'),
    State(component_id='chat-input', component_property='value'),
    prevent_initial_call=True
)
def crear_mensaje_callback(n_clicks, sender, recipient, chat):
    if n_clicks != 0:
        response = crear_mensaje(sender, recipient, chat)
        return f'Mensaje enviado por {sender} a {recipient}: {response}'

    return ''


@app.callback(
    Output(component_id='output-div', component_property='children', allow_duplicate=True),
    Input(component_id='acceso-button', component_property='n_clicks'),
    prevent_initial_call=True
)
def verificar_acceso_callback(n_clicks):
    if n_clicks != 0:
        response = verificar_acceso()
        return response

    return ''


@app.callback(
    Output(component_id='output-div', component_property='children', allow_duplicate=True),
    Input(component_id='cadena-button', component_property='n_clicks'),
    prevent_initial_call=True
)
def obtener_cadena_callback(n_clicks):
    if n_clicks != 0:
        response = obtener_cadena()
        return response

    return ''


@app.callback(
    Output(component_id='output-div', component_property='children', allow_duplicate=True),
    Input(component_id='sellar-button', component_property='n_clicks'),
    prevent_initial_call=True
)
def obtener_cadena_callback(n_clicks):
    if n_clicks != 0:
        response = sellar_bloque('1SF125', 'Steven Guerra')
        return response

    return ''


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
