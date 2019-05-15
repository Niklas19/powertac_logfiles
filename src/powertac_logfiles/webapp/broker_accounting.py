import glob
import pandas as pd
import dash_table
PATH_LOGFILES = '/Users/Niklas/dev/powertac_analyzer/powertac_logfiles/data/processed/'
SUBSTRING_LOGTOOLS = ['BrokerAccounting', 'BrokerBalancing','BrokerMktPrices','TariffMktShare', 'BrokerImbalanceCost']




def get_best_games():
    matching_files = glob.glob(PATH_LOGFILES + '*{}*'.format(SUBSTRING_LOGTOOLS[0]))
    for count, file in enumerate(matching_files):
        df_tmp = pd.read_csv(file)
        print(df_tmp.index)
    return


if __name__ == '__main__':
    get_best_games
