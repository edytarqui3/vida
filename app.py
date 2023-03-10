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
                html.Br(),
                html.A("Mapa", href='https://mapa-wms.onrender.com', target="_blank"),
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
                    dcc.Graph(id = 'map_1',
                        config = {'displayModeBar': 'hover'}),
                ], className = "create_container five columns"),
    ], className = "row flex-display"),
    html.H6(id='txt_municipio', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_01_ap_suelo', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_02_abu_rrhh', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_03_riq_espe', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_04_cap_carb', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_05_turismo', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_06_psicola', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_07_minero', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_08_agro_int', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_09_agro_ext', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_10_agrosilv', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_11_ap_fores', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_12_uso_limi', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_13_acc_ee', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_14_acc_vivienda', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_15_acc_educa', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_16_acc_salud', style = {'color': 'white','size': 10}, hidden = True),
    html.H6(id='txt_17_acc_agua', style = {'color': 'white','size': 10}, hidden = True),
    html.Div(id='graph_img', hidden = True),
    html.Div(id='graph_img_map', hidden = True)
])

app.clientside_callback(
    '''
    function (chart_children) {
        if (chart_children.type == "Img") {
            console.log(chart_children);
            // let pdfWindow = window.open("https://datos.siarh.gob.bo/index.php?module=agrobiodiversidad&smodule=geovisor",'' , 'location=no, menubar=no, status=no, resizable=no, toolbar=no ,width=1060,height=720');
            // var canvas = $('map').get(0); 
            
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
           
            pdf.setFontSize(12);
            pdf.setFontType("bold");
            pdf.setFontSize(10);
            pdf.text('REPORTE: INDICE DE CARACTERIZACIÓN DE SISTEMA DE VIDA - SMTCC', 35, 47);
            pdf.setFontType("italic");
            pdf.text('El Municipio de "'+$('#txt_municipio').text()+'", posee un "'+$('#indice_txt').text()+'" ,es decir un(a)  '+$('#clasificacion_txt').text()+' de relacion ', 15, 52);
            pdf.text('entre las caracteristicas del sistema de vida,En cuanto a las Funciones Ambientales,', 15, 56);
            pdf.text(''+$('#txt_01_ap_suelo').text()+' del espacio geografico posee  ', 15, 60);
            pdf.text(''+$('#txt_02_abu_rrhh').text()+'  para  actividades  agricolas,', 15, 64);
            pdf.text('con el "'+$('#txt_02_abu_rrhh').text()+'" de (Abundancia de recursos hidricos)', 15, 68);
            pdf.text('por otro lado,la Riqueza.es(Riquezas de Especies)', 15, 72);
            pdf.text('del municipio cuenta con "'+$('#txt_03_riq_espe').text()+'" y una  (captura', 15, 76);
            pdf.text('de Biomasa) del "'+$('#txt_04_cap_carb').text()+'".', 15, 80);

            pdf.text('Dentro  de los Sistemas  productivos  sustentables,', 15, 88);
            pdf.text('el  sector  Turismo tiene  un "'+$('#txt_05_turismo').text()+'" de participacion  municipal ,', 15, 92);
            pdf.text('las actividades Piscicolas,entre crianza y pesca tiene un "'+$('#txt_06_psicola').text()+'".', 15, 96);
            pdf.text('El rubro Minero,principalmente de extraccion cuenta con el "'+$('#txt_07_minero').text()+'"', 15, 100);
            
            pdf.text('La distribucion geografica de la clasificacion (Agropecuario', 15, 108);
            pdf.text('intensivo) tiene un "'+$('#txt_08_agro_int').text()+'" y la clasificacion de (Agropecuario Extensivo) con "'+$('#txt_09_agro_ext').text()+'".', 15, 112);
            pdf.text('Las tierras destinadas al uso Agrosilvopastoril tienen el "'+$('#txt_10_agrosilv').text()+'" del', 15, 116);
            pdf.text('territorio posee (Aptitud forestal) El "'+$('#txt_11_ap_fores').text()+'",esta destinado al,', 15, 120);
            pdf.text('(Uso limitado y restringido) ,El "'+$('#txt_12_uso_limi').text()+'",dentro de las areas protegidas,', 15, 124);
            pdf.text('en reservas forestales,en areas de inmovilizacion ', 15, 128);
            pdf.text('y en servidumbres ecologicas.', 15, 132);

            pdf.text('Referente a los Grados de Pobreza, de los servicios basicos el "'+$('#txt_13_acc_ee').text()+'"', 15, 140);
            pdf.text('de la poblacion tiene  (Acceso a Energia Electrica), seguido del "'+$('#txt_14_acc_vivienda').text()+' "', 15, 144);
            pdf.text('tiene  (Acceso a vivienda ).', 15, 148);
            pdf.text('En cuanto a los servicios sociales, el "'+$('#txt_15_acc_educa').text()+'" de la poblacion tiene', 15, 152);
            pdf.text('(Acceso a la educacion), el "'+$('#txt_16_acc_salud').text()+'"  a   (Servicios de Salud)', 15, 156);
            pdf.text('y el "'+$('#txt_17_acc_agua').text()+'" de la poblacion tienen (Acceso a servicios de agua).', 15, 160);
            

            let date = new Date()
            let day = date.getDate()
            let month = date.getMonth() + 1
            let year = date.getFullYear()
                
            pdf.addImage(logo_mmaya.src, 'PNG', 15, 15, 50, 18.3);
            pdf.addImage(logo_madre.src, 'PNG', 75, 15, 50, 18.3);
            pdf.addImage(logo_giz.src, 'PNG', 135, 15, 60, 18.3);
            pdf.addImage(chart_children.props.src, 'PNG', 130, 60, 70, 60);
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
        State('map_1', 'figure')
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
    Output('txt_municipio', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return '' + terr5['MUNICIPIO'].astype(str).values + ''
@app.callback(
    Output('txt_01_ap_suelo', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Ap.suelo'].astype(str).values + ' %'
@app.callback(
    Output('txt_02_abu_rrhh', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Abu.rrhh'].astype(str).values + ' %'
@app.callback(
    Output('txt_03_riq_espe', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Riqueza.es'].astype(str).values + ' %'
@app.callback(
    Output('txt_04_cap_carb', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Captura.ca'].astype(str).values + ' %'
@app.callback(
    Output('txt_05_turismo', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Turismo'].astype(str).values + ' %'
@app.callback(
    Output('txt_06_psicola', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Piscicol'].astype(str).values + ' %'
@app.callback(
    Output('txt_07_minero', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Minero'].astype(str).values + ' %'
@app.callback(
    Output('txt_08_agro_int', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Agro.inten'].astype(str).values + ' %'
@app.callback(
    Output('txt_09_agro_ext', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Agro.exten'].astype(str).values + ' %'
@app.callback(
    Output('txt_10_agrosilv', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Agrosilvo'].astype(str).values + ' %'
@app.callback(
    Output('txt_11_ap_fores', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Ap.fores'].astype(str).values + ' %'
@app.callback(
    Output('txt_12_uso_limi', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Uso.limit'].astype(str).values + ' %'
@app.callback(
    Output('txt_13_acc_ee', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Acc.EE'].astype(str).values + ' %'
@app.callback(
    Output('txt_14_acc_vivienda', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Acc.vivien'].astype(str).values + ' %'
@app.callback(
    Output('txt_15_acc_educa', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Acc.edu'].astype(str).values + ' %'
@app.callback(
    Output('txt_16_acc_salud', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Acc.salud'].astype(str).values + ' %'
@app.callback(
    Output('txt_17_acc_agua', component_property='children'),
    [Input('w_provincias', 'value')],
    [Input('w_municipios', 'value')])
def get_clasificacion_value(w_provincias,w_municipios):
    terr5 = terr2[(terr2['PROVINCIA'] == w_provincias) & (terr2['MUNICIPIO'] == w_municipios)]
    return ' ' + terr5['Acc.agua'].astype(str).values + ' %'

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
@app.callback(Output('map_1', 'figure'),
              [Input('w_provincias', 'value')],
              [Input('w_municipios', 'value')])
def update_mapa(w_provincias, w_municipios):
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
    app.run_server(debug=True)