import dash_table
import pandas as pd
import dash_core_components as dcc
import plotly.graph_objs as go


#CONSTANTS
GAME_SIZE = 7

cols = ['gameId', 'gameSize', 'gameLength', 'AgentUDE', 'Bunnie','COLDPower18', 'CrocodileAgent', 'EWIIS3', 'SPOT', 'VidyutVanika']

df_broker_accounting = pd.read_csv('/Users/Niklas/dev/powertac_analyzer/powertac_logfiles/data/processed/finals_2018_games.csv', nrows=50 ,delimiter=';', usecols=cols)



def generate_table():
    dt_tmp = dash_table.DataTable(
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        id='table',
        columns=[{"name": i, "id": i} for i in df_broker_accounting.columns],
        data=df_broker_accounting.to_dict('records'),
        style_table={
            'maxWidth':'95%',
            'overflowX': 'scroll',
            'maxHeight': '400px',
            'overflowY': 'scroll',
        },
    )
    return dt_tmp


def plot_broker_acc():
    graph = dcc.Graph(
        figure=go.Figure(
            data=[
                go.Scatter(
                y=df_broker_accounting['EWIIS3'].values,
                x=df_broker_accounting['gameId'].values,
                mode='lines',
                name='EWIIS3'),
                go.Scatter(
                    y=df_broker_accounting['COLDPower18'].values,
                    x=df_broker_accounting['gameId'].values,
                    mode='lines',
                    name='COLDPower18'),
                go.Scatter(
                    y=df_broker_accounting['AgentUDE'].values,
                    x=df_broker_accounting['gameId'].values,
                    mode='lines',
                    name='AgentUDE')
                ],
            layout=go.Layout(
                title='Overview Finals',
                showlegend=True,
                legend=go.layout.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph'
    )
    return graph





if __name__ == '__main__':
    print(df_broker_accounting.columns)
