import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import plotly.graph_objects as go
# import plotly.graph_objs as go
import pandas as pd
import dash_leaflet as dl

terr2 = pd.read_csv('database.csv')
region = terr2['DEPARTAMENTO'].unique()

location1 = terr2[['MUNICIPIO', 'latitude', 'longitude']]
list_locations = location1.set_index('MUNICIPIO')[['latitude', 'longitude']]


external_stylesheets = [
    {'src': 'https://codepen.io/chriddyp/pen/bWLwgP.css'},
    {'src':'assets/s1.css'},
    {'src':'assets/style.css'},
]
# external JavaScript files
external_scripts = [
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {'src': 'https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js'},
    {'src':'assets/jQuery.printarea/canvas2image.js'},
    {'src':'assets/jsPDF-master/dist/jspdf.min.js'},
    {'src':'assets/FileSaver.js-master/dist/FileSaver.min.js'}
]

app = dash.Dash(__name__, external_scripts=external_scripts, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div(children=[
    html.Div([
        html.Div([
             html.Img(src=app.get_asset_url('logo01.png'),
                     style={
                         "height": "70px",
                         "width": "auto",
                     },)
        ], className=" one-half column",),
        html.Div([
             html.Img(src=app.get_asset_url('Madre-Tierra2.png'),
                     style={
                         "height": "80px",
                         "width": "auto",
                     },)
        ], className=" one-half column", id="title3"),

        html.Div([
            html.Img(src=app.get_asset_url('giz.png'),
                     style={
                         "height": "70px",
                         "width": "auto",
                     },)

        ], className=" one-half column", id='title1'),

    ], className="row flex-display",),
    html.Div([
        html.Div([
            html.Div([
                html.H3('MÓDULO DEL INDICE DE CARACTERIZACIÓN DE SISTEMA DE VIDA - SMTCC', 
                style = { 'color': 'black'}),
            ]),
        ], className = "six column", id = "title4")

    ], id = "header", className = "row flex-display"),
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
        ], className="create_container one-half column",),
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

    ], className="row flex-display",),
    html.Div([
        html.Div([
                html.H6('Resultados', style = { 'color': 'white','size': 10}),
                html.H6(id='indice_txt', style = {'color': 'white','size': 10}),
                html.H6(id='clasificacion_txt', style = {'color': 'white','size': 10}),
                html.Button('imprimir Pdf', id='button'),
            ], className = "create_container  columns"),
    ], id = "header3", className = "row flex-display", ),

    html.Div([        
        html.Div([
            dcc.Graph(
                id='bar_line_1',
                config = {'displayModeBar': False}
            ),
        ], className = "create_container seven columns"),
        html.Div([              
                    dl.Map([
                            dl.LayersControl(
                                [dl.BaseLayer(dl.TileLayer(id="base-layer-id"),) ] +
                                [dl.Overlay(dl.LayerGroup(id="layer"), name="markers", checked=True)]
                            )
                        ],
                    id="map", style={'width': '100%', 'height': '100%', 'margin': "auto", "display": "block"}),
                ], className = "create_container five columns"),
    ], className = "row flex-display"),
    html.Div(id='graph_img', hidden = True),
    html.Div(id='graph_img_map', hidden = True)
])

