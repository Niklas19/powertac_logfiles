import glob
PATH_LOGFILES = '/Users/Niklas/dev/powertac_analyzer/powertac_logfiles/data/processed/'
SUBSTRING_LOGTOOLS = ['BrokerAccounting', 'BrokerBalancing','BrokerMktPrices','TariffMktShare']


def count_files():
    matching_files = glob.glob(PATH_LOGFILES + '*{}*'.format(SUBSTRING_LOGTOOLS[0]))
    for count, file in enumerate(matching_files):
        pass
    return count+1

def get_path_file(game='19', file='BrokerAccounting'):
    matching_files = glob.glob(PATH_LOGFILES + '*_{}_{}*'.format(game, file))
    return matching_files[0]

if __name__ == '__main__':
    print(get_path_file())


