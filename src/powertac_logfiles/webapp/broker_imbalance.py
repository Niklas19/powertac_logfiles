import pandas as pd
import dash_core_components as dcc
import plotly.graph_objs as go
import powertac_logfiles.webapp.helpers as h





def plot_imbalance(gameid, type):
    df_tmp = h.get_current_df(str(gameid), file='BrokerImbalanceCost')
    data = []
    ycol = ''
    for broker in df_tmp['broker'].unique():
        data.append(
            go.Scatter(
            y=df_tmp[df_tmp['broker']==broker][type].values,
            x=df_tmp[df_tmp['broker']==broker]['timeslot'].values,
            mode= 'lines',
            name= broker
            )
        )

    layout = go.Layout(
        #title = {'Test'},
        xaxis={
            'title': 'Timeslot',
            #'type': 'linear' if xaxis_type == 'Linear' else 'log'
        },
        yaxis={
            'title': type.capitalize(),
            #'type': 'linear' if yaxis_type == 'Linear' else 'log'
        },
        #margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
        #height=450,
        #hovermode='closest'
    )

    return {'data' : data, 'layout' : layout}




if __name__ == '__main__':
    df = h.get_current_df(game='2', file='BrokerImbalanceCost')
    print(df.head())