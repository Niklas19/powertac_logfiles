import dash
import dash_core_components as dcc
import dash_html_components as html
import powertac_logfiles.vis.components as cs

from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate


app = dash.Dash(__name__)
app.title = 'PowerTAC Analyzer'
app.config['suppress_callback_exceptions']=True

### Additional Styles
colors = {
    'background': '#696969',
    'text': 'white'
}

graph1 = cs.plot_broker_acc()
table = cs.generate_table()


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
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
# Tab
    if tab == 'tab-1':
        return html.Div([
            html.H1(children='About the PowerTAC Analyses Tool'),
            table])

    elif tab == 'tab-2':
        return html.Div([
            html.H1(children='Market details'),
            graph1
        ])

    elif tab == 'tab-3':
        return html.Div([
            html.H1(children='KPIS'),
            html.Div(dcc.Input(id='input-box', type='text')),
            html.Button('Save to Storage', id='btn_store'),
            html.Button('Show storage', id='btn_out'),
            html.Div(id='output-store', children='Hallo')
        ])

    elif tab == 'tab-4':
        return html.Div([
            html.H1(children='Settings'),
            dcc.Input(id='input-1-keypress',placeholder='Enter a value...',type='text',value=''),
            html.Div(id='output-keypress')
        ])

#________Tab4_____________
@app.callback(Output('output-keypress', 'children'),
              [Input('input-1-keypress', 'value')])
def change_output(input1):
    return u'Input 1 is "{}"'.format(input1)



#________Tab3______________
#Input
@app.callback(Output('session', 'data'),
              [Input('btn_store', 'n_clicks')],
               [State('input-box', 'value')])
def on_click(n_clicks, value):
    # Give a default data dict with 0 clicks if there's no data.
    if n_clicks!= 0:
        data = {'Test': str(value)}
        return data


#Output
@app.callback(Output('output-store', 'children'),
                [Input('btn_out', 'n_clicks')],
                [State('session', 'data')])
def update_output(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return data.get('Test')


if __name__ == '__main__':
    app.run_server(debug=True)