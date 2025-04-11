from dash import Dash, html, dcc, Input, Output, no_update,State,clientside_callback
import mysql.connector
from datetime import datetime
import dash_bootstrap_components as dbc
import time

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
DB_HOST = 'database-1.c12wu4gkibta.us-east-2.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = '-----'
DB_NAME = 'prueba_sql'
lat=0
long=0
#Create the connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn
app.layout = html.Div([
    dbc.Container([
        html.Div(
            className="form-container",
            children=[
                html.H3("Formulario de Registro", style={"textAlign": "center", "marginBottom": "30px"}),

                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Label("Apellido Paterno"),
                            dcc.Input(id='apellido_paterno', type='text', placeholder='Apellido Paterno', className='form-control'),
                        ], className='form-group'),
                        html.Div([
                            html.Label("Apellido Materno"),
                            dcc.Input(id='apellido_materno', type='text', placeholder='Apellido Materno', className='form-control'),
                        ], className='form-group'),
                        html.Div([
                            html.Label("Nombre(s)"),
                            dcc.Input(id='nombre', type='text', placeholder='Nombre(s)', className='form-control'),
                        ], className='form-group'),
                        html.Div([
                            html.Label("CURP"),
                            dcc.Input(id='curp', type='text', placeholder='Clave CURP', className='form-control', maxLength=18),
                        ], className='form-group'),
                        html.Div([
                            html.Label("Clave Electoral"),
                            dcc.Input(id='clave_elector', type='text', placeholder='Clave Electoral', className='form-control', maxLength=18),
                        ], className='form-group'),
                        html.Div([
                            html.Label("Celular"),
                            dcc.Input(id='celular', type='number', placeholder='Celular', className='form-control'),
                        ], className='form-group'),
                        html.Div([
                            html.Label("Fecha de la Gestión"),
                            dcc.DatePickerSingle(id='fecha', date='2025-04-10', display_format='DD-MM-YYYY', className='form-control'),
                        ], className='form-group'),
                        html.Div([
                            html.Label("Monto"),
                            dcc.Input(id='monto', type='number', placeholder='Monto', className='form-control', min=0),
                        ], className='form-group'),
                        html.Div([
                            html.Label("Rubro"),
                            dcc.Dropdown(id='rubro', options=[
                                {'label': 'Salud', 'value': 'Salud'},
                                {'label': 'Apoyo Político', 'value': 'Apoyo Político'},
                                {'label': 'Prensa', 'value': 'Prensa'},
                                {'label': 'Otro', 'value': 'Otro'}
                            ], placeholder='Selecciona un Rubro', className='form-control', style={'backgroundColor': 'white', 'color': 'black'}),
                        ], className='form-group'),
                        html.Div([
                            html.Label("Estatus"),
                            dcc.Dropdown(id='status', options=[
                                {'label': 'Atendido', 'value': 'Atendido'},
                                {'label': 'En atención', 'value': 'En atención'},
                                {'label': 'Pendiente', 'value': 'Pendiente'},
                                {'label': 'No atendido', 'value': 'No atendido'}
                            ], placeholder='Selecciona un Estatus', className='form-control', style={'backgroundColor': 'white', 'color': 'black'}),
                        ], className='form-group'),
                        html.Div([
                            html.Label("Impacto"),
                            dcc.Dropdown(id='impacto', options=[
                                {'label': 'Personal', 'value': 'Personal'},
                                {'label': 'Familiar', 'value': 'Familiar'},
                                {'label': 'Comunitario', 'value': 'Comunitario'}
                            ], placeholder='Selecciona un Impacto', className='form-control', style={'backgroundColor': 'white', 'color': 'black'}),
                        ], className='form-group'),
                        html.Div([
                            html.Label("Imagen"),
                            dcc.Upload(
                                id='imagen',
                                children=html.Button('Subir Imagen', className='btn btn-primary'),
                                accept='image/png, image/jpeg'
                            ),
                            html.Div(id='output-image-upload', style={'marginTop': '10px'})
                        ], className='form-group'),
                        html.Button('Guardar Registro', id='guardar', n_clicks=0, className='btn btn-danger btn-lg', style={'width': '100%', 'marginTop': '10px'})
                    ], width=6),

                    dbc.Col([
                        html.Div([
                            html.Iframe(
                                id='mapa_google',
                                src='assets/map.html',  # Path to your HTML file
                                style={"height": "600px", "width": "100%"},n_clicks=0
                            ),
    
                            # Hidden div for passing lat, lng back to Dash
                            html.Div(id="lat_lng_output", style={"display": "none"})
                        ]),
                        dcc.Store(id='google_store', data={'lat': 0, 'lng': 0}),
                        html.Div(id='output-div', style={'marginTop': '10px'}),
                        dcc.Store(id='finish',data={})
                    ], width=6)
                ])
            ]
        )
    ], fluid=True)
])

