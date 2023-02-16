import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

terr2 = pd.read_csv('database.csv')
region = terr2['DEPARTAMENTO'].unique()

location1 = terr2[['MUNICIPIO', 'latitude', 'longitude']]
list_locations = location1.set_index('MUNICIPIO')[['latitude', 'longitude']]
zoom_min, zoom_max, zoom0 = 1, 18, 6 

app = dash.Dash(__name__, )
app.layout = html.Div([
html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('logo01.png'),
                     id='mmaya-image',
                     style={
                         "height": "150px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )
        ],
            className="one-third column",
        ),
        html.Div([
             html.Img(src=app.get_asset_url('madre-tierra.png'),
                     id='madre-tierra-image',
                     style={
                         "height": "150px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )
        ], className="one-half column", id="title"),

        html.Div([
          html.Img(src=app.get_asset_url('giz.png'),
                     id='giz-image',
                     style={
                         "height": "100px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),
    html.Div([
        html.Div([
            html.Div([
                html.H3('MÓDULO DEL INDICE DE CARACTERIZACIÓN DE SISTEMA DE VIDA - SMTCC', 
                style = {"margin-bottom": "0px", 'color': 'black'}),
            ]),
        ], className = "six column", id = "title")

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "25px"}),
  
    html.Div([
        html.Div([
            html.P('Seleccione Departamento:', className = 'fix_label', style = {'color': 'white'}),
            dcc.Dropdown(id = 'w_departamentos',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'La Paz',
                         placeholder = 'Seleccione Departamento',
                         options = [{'label': c, 'value': c}
                                    for c in region], className = 'dcc_compon'),

            html.P('Seleccione Provincia:', className = 'fix_label', style = {'color': 'white'}),
            dcc.Dropdown(id = 'w_provincias',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Ingavi',
                         placeholder = 'Seleccione Provincia',
                         options = [], className = 'dcc_compon'),

            html.P('Seleccione Municipio:', className = 'fix_label', style = {'color': 'white'}),
            dcc.Dropdown(id = 'w_municipios',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         placeholder = 'Seleccione Municipio',
                         options = [], className = 'dcc_compon'),
            html.H6('Resultados', style = {"margin-top": "0px", 'color': 'white','size': 10}),
            html.H6(id='clasificacion_txt', style = {"margin-top": "0px", 'color': 'white','size': 10}),
        ], className = "create_container three columns"),
             html.Div([
                dcc.Graph(id = 'bar_line_1',
                        config = {'displayModeBar': 'hover'}),

            ], className = "create_container five columns"),

           html.Div([
                dcc.Graph(id = 'map_1',
                        config = {'displayModeBar': 'hover'}),
            ], className = "create_container four columns"),


    ], className = "row flex-display"),



], id = "mainContainer", style = {"display": "flex", "flex-direction": "column"})


@app.callback(
    Output('w_provincias', 'options'),
    Input('w_departamentos', 'value'))
def get_provincias_options(w_provincias):
    terr3 = terr2[terr2['DEPARTAMENTO'] == w_provincias]
    return [{'label': i, 'value': i} for i in terr3['PROVINCIA'].unique()]

@app.callback(
    Output('w_municipios', 'options'),
    Input('w_provincias', 'value'))
def get_municipios_options(w_provincias):
    terr4 = terr2[terr2['PROVINCIA'] == w_provincias]
    return [{'label': i, 'value': i} for i in terr4['MUNICIPIO'].unique()]
@app.callback(
    Output('w_provincias', 'value'),
    Input('w_provincias', 'options'))
def get_provincia_value(w_provincias):
    return [k['value'] for k in w_provincias][0]
@app.callback(
    Output('w_municipios', 'value'),
    Input('w_municipios', 'options'))
def get_municipio_value(w_municipios):
    return [k['value'] for k in w_municipios][0]

@app.callback(
    Output('clasificacion_txt', component_property='children'),
    Input('w_municipios', 'value'))
def get_clasificacion_value(w_municipios):
    terr5 = terr2[terr2['MUNICIPIO'] == w_municipios]
    k =terr5['Clasificac'].values
    thestring = ""
    for i in range(0,len(k)):
        thestring += k[i]
    death = '' + terr5['porc_i.CSV'].astype(str).values + ' %'
    return ' Indice de Caracterización :  '+death+'            Clasificación : '+thestring
@app.callback(Output('bar_line_1', 'figure'),
              [Input('w_provincias', 'value')],
              [Input('w_municipios', 'value')])
def update_graph(w_provincias, w_municipios):
    terr6 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios) ]
    terr8 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)  ]
    colores = ['lightslategray',] * 18
    colores[0] = 'crimson'
    colores[1] = 'crimson'
    colores[2] = 'crimson'
    colores[3] = 'crimson'
    colores[4] = 'crimson'

    colores[5] = 'green'
    colores[6] = 'green'
    colores[7] = 'green'
    colores[8] = 'green'
    colores[9] = 'green'
    colores[10] = 'green'

    colores[11] = 'blue'
    colores[12] = 'blue'
    colores[13] = 'blue'

    colores[14] = '#F6F926'
    colores[15] = '#F6F926'
    colores[16] = '#F6F926'
    colores[17] = '#F6F926'
    return {
        'data': [
                 go.Bar(
                    x = ['Acceso a energía eléctrica'],
                    y = terr8['_Acceso.en'],

                     textposition = 'auto',
                     name = 'Acceso a energía eléctrica',
                     marker = dict(color = '#9C0C38'),
                 ),
                  go.Bar(
                    x = ['Acceso a la Vivienda'],
                    y = terr8['_Acceso.vi'],

                     textposition = 'auto',
                     name = 'Acceso a la Vivienda',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    x = ['Acceso a educación'],
                    y = terr8['_Acceso.ed'],

                     textposition = 'auto',
                     name = 'Acceso a educación',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    x = ['Acceso a servicio de salud'],
                    y = terr8['_Acceso.se'],

                     textposition = 'auto',
                     name = 'Acceso a servicio de salud',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    x = ['Acceso a servicio de agua'],
                    y = terr8['_Acceso.h2o'],

                     textposition = 'auto',
                     name = 'Acceso a servicio de agua',
                     marker = dict(color = '#9C0C38'),
                 ),
                  go.Bar(
                    x = ['Restricciones a actividades productivas'],
                    y = terr8['_Restricci'],

                     textposition = 'auto',
                     name = 'Restricciones a actividades productivas',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    x = ['Uso limitado y restringido'],
                    y = terr8['_Uso.limit'],

                     textposition = 'auto',
                     name = 'Uso limitado y restringido',
                     marker = dict(color = 'green'),
                 ),
                  go.Bar(
                    x = ['Aptitud Forestal'],
                    y = terr8['_Aptitud.f'],

                     textposition = 'auto',
                     name = 'Aptitud Forestal',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    x = ['Agrosivopastoril'],
                    y = terr8['_Agrosilvo'],

                     textposition = 'auto',
                     name = 'Agrosivopastoril',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    x = ['Agropecuario extensivo'],
                    y = terr8['_Agropec_1'],

                     textposition = 'auto',
                     name = 'Agropecuario extensivo',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    x = ['Agropecuario intensivo'],
                    y = terr8['_Agropecua'],

                     textposition = 'auto',
                     name = 'Agropecuario intensivo',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    x = ['Turismo'],
                    y = terr8['Turismo'],

                     textposition = 'auto',
                     name = 'Turismo',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = ['Psicola'],
                    y = terr8['Piscícol'],

                     textposition = 'auto',
                     name = 'Psicola',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = ['Minero'],
                    y = terr8['Minero'],

                     textposition = 'auto',
                     name = 'Minero',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = ['Aptitud de suelos'],
                    y = terr8['Aptitud.s'],

                     textposition = 'auto',
                     name = 'Aptitud de suelos',
                     marker = dict(color = 'yellow'),
                 ),
                 go.Bar(
                    x = ['Abundancia recursos hidricos'],
                    y = terr8['Abundancia'],
                    textposition = 'auto',
                     name = 'Abundancia recursos hidricos',
                     marker = dict(color = 'yellow'),
                 ),
                 go.Bar(
                    x = ['Riqueza de especies'],
                    y = terr8['Riqueza.e'],
                    textposition = 'auto',
                     name = 'Riqueza de especies',
                     marker = dict(color = 'yellow'),
                 ),
                 go.Bar(
                    x = ['captura carbono biomasa'],
                    y = terr8['Captura.c'],
                    textposition = 'auto',
                     name = 'captura carbono biomasa',
                     marker = dict(color = 'yellow'),
                 ),
            ],

        'layout': go.Layout(
            plot_bgcolor = '#010915',
            paper_bgcolor = '#010915',
            title = {
                'text': 'Municipio : ' + (w_municipios) + '  ' ,
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont = {
                'color': 'white',
                'size': 20},
            hovermode = 'x',

            xaxis = dict(title = '',
                         tick0 = 0,
                         dtick = 1,
                         color = 'white',
                         showline = True,
                         showgrid = True,
                         showticklabels = True,
                         linecolor = 'white',
                         linewidth = 2,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 8,
                             color = 'white'
                         )
                         ),

            yaxis = dict(title = '<b>Porcentaje</b>',
                         color = 'white',
                         showline = True,
                         showgrid = True,
                         showticklabels = True,
                         linecolor = 'white',
                         linewidth = 2,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white'
                         )
                         ),
            legend = {
                'orientation': 'h',
                'bgcolor': '#010915',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),
                showlegend=False
        )
    }
