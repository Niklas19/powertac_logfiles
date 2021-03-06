import glob
import pandas as pd

PATH_LOGFILES = '/Users/Niklas/dev/powertac_analyzer/powertac_logfiles/data/processed/'
SUBSTRING_LOGTOOLS = ['BrokerAccounting', 'BrokerBalancing','BrokerMktPrices','TariffMktShare', 'BrokerImbalanceCost']


def get_games():
    matching_files = glob.glob(PATH_LOGFILES + '*{}*'.format(SUBSTRING_LOGTOOLS[0]))
    list_options = []
    for count, file in enumerate(matching_files):
        tmp = {}
        tmp['label'] = str(count+1)
        tmp['value'] = str(count+1)
        list_options.append(tmp)
    return list_options

def get_current_file(game, file):
    matching_files = glob.glob(PATH_LOGFILES + '*_{}_{}*'.format(game, file))
    return matching_files[0]

def get_current_df(game='1', file='BrokerAccounting', broker=[]):
    path = get_current_file(game, file)
    df_tmp = pd.read_csv(path, delimiter=';')

    if isinstance(broker, str):
        return df_tmp[df_tmp['broker'].isin([broker])]
    if len(broker)==0:
        return df_tmp
    else:
        return df_tmp[df_tmp['broker'].isin(broker)]

def get_participating_brokers(game='1', file='BrokerAccounting'):
    path = get_current_file(game, file)
    df_tmp = pd.read_csv(path, delimiter=';')
    list_options = []
    for broker in df_tmp['broker'].unique():
        tmp = {}
        tmp['label'] = broker
        tmp['value'] = broker
        list_options.append(tmp)
    return list_options


if __name__ == '__main__':
    get_participating_brokers()