app.clientside_callback(
    """
    function(n_clicks) {
        data={}
        if (n_clicks > 0) {
            console.log("Dummy button clicked");
            navigator.geolocation.getCurrentPosition(function(position) {
                localStorage.setItem('latitude_gps', position.coords.latitude);
                localStorage.setItem('longitude_gps', position.coords.longitude);
            })
            var lat = localStorage.getItem('latitude');
            var lng =localStorage.getItem('longitude');
            var lat_gps = localStorage.getItem('latitude_gps');
            var lng_gps =localStorage.getItem('longitude_gps');
            
            // Return the updated data to Dash
            data={'lat': lat, 'lng': lng}
            return {'lat': lat, 'lng': lng,'lat_gps': lat_gps, 'lng_gps': lng_gps};
        }
        return data;
    }
    """,
    Output('finish', 'data'),
    Input('guardar', 'n_clicks')
)
@app.callback(
              Input('finish', 'data'))
def update_lat_lng(data):
    print(data)
    lat=data.get('lat')
    lng=data.get('lng')
    print(lat,lng)
    
@app.callback(
    Output('output-image-upload', 'children'),
    [Input('imagen', 'contents')]
)
def update_output_image(contents):
    if contents is not None:
        return html.Img(src=contents, style={'maxWidth': '100%', 'maxHeight': '200px'})
    return None


# @app.callback(
#     [Output('output-div', 'children'),
#       Output('guardar', 'disabled'),
#       Output('interval', 'disabled')],
#     [Input('guardar', 'n_clicks'),
    
#         State('apellido_paterno', 'value'),
#         State('apellido_materno', 'value'),
#         State('nombre', 'value'),
#         State('curp', 'value'),
#         State('clave_elector', 'value'),
#         State('celular', 'value'),
#         State('fecha', 'date'),
#         State('monto', 'value'),
#         State('rubro', 'value'),
#         State('status', 'value'),
#         State('impacto', 'value'),
#         State('google_store', 'data')
#     ]
# )


@app.callback(Output('output-div', 'children'),
      Output('guardar', 'disabled'),[Input('finish','data'),
                        State('apellido_paterno', 'value'),
        State('apellido_materno', 'value'),
        State('nombre', 'value'),
        State('curp', 'value'),
        State('clave_elector', 'value'),
        State('celular', 'value'),
        State('fecha', 'date'),
        State('monto', 'value'),
        State('rubro', 'value'),
        State('status', 'value'),
        State('impacto', 'value'),
                        ])
def save_record(disabled, apellido_paterno, apellido_materno, nombre, curp, clave_elector, celular, fecha, monto, rubro, status, impacto):
    if disabled !={}:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        #Connect to the RDS MySQL database
        conn = get_db_connection()  # You must define this function elsewhere
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(tables)
        cursor.execute("""
            INSERT INTO formulario_registro (
                apellido_paterno, apellido_materno, nombre, curp, clave_elector,
                celular, fecha_gestion, monto, rubro, estatus, impacto,imagen_url, latitud_introducida, longitud_introducida, fecha_registro, latitud_gps,longitud_gps
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s)
        """, (
            apellido_paterno, apellido_materno, nombre, curp, clave_elector,
            celular, fecha, monto, rubro, status, impacto, "pendiente",disabled.get('lat'), disabled.get('lng'), now,disabled.get('lng_gps'),disabled.get('lng_gps')
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return html.Div([
            html.H2(f"Registro guardado exitosamente a las {now}"),
            html.P(f"Nombre: {nombre} {apellido_paterno} {apellido_materno}"),
            html.P(f"CURP: {curp}"),
            html.P(f"Clave Electoral: {clave_elector}"),
            html.P(f"Celular: {celular}"),
            html.P(f"Fecha de Gestión: {fecha}"),
            html.P(f"Monto: {monto}"),
            html.P(f"Rubro: {rubro}"),
            html.P(f"Estatus: {status}"),
            html.P(f"Impacto: {impacto}"),
            html.P(f"Ubicación introducida por usuario: {disabled.get('lat')}, {disabled.get('lng')}"),
            html.P(f"Ubicación según IP: {disabled.get('lat_gps')}, {disabled.get('lng_gps')}"),

        ]), True
    return "", no_update


#Run the app
if __name__ == "__main__":
    app.run(debug=True)
