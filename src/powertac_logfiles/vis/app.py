import dash
import dash_core_components as dcc
import dash_html_components as html
import powertac_logfiles.vis.components as cs


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'PowerTAC Analyzer'

### Additional Styles
colors = {
    'background': '#696969',
    'text': 'white'
}




app.layout = html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']},children=[

    html.H1(children='PowerTAC Analyzer'),

    html.Div(children='Dash: A web application framework for Python.',style={
        'textAlign': 'right',
        'color': colors['text']
    }),

    cs.generate_table(),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)