@app.callback(Output('map_1', 'figure'),
              [Input('w_provincias', 'value')],
              [Input('w_municipios', 'value')])
def update_graph(w_provincias, w_municipios):
    terr3 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios) ]

    if w_municipios:
        zoom = 7 
        zoom_lat = float(terr3.latitude.astype(float).mean())
        zoom_lon = float(terr3.longitude.astype(float).mean())

    return {
        'data': [go.Scattermapbox(
            lon = [f'{x:,.000000f}' for x in terr3['longitude']],
            lat = [f'{y:,.000000f}' for y in terr3['latitude']],
            mode = 'markers',
            marker = go.scattermapbox.Marker(
                 size=25,
                 color='red',
            ),

            hoverinfo = 'text',
            hovertext =
            '<b>Departamento</b>: ' + terr3['DEPARTAMENTO'].astype(str) + '<br>' +
            '<b>Provincia</b>: ' + terr3['PROVINCIA'].astype(str) + '<br>' +
            '<b>Municipio</b>: ' + terr3['MUNICIPIO'].astype(str) + '<br>' +
            '<b>Indice de Caracterización de Vida</b>: ' + terr3['porc_i.CSV'].astype(str) + ' %<br>' +
            '<b>Clasificacion</b>: ' + terr3['Clasificac'].astype(str) + '<br>'
        )],

        'layout': go.Layout(
            margin = {"r": 0, "t": 0, "l": 0, "b": 0},
            hovermode='closest',
            mapbox = dict(
                accesstoken = 'pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',  # Use mapbox token here
                center = go.layout.mapbox.Center(lat = zoom_lat, lon = zoom_lon),
                style='open-street-map',
                zoom = zoom
            ),
            autosize = True,
        )
    }


if __name__ == '__main__':
    app.run_server(debug = True)
