import dash_html_components as html
import pandas as pd


dataframe = pd.read_csv('/Users/Niklas/dev/powertac_analyzer/powertac_logfiles/data/processed/PowerTAC_2018_Finals_1_BrokerAccounting.csv')


def generate_table(max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



