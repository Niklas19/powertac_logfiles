import dash
import flask
import os
import threading
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_dangerously_set_inner_html
from flask import flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from powertac_logfiles import build as b
from powertac_logfiles.webapp import helpers as h


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__ ))))
UPLOAD_FOLDER = os.path.join(BASE_DIR,'data/local')
ALLOWED_EXTENSIONS = set(['state', 'trace','doc'])
UPLOAD_COMPONENT = html.Div([
            dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
<title>Python Flask File Upload Example</title>
<h2 style="margin-top: 0px;">Select file(s) to upload</h2>
<div style="text-align:center">
<form method="post" action="/upload_file" enctype="multipart/form-data">
    <dl>
		<p>
			<input type="file" name="file" multiple="true" autocomplete="off" required>
		</p>
    </dl>
    <p>
		<input type="submit" value="Submit">
	</p>
</form>
</div>
    '''),
    html.Div([html.Button(children='Convert', id='btn_convert_logs', formAction='/generate'), html.Br(),html.Output(id='out_convert_logs')],style={'text-align':'center'})
])



external_scripts = [
    {
        'src': 'https://use.fontawesome.com/releases/v5.0.13/js/solid.js',
        'integrity': 'sha384-tzzSw1/Vo+0N5UhStP3bvwWPq+uvzCMfrN1fEFe+xBmv1C/AtVX5K0uZtmcHitFZ',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js',
        'integrity': 'sha384-6OIrr52G08NpOFSZdxxz1xdNSndlD4vdcf/q2myIUVO0VsqaGHJsB0RaBE01VTOY',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://code.jquery.com/jquery-3.3.1.slim.min.js',
        'integrity': 'sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js',
        'integrity': 'sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js',
        'integrity': 'sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm',
        'crossorigin': 'anonymous'
    }
]


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,external_scripts=external_scripts)
app.config['suppress_callback_exceptions']=True
server.secret_key = os.urandom(24)
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['MAX_CONTENT_LENGTH'] = 1073741824

app.index_string = '''<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>PowerTAC Analyzer</title>
        {%favicon%}
        {%css%}
    </head>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            <script type="text/javascript">
            </script>
            {%renderer%}
        </footer>
    </body>
</html>'''

app.layout = html.Div([
    html.Header([
        html.H1(children='PowerTAC Analysis Tool'),
        html.Img(src='/assets/powertac_header.png')
        #dcc.Store(id='session', storage_type='session')
    ]),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='About', value='tab-1'),
        dcc.Tab(label='Tables', value='tab-2'),
        dcc.Tab(label='Visualizations', value='tab-3'),
        dcc.Tab(label='KPIs', value='tab-4'),
    ]),
    html.Div(id='tabs-content')
], style={'text-align':'left'})



@app.callback(Output('out_convert_logs','children'),
              [Input('btn_convert_logs','n_clicks')])
def call_process_log_files(n_clicks):
    if n_clicks !=None:
        thread_logfile_creation.start()
        return 'Started log file generation successfully!'

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-2':
        df_tmp = h.get_current_df()
        games = h.get_games()
        participating_brokers = h.get_participating_brokers()
        return html.Div([
            html.H1(children='About the PowerTAC Analyses Tool'),
            html.Div([
            html.Div(dcc.Dropdown(id='dropdown_games',options=games,value=games[0]['value'],clearable=False),style={'width': '100px', 'display': 'inline-block'}),

            html.Div(dcc.Dropdown(id='dropdown_file',
                options=[
                    {'label': 'BrokerAccounting', 'value': 'BrokerAccounting'},
                    {'label': 'BrokerImbalance', 'value': 'BrokerImbalance'},
                    {'label': 'BrokerMktPrices', 'value': 'BrokerMktPrices'}
                ],value='BrokerAccounting',clearable=False), style={'width': '300px', 'display': 'inline-block'}),

            html.Div(dcc.Dropdown(id='dropdown_broker',options=participating_brokers,value=[], multi=True),style={'width': '600px', 'display': 'inline-block'}),

            html.Div(html.Button(id='btn_update_table', children='Update'), style={'display':'inline-block','float': 'right'})],

            style={'vertical-align':'middle','margin':'0px 40px 0px 40px'}),

            dash_table.DataTable(id='mytable',
            css=[{
                'selector': '.dash-cell div.dash-cell-value',
                'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
            }],
            columns=[{"name": i, "id": i} for i in df_tmp.columns],
            data=df_tmp.to_dict('rows'),
            pagination_mode = 'fe',
            filtering=False,
            style_table={
                'maxWidth': '100%',
                'overflowX': 'scroll',
                'maxHeight': '600px',
                'overflowY': 'scroll',
            },
        )
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H1(children='KPIs')
        ])

    elif tab == 'tab-3':
        return html.Div([
            html.H1(children='Visualization'),
            # html.Div(dcc.Input(id='input-box', type='text')),
            # html.Button('Save to Storage', id='btn_store'),
            # html.Br(),
            # html.Button('Show storage', id='btn_out'),
            # html.Div(id='output-store')
        ])

    elif tab == 'tab-1':
        return UPLOAD_COMPONENT

# @app.callback(Output('session', 'data'),
#               [Input('btn_store', 'n_clicks')],
#                [State('input-box', 'value')])
# def on_click(n_clicks, value):
#     # Give a default data dict with 0 clicks if there's no data.
#     if n_clicks!= 0:
#         data = {'Test': str(value)}
#         return data

# @app.callback(Output('output-store', 'children'),
#                 [Input('btn_out', 'n_clicks')],
#                 [State('session', 'data')])
# def update_output(n_clicks, data):
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         return data.get('Test')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_log_files():
    b.make_log_files()

@server.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
            return redirect('/')


thread_logfile_creation = threading.Thread(target=process_log_files)


@app.callback(Output('mytable', 'columns'),
            [Input('btn_update_table','n_clicks')],
              [State('dropdown_games','value'),
               State('dropdown_broker','value'),
               State('dropdown_file','value')])
def update_table(n_clicks, gameid, broker, file):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print(gameid)
        print(broker)
        print(file)
        return [{"name": i, "id": i} for i in h.get_current_df(gameid, file, broker).columns]

@app.callback(Output('mytable', 'data'),
            [Input('btn_update_table','n_clicks')],
              [State('dropdown_games','value'),
               State('dropdown_broker','value'),
               State('dropdown_file','value')])
def update_table2(n_clicks, gameid, broker, file):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return h.get_current_df(gameid, file, broker).to_dict('rows')




if __name__ == '__main__':
    app.run_server(debug=True)