app.clientside_callback(
    '''
    function (chart_children) {
        if (chart_children.type == "Img") {
            // console.log(chart_children);
            var canvas = $('map').get(0); 
            
            var logo_mmaya = new Image();
                    logo_mmaya.src= 'assets/logo_mmaya2018.png';
                    var mm_in_px = 3.77952755905511;
                    var imgAncho = Math.round(10/mm_in_px);
                    var imgAlto = Math.round(15/mm_in_px);
                    var pageAncho = 279.4;
                    var pageAlto = 215.9;
                    var imgAnchoAux = 0;
                    var imgAltoAux = 0;
                    var puntoX = 0;

                    if (imgAncho > 249) {
                        imgAltoAux = imgAlto - 145.81;
                        imgAlto = imgAlto - imgAltoAux;
                        imgAnchoAux = imgAncho - imgAltoAux - (1.29 * imgAltoAux);
                    } else {
                        imgAltoAux = 145.81 - imgAlto;
                        imgAlto = imgAlto + imgAltoAux;
                        imgAnchoAux = imgAncho + imgAltoAux + (1.29 * imgAltoAux);
                    }
            puntoX = 14 + (pageAncho - imgAncho - 30)/2;
            var pdf = new jsPDF({
                            orientation: 'p',
                            unit: 'mm',
                            format: 'letter'
                        });
            var dataImg = null;
           
            pdf.setFontSize(12);
            pdf.setFontType("bold");
            pdf.text('Ministerio de Medio Ambiente y Agua', 100, 20);
            pdf.setFontSize(10);
            pdf.text('Autoridad Purinacional de la Madre Tierra', 102, 25);
            pdf.text('INDICE DE CARACTERIZACIÓN DE SISTEMA DE VIDA - SMTCC', 81, 30);
            pdf.text('REPORTE: ', 15, 47);
            pdf.setFontType("italic");
            pdf.text('El Municipio de '+$('#w_municipios').text()+' . ,Tiene un '+$('#indice_txt').text()+' ', 15, 52);
            pdf.text('Tiene una '+$('#clasificacion_txt').text()+' de relacion entre las caracteristicas del sistema de vida', 15, 56);

            pdf.text('El municipio de "'+$('#w_municipios').text()+'", de acuerdo a la valoracion de la caracterizacion de los Sistemas de Vida,', 15, 64);
            pdf.text(' presenta las siguientes vocaciones productivas: ', 15, 68);
           
            let date = new Date()

                let day = date.getDate()
                let month = date.getMonth() + 1
                let year = date.getFullYear()
                
            pdf.addImage(logo_mmaya.src, 'PNG', 15, 15, 60, 18.3);
            pdf.addImage(chart_children.props.src, 'PNG', 20, 70, 150, 80);
            pdf.save(`reporte-sistema-vida-${year}-${month}-${day}.pdf`);
            
        }
        return 0;
    }
    ''',
    Output('graph_img', 'n_clicks'),
    [
        Input('graph_img', 'children'),
    ]
)


