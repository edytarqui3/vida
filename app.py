import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function

terr2 = pd.read_csv('database.csv')
region = terr2['DEPARTAMENTO'].unique()

location1 = terr2[['MUNICIPIO', 'latitude', 'longitude']]
list_locations = location1.set_index('MUNICIPIO')[['latitude', 'longitude']]

zoom_min, zoom_max, zoom0 = 1, 18, 6  # min/max zoom levels might depend on the tiles used

app = dash.Dash(__name__, )
app.layout = html.Div([
html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('logo01.png'),
                     id='mmaya-image',
                     style={
                         "height": "70px",
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
                         "height": "70px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )
        ], className="one-half column", id="title9"),

        html.Div([
          html.Img(src=app.get_asset_url('giz.png'),
                     id='giz-image',
                     style={
                         "height": "70px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )

        ], className="one-half column", id='title10'),

    ], id="header2", className="row flex-display", style={"margin-bottom": "25px"}),
    html.Div([
        html.Div([
            html.Div([
                html.H3('MÓDULO DEL INDICE DE CARACTERIZACIÓN DE SISTEMA DE VIDA - SMTCC', 
                style = {"margin-bottom": "0px", 'color': 'black'}),
            ]),
        ], className = "six column", id = "title4")

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
        ],
            className="create_container one-half column",
        ),
        html.Div([
             html.P('Seleccione Provincia:', className = 'fix_label', style = {'color': 'white'}),
            dcc.Dropdown(id = 'w_provincias',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Ingavi',
                         placeholder = 'Seleccione Provincia',
                         options = [], className = 'dcc_compon'),
        ], className="create_container one-half column", id="title3"),

        html.Div([
         html.P('Seleccione Municipio:', className = 'fix_label', style = {'color': 'white'}),
            dcc.Dropdown(id = 'w_municipios',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         placeholder = 'Seleccione Municipio',
                         options = [], className = 'dcc_compon'),

        ], className="create_container one-half column", id='title1'),

    ], id="header5", className="row flex-display", style={"margin-bottom": "25px"}),
    html.Div([
        html.Div([
                html.H6('Resultados', style = {"margin-top": "0px", 'color': 'white','size': 10}),
                html.H6(id='clasificacion_txt', style = {"margin-top": "0px", 'color': 'white','size': 10}),
                html.Button('imprimir Pdf', id='run'),
            ], className = "create_container  columns"),

        ], id = "header3", className = "row flex-display", style = {"margin-bottom": "25px"}),
        html.Div([
            
                html.Div([
                    dcc.Graph(id = 'bar_line_1',
                            config = {'displayModeBar': 'hover'}),

                ], className = "create_container five columns"),

            html.Div([
                    dcc.Graph(id = 'map_1',
                            config = {'displayModeBar': 'hover'}),
                ], className = "create_container three columns"),
            html.Div([              
                    dl.Map([
                        dl.TileLayer(id="base-layer-id"), 
                        dl.LayerGroup(id="layer")
                        ],
                    id="map", style={'width': '100%', 'height': '100%', 'margin': "auto", "display": "block"}),
                ], className = "create_container five columns"),

        ], className = "row flex-display"),
        html.Div([
            


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
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
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
    return {
        'data': [
                 go.Bar(
                    y = ['Acceso a energía eléctrica'],
                    x = round(terr8['_Acceso.en']*100,0),orientation='h',

                     textposition = 'auto',
                     name = 'Acceso a energía eléctrica',
                     marker = dict(color = '#9C0C38'),
                 ),
                  go.Bar(
                    y = ['Acceso a la Vivienda'],
                    x = round(terr8['_Acceso.vi']*100,0),orientation='h',

                     textposition = 'auto',
                     name = 'Acceso a la Vivienda',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    y = ['Acceso a educación'],
                    x = round(terr8['_Acceso.ed']*100,0),orientation='h',

                     textposition = 'auto',
                     name = 'Acceso a educación',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    y = ['Acceso a servicio de salud'],
                    x = round(terr8['_Acceso.se']*100,0),orientation='h',

                     textposition = 'auto',
                     name = 'Acceso a servicio de salud',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    y = ['Acceso a servicio de agua'],
                    x = round(terr8['_Acceso.h2o']*100,0),orientation='h',

                     textposition = 'auto',
                     name = 'Acceso a servicio de agua',
                     marker = dict(color = '#9C0C38'),
                 ),
                  go.Bar(
                    y = ['Restricciones a actividades productivas'],
                    x = round(terr8['_Restricci']*100,0),orientation='h',

                     textposition = 'auto',
                     name = 'Restricciones a actividades productivas',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Uso limitado y restringido'],
                    x = round(terr8['_Uso.limit']*100,0),orientation='h',

                     textposition = 'auto',
                     name = 'Uso limitado y restringido',
                     marker = dict(color = 'green'),
                 ),
                  go.Bar(
                    y = ['Aptitud Forestal'],
                    x = round(terr8['_Aptitud.f']*100,0),orientation='h',

                     textposition = 'auto',
                     name = 'Aptitud Forestal',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Agrosivopastoril'],
                    x = round(terr8['_Agrosilvo']*100,0),orientation='h',

                     textposition = 'auto',
                     name = 'Agrosivopastoril',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Agropecuario extensivo'],
                    x = round(terr8['_Agropec_1']*100,0),orientation='h',

                     textposition = 'auto',
                     name = 'Agropecuario extensivo',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Agropecuario intensivo'],
                    x = round(terr8['_Agropecua']*100,0),orientation='h',

                     textposition = 'auto',
                     name = 'Agropecuario intensivo',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Turismo'],
                    x = round(terr8['Turismo']*100,0),
                    orientation='h',
                     textposition = 'auto',
                     name = 'Turismo',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = round(terr8['Piscícol']*100,0),
                    y = ['Psicola'],
                    orientation='h',
                     textposition = 'auto',
                     name = 'Psicola',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = round(terr8['Minero']*100,0),
                    y = ['Minero'],
                    orientation='h',
                     textposition = 'auto',
                     name = 'Minero',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = round(terr8['Aptitud.s']*100,0),
                    y = ['Aptitud de suelos'],
                    orientation='h',
                     textposition = 'auto',
                     name = 'Aptitud de suelos',
                     marker = dict(color = 'yellow'),
                 ),
                 go.Bar(
                    x = round(terr8['Abundancia']*100,0),
                    y = ['Abundancia recursos hidricos'],
                    textposition = 'auto',
                     name = 'Abundancia recursos hidricos',
                     marker = dict(color = 'yellow'),
                     orientation='h',
                 ),
                 go.Bar(
                    x = round(terr8['Riqueza.e']*100,0),
                    y = ['Riqueza de especies'],
                    textposition = 'auto',
                     name = 'Riqueza de especies',
                     marker = dict(color = 'yellow'),
                     orientation='h',
                 ),
                 go.Bar(
                    x = round(terr8['Captura.c']*100,0) ,
                    y = ['captura carbono biomasa'],
                    textposition = 'auto',
                     name = 'captura carbono biomasa',
                     marker = dict(color = 'yellow'),
                     orientation='h',
                 ),
                # go.Bar(
                #     x=[20, 14, 23],
                #     y=['giraffes', 'orangutans', 'monkeys'],
                #     orientation='h'
                # ),
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
            hovermode = 'y',

            legend = {
                'orientation': 'h',
                'bgcolor': '#010915',
                'xanchor': 'center', 'x': 0.5, 'y': 0.3},
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
                 style="white-bg",
                layers=[
                    {
                        "below": 'traces',
                        "sourcetype": "raster",
                        "sourceattribution": "United States Geological Survey",
                        "source": [
                            "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                        ]
                    }
                ],
                zoom = zoom
            ),
            autosize = True,
        )
    }
@app.callback(Output('map', 'children'),
              [Input('w_provincias', 'value')],
              [Input('w_municipios', 'value')])
def update_mapa(w_provincias, w_municipios):
    terr3 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios) ]
    if w_municipios:
        zoom = 7 
        zoom_lat = float(terr3.latitude.astype(float).mean())
        zoom_lon = float(terr3.longitude.astype(float).mean())

    return [
        dl.Map(style={'width': '100%', 'height': '100%'}, 
            center=[zoom_lat, zoom_lon], zoom=10, children=[
           dl.LayersControl(
                [
                    dl.BaseLayer(
                    dl.TileLayer(id="base-layer-id"),
                    dl.WMSTileLayer(url="http://siip.produccion.gob.bo:8080/geoserver/comAgrico/wms?service=WMS",
                                    layers="comAgrico:Riqueza_Especies_Biodiversidad", 
                                    format="image/png", transparent=True),)] +
                [
                    dl.Overlay(dl.LayerGroup(dl.Marker(position=[zoom_lat, zoom_lon], children=[
                    dl.Popup([
                            html.H3('Indice de Caracterización de Vida: ' + terr3['porc_i.CSV'].astype(str) + ' %' ),
                            html.P('Municipio: ' + terr3['MUNICIPIO'].astype(str) + '')
                        ])
                    ])), name="markers", checked=True)]
            )
        ])
    ]

if __name__ == '__main__':
    app.run_server(debug = True)
