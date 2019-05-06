import dash
import flask
import os
import dash_html_components as html
import dash_core_components as dcc
import dash_dangerously_set_inner_html
from flask import flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from powertac_logfiles import build as b

UPLOAD_FOLDER = "data"
UPLOAD_COMPONENT = html.Div([
            dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
<title>Python Flask File Upload Example</title>
<h2>Select file(s) to upload</h2>
<form method="post" action="/" enctype="multipart/form-data">
    <dl>
		<p>
			<input type="file" name="file" multiple="true" autocomplete="off" required>
		</p>
    </dl>
    <p>
		<input type="submit" value="Submit">
	</p>
</form>
    '''),html.Button(children='Convert', id='btn_convert_logs'), html.Output(id='out_convert_logs')
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
        html.Img(src='/assets/powertac_header.png'),
        dcc.Store(id='session', storage_type='session')
    ]),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='About', value='tab-1'),
        dcc.Tab(label='Market details', value='tab-2'),
        dcc.Tab(label='KPIs', value='tab-3'),
        dcc.Tab(label='Settings', value='tab-4'),
    ]),
    html.Div(id='tabs-content')
], style={'text-align':'center'})



@app.callback(Output('out_convert_logs','children'),
              [Input('btn_convert_logs','n_clicks')])
def process_log_files(n_clicks):
    if n_clicks !=0:
        b.make_log_files()
        return 'Started log file generation successfully!'

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
# Tab
    if tab == 'tab-1':
        return html.Div([
            html.H1(children='About the PowerTAC Analyses Tool')])

    elif tab == 'tab-2':
        return html.Div([
            html.H1(children='Market details')
        ])

    elif tab == 'tab-3':
        return html.Div([
            html.H1(children='KPIS'),
            html.Div(dcc.Input(id='input-box', type='text')),
            html.Button('Save to Storage', id='btn_store'),
            html.Br(),
            html.Button('Show storage', id='btn_out'),
            html.Div(id='output-store')
        ])

    elif tab == 'tab-4':
        return UPLOAD_COMPONENT



@app.callback(Output('session', 'data'),
              [Input('btn_store', 'n_clicks')],
               [State('input-box', 'value')])
def on_click(n_clicks, value):
    # Give a default data dict with 0 clicks if there's no data.
    if n_clicks!= 0:
        data = {'Test': str(value)}
        return data

@app.callback(Output('output-store', 'children'),
                [Input('btn_out', 'n_clicks')],
                [State('session', 'data')])
def update_output(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return data.get('Test')



ALLOWED_EXTENSIONS = set(['state', 'trace', 'png', 'jpg', 'jpeg', 'pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@server.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
            flash('File(s) successfully uploaded')
            return redirect('/')


if __name__ == '__main__':
    app.run_server(debug=True)