@app.callback(
    Output('graph_img', 'children'),
    [
        Input('button', 'n_clicks')
    ],
    [
        State('bar_line_1', 'figure')
    ]
)
def figure_to_image(n_clicks, figure_dict):
    if n_clicks:
        # Higher scale = better resolution but also takes longer/larger size
        figure = go.Figure(figure_dict)
        img_uri = figure.to_image(format="png", scale=3)
        src = "data:image/png;base64," + base64.b64encode(img_uri).decode('utf8')
        return html.Img(src=src)
    return ''
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
    Output('indice_txt', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    death = '' + terr5['porc_i.CSV'].astype(str).values + ' %'
    return ' Indice de Caracterización :  '+death
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
    return 'Clasificación : '+thestring
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

                    text=round(terr8['_Acceso.en']*100,0),
                    textposition="auto",
                     name = 'Acceso a energía eléctrica',
                     marker = dict(color = '#9C0C38'),
                 ),
                  go.Bar(
                    y = ['Acceso a la Vivienda'],
                    x = round(terr8['_Acceso.vi']*100,0),orientation='h',

                    text=round(terr8['_Acceso.vi']*100,0),
                    textposition="auto",
                     name = 'Acceso a la Vivienda',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    y = ['Acceso a educación'],
                    x = round(terr8['_Acceso.ed']*100,0),orientation='h',

                    text=round(terr8['_Acceso.ed']*100,0),
                    textposition="auto",
                     name = 'Acceso a educación',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    y = ['Acceso a servicio de salud'],
                    x = round(terr8['_Acceso.se']*100,0),orientation='h',

                    text=round(terr8['_Acceso.se']*100,0),
                    textposition="auto",
                     name = 'Acceso a servicio de salud',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    y = ['Acceso a servicio de agua'],
                    x = round(terr8['_Acceso.h2o']*100,0),orientation='h',

                    text=round(terr8['_Acceso.h2o']*100,0),
                    textposition="auto",
                     name = 'Acceso a servicio de agua',
                     marker = dict(color = '#9C0C38'),
                 ),
                  go.Bar(
                    y = ['Restricciones a actividades productivas'],
                    x = round(terr8['_Restricci']*100,0),orientation='h',

                    text=round(terr8['_Restricci']*100,0),
                    textposition="auto",
                     name = 'Restricciones a actividades productivas',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Uso limitado y restringido'],
                    x = round(terr8['_Uso.limit']*100,0),orientation='h',

                    text=round(terr8['_Uso.limit']*100,0),
                    textposition="auto",
                     name = 'Uso limitado y restringido',
                     marker = dict(color = 'green'),
                 ),
                  go.Bar(
                    y = ['Aptitud Forestal'],
                    x = round(terr8['_Aptitud.f']*100,0),orientation='h',

                    text=round(terr8['_Aptitud.f']*100,0),
                    textposition="auto",
                     name = 'Aptitud Forestal',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Agrosivopastoril'],
                    x = round(terr8['_Agrosilvo']*100,0),orientation='h',

                    text=round(terr8['_Agrosilvo']*100,0),
                    textposition="auto",
                     name = 'Agrosivopastoril',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Agropecuario extensivo'],
                    x = round(terr8['_Agropec_1']*100,0),orientation='h',

                    text=round(terr8['_Agropec_1']*100,0),
                    textposition="auto",
                     name = 'Agropecuario extensivo',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Agropecuario intensivo'],
                    x = round(terr8['_Agropecua']*100,0),orientation='h',

                    text=round(terr8['_Agropecua']*100,0),
                    textposition="auto",
                     name = 'Agropecuario intensivo',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Turismo'],
                    x = round(terr8['Turismo']*100,0),
                    orientation='h',
                    text=round(terr8['Turismo']*100,0),
                    textposition="auto",
                     name = 'Turismo',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = round(terr8['Piscícol']*100,0),
                    y = ['Psicola'],
                    orientation='h',
                    text=round(terr8['Piscícol']*100,0),
                    textposition="auto",
                     name = 'Psicola',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = round(terr8['Minero']*100,0),
                    y = ['Minero'],
                    orientation='h',
                    text=round(terr8['Minero']*100,0),
                    textposition="auto",
                     name = 'Minero',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = round(terr8['Aptitud.s']*100,0),
                    y = ['Aptitud de suelos'],
                    orientation='h',
                    text=round(terr8['Aptitud.s']*100,0),
                    textposition="auto",
                     name = 'Aptitud de suelos',
                     marker = dict(color = 'yellow'),
                 ),
                 go.Bar(
                    x = round(terr8['Abundancia']*100,0),
                    y = ['Abundancia recursos hidricos'],
                    text=round(terr8['Abundancia']*100,0),
                    textposition="auto",
                     name = 'Abundancia recursos hidricos',
                     marker = dict(color = 'yellow'),
                     orientation='h',
                 ),
                 go.Bar(
                    x = round(terr8['Riqueza.e']*100,0),
                    y = ['Riqueza de especies'],
                    text=round(terr8['Riqueza.e']*100,0),
                    textposition="auto",
                     name = 'Riqueza de especies',
                     marker = dict(color = 'yellow'),
                     orientation='h',
                 ),
                 go.Bar(
                    x = round(terr8['Captura.c']*100,0) ,
                    y = ['captura carbono biomasa'],
                    text=round(terr8['Captura.c']*100,0),
                     name = 'captura carbono biomasa',
                     marker = dict(color = 'yellow'),
                     orientation='h',
                 ),
            ],

        'layout': go.Layout(
            margin=dict(l=250, r=120, t=50, b=50),
            margin_pad=10,
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

            yaxis = dict(title = '',
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
                'xanchor': 'center', 'x': 0.5, 'y': 0.3},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),
                showlegend=False
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
            dl.TileLayer(id="base-layer-id"),
            dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                              activeColor="#214097", completedColor="#972158"),
            # Marker with tool tip and popup
            # for i in range page_size:
            # create marker at i position long,lang
            dl.Marker(position=[zoom_lat, zoom_lon], children=[
                dl.Popup([
                    html.H3('Indice de Caracterización de Vida: ' + terr3['porc_i.CSV'].astype(str) + ' %' ),
                    html.P('Municipio: ' + terr3['MUNICIPIO'].astype(str) + '')
                ])
            ])
        ])
    ]


if __name__ == '__main__':
    app.run_server(debug=True)