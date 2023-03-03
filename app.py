import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import plotly.graph_objects as go
import pandas as pd
import dash_leaflet as dl

terr2 = pd.read_csv('database123.csv')
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
        ], className=" one-half column"),

        html.Div([
            html.Img(src=app.get_asset_url('giz.png'),
                     style={
                         "height": "70px",
                         "width": "auto",
                     },)

        ], className=" one-half column"),

    ], className="row flex-display",),
    html.Div([
        html.Div([
            html.Div([
                html.H3('MÓDULO DEL INDICE DE CARACTERIZACIÓN DE SISTEMA DE VIDA - SMTCC', 
                style = { 'color': 'black'}),
            ]),
        ], className = "six column")

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
        ], className="create_container one-half column"),

        html.Div([
         html.P('Seleccione Municipio:', className = 'fix_label', style = {'color': 'white'}),
            dcc.Dropdown(id = 'w_municipios',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         placeholder = 'Seleccione Municipio',
                         options = [], className = 'dcc_compon'),

        ], className="create_container one-half column"),

    ], className="row flex-display",),
    html.Div([
        html.Div([
                html.H6('Resultados', style = { 'color': 'white','size': 10}),
                html.H6(id='indice_txt', style = {'color': 'white','size': 10}),
                html.H6(id='clasificacion_txt', style = {'color': 'white','size': 10}),
                html.Button('Reporte', id='button'),
                html.A("Visor de Mapa", href='https://datos.siarh.gob.bo/index.php?module=agrobiodiversidad&smodule=geovisor', target="_blank"),
               # html.Br(),
               # html.Button('Visor de Mapas', id='button2'),
            ], className = "create_container  columns"),
    ], className = "row flex-display", ),

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
                                [dl.Overlay(dl.LayerGroup(id="layer"), name="Municipios", checked=True)]
                            )
                        ],
                    id="map", style={'width': '100%', 'height': '100%', 'margin': "auto", "display": "block"}),
                ], className = "create_container five columns"),
    ], className = "row flex-display"),
    html.H6(id='txt_01', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_02', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_03', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_04', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_05', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_06', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_07', style = {'color': 'white','size': 10}, hidden = True),
    html.Div(id='graph_img', hidden = True),
    html.Div(id='graph_img_map', hidden = True)
])

app.clientside_callback(
    '''
    function (chart_children) {
        if (chart_children.type == "Img") {
            // console.log(chart_children);
            // let pdfWindow = window.open("https://datos.siarh.gob.bo/index.php?module=agrobiodiversidad&smodule=geovisor",'' , 'location=no, menubar=no, status=no, resizable=no, toolbar=no ,width=1060,height=720');
            //var canvas = $('map').get(0); 
            
            var logo_mmaya = new Image();
            var logo_madre = new Image();
            var logo_giz = new Image();
                    logo_mmaya.src= 'assets/logo01.png';
                    logo_madre.src= 'assets/Madre-Tierra2.png';
                    logo_giz.src= 'assets/Footer.png';
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
            pdf.setFontSize(10);
            pdf.text('REPORTE: INDICE DE CARACTERIZACIÓN DE SISTEMA DE VIDA - SMTCC', 35, 47);
            pdf.setFontType("italic");
            pdf.text('El Municipio de '+$('#w_municipios').text()+' . ,Tiene un '+$('#indice_txt').text()+' ', 15, 52);
            pdf.text('En cuanto a las Funciones Ambientales,'+$('#txt_01').text()+' ,', 15, 56);
            pdf.text('del espacio geografico posee  '+$('#txt_02').text()+'  para  actividades  agricolas,', 15, 60);

            pdf.text('Dentro  de los Sistemas  productivos  sustentables,  el  sector  Turismo,', 15, 68);
            pdf.text('tiene  un  '+$('#txt_03').text()+'  de participacion  municipal ,las actividades Piscicolas,', 15, 72);
            pdf.text('entre crianza  y  pesca tienen un  Referente  a  los Grados de  Pobreza,', 15, 76);
            pdf.text('de los servicios basicos el '+$('#txt_04').text()+' de la poblacion tiene Acceso a energia ,', 15, 80);
            pdf.text('electrica,  seguido  del '+$('#txt_05').text()+'  tiene  Acceso   a   vivienda.', 15, 84);

            pdf.text('El municipio de "'+$('#w_municipios').text()+'",', 15, 92);
            pdf.text('de acuerdo a la valoracion de la caracterización de los ,', 15, 96);
            pdf.text('Sistemas de Vida presenta las', 15, 100);
            pdf.text('siguientes vocaciones productivas:', 15, 104);

            let date = new Date()
            let day = date.getDate()
            let month = date.getMonth() + 1
            let year = date.getFullYear()
                
            pdf.addImage(logo_mmaya.src, 'PNG', 15, 15, 50, 18.3);
            pdf.addImage(logo_madre.src, 'PNG', 75, 15, 50, 18.3);
            pdf.addImage(logo_giz.src, 'PNG', 135, 15, 60, 18.3);
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
@app.callback(
    Output('txt_01', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Captura.ca'].astype(str).values + ' %'
@app.callback(
    Output('txt_02', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Ap.suelo'].astype(str).values + ' %'
@app.callback(
    Output('txt_03', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Turismo'].astype(str).values + ' %'
@app.callback(
    Output('txt_04', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Acc.EE'].astype(str).values + ' %'
@app.callback(
    Output('txt_05', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Acc.vivien'].astype(str).values + ' %'

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
                    x = terr8['Acc.EE'],orientation='h',

                    text=terr8['Acc.EE'],
                    textposition="auto",
                     name = 'Acceso a energía eléctrica',
                     marker = dict(color = '#9C0C38'),
                 ),
                  go.Bar(
                    y = ['Acceso a la Vivienda'],
                    x = terr8['Acc.vivien'],orientation='h',

                    text=terr8['Acc.vivien'],
                    textposition="auto",
                     name = 'Acceso a la Vivienda',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    y = ['Acceso a educación'],
                    x = terr8['Acc.edu'],orientation='h',

                    text=terr8['Acc.edu'],
                    textposition="auto",
                     name = 'Acceso a educación',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    y = ['Acceso a servicio de salud'],
                    x = terr8['Acc.salud'],orientation='h',

                    text=terr8['Acc.salud'],
                    textposition="auto",
                     name = 'Acceso a servicio de salud',
                     marker = dict(color = '#9C0C38'),
                 ),
                 go.Bar(
                    y = ['Acceso a servicio de agua'],
                    x = terr8['Acc.agua'],orientation='h',

                    text=terr8['Acc.agua'],
                    textposition="auto",
                     name = 'Acceso a servicio de agua',
                     marker = dict(color = '#9C0C38'),
                 ),
                  go.Bar(
                    y = ['Restricciones a actividades productivas'],
                    x = terr8['R.actv.prd'],orientation='h',

                    text=terr8['R.actv.prd'],
                    textposition="auto",
                     name = 'Restricciones a actividades productivas',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Uso limitado y restringido'],
                    x = terr8['Uso.limit'],orientation='h',

                    text=terr8['Uso.limit'],
                    textposition="auto",
                     name = 'Uso limitado y restringido',
                     marker = dict(color = 'green'),
                 ),
                  go.Bar(
                    y = ['Aptitud Forestal'],
                    x = terr8['Ap.fores'],orientation='h',

                    text=terr8['Ap.fores'],
                    textposition="auto",
                     name = 'Aptitud Forestal',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Agrosivopastoril'],
                    x = terr8['Agrosilvo'],orientation='h',

                    text=terr8['Agrosilvo'],
                    textposition="auto",
                     name = 'Agrosivopastoril',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Agropecuario extensivo'],
                    x = terr8['Agro.exten'],orientation='h',

                    text=terr8['Agro.exten'],
                    textposition="auto",
                     name = 'Agropecuario extensivo',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Agropecuario intensivo'],
                    x = terr8['Agro.inten'],orientation='h',

                    text=terr8['Agro.inten'],
                    textposition="auto",
                     name = 'Agropecuario intensivo',
                     marker = dict(color = 'green'),
                 ),
                 go.Bar(
                    y = ['Turismo'],
                    x = terr8['Turismo'],
                    orientation='h',
                    text=terr8['Turismo'],
                    textposition="auto",
                     name = 'Turismo',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = terr8['Piscicol'],
                    y = ['Psicola'],
                    orientation='h',
                    text=terr8['Piscicol'],
                    textposition="auto",
                     name = 'Psicola',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = terr8['Minero'],
                    y = ['Minero'],
                    orientation='h',
                    text=terr8['Minero'],
                    textposition="auto",
                     name = 'Minero',
                     marker = dict(color = 'blue'),
                 ),
                 go.Bar(
                    x = terr8['Ap.suelo'],
                    y = ['Aptitud de suelos'],
                    orientation='h',
                    text=terr8['Ap.suelo'],
                    textposition="auto",
                     name = 'Aptitud de suelos',
                     marker = dict(color = 'yellow'),
                 ),
                 go.Bar(
                    x = terr8['Abu.rrhh'],
                    y = ['Abundancia recursos hidricos'],
                    text=terr8['Abu.rrhh'],
                    textposition="auto",
                     name = 'Abundancia recursos hidricos',
                     marker = dict(color = 'yellow'),
                     orientation='h',
                 ),
                 go.Bar(
                    x = terr8['Riqueza.es'],
                    y = ['Riqueza de especies'],
                    text=terr8['Riqueza.es'],
                    textposition="auto",
                     name = 'Riqueza de especies',
                     marker = dict(color = 'yellow'),
                     orientation='h',
                 ),
                 go.Bar(
                    x = terr8['Captura.ca'] ,
                    y = ['captura carbono biomasa'],
                    text=terr8['Captura.ca'],
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