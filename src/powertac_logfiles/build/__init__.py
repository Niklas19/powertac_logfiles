from .utils import create_mvn_command  # noqa
from .utils import create_mvn_parameter  # noqa
from .utils import execute_logtool  # noqa
from .utils import get_log_files  # noqa
from .make import make_log_files  # noqa
from .make import make_web_log_files  # noqa


# Constants for local processing

#LOG_FILES = {'BrokerAccounting': 'org.powertac.logtool.example.BrokerAccounting'}

LOG_FILES = {#'BrokerAccounting': 'org.powertac.logtool.example.BrokerAccounting',
             'BrokerBalancingActions': 'org.powertac.logtool.example.BrokerBalancingActions',
             #'BrokerCosts': 'org.powertac.logtool.example.BrokerCosts',
             #'BrokerImbalanceCost': 'org.powertac.logtool.example.BrokerImbalanceCost',
             'BrokerMktPrices': 'org.powertac.logtool.example.BrokerMktPrices',
             #'BrokerPriceAnomaly': 'org.powertac.logtool.example.BrokerPriceAnomaly',
             #'CapacityAnalysis': 'org.powertac.logtool.example.CapacityAnalysis',
             #'CapacityValidator': 'org.powertac.logtool.example.CapacityValidator',
             #'CustomerBalancingCapacity': 'org.powertac.logtool.example.CustomerBalancingCapacity',
             #'CustomerProductionConsumption': 'org.powertac.logtool.example.CustomerProductionConsumption',
             #'CustomerStats': 'org.powertac.logtool.example.CustomerStats',
             #'DemandResponseStats': 'org.powertac.logtool.example.DemandResponseStats',
             #'EnergyMixStats': 'org.powertac.logtool.example.EnergyMixStats',
             #'GameBrokerInfo': 'org.powertac.logtool.example.GameBrokerInfo',
             #'ImbalanceStats': 'org.powertac.logtool.example.ImbalanceStats',
             #'ImbalanceSummary': 'org.powertac.logtool.example.ImbalanceSummary',
             #'MeritOrder': 'org.powertac.logtool.example.MeritOrder',   -> Ask John if helpful or not
             #'MktPriceStats': 'org.powertac.logtool.example.MktPriceStats',
             #'ProductionConsumption': 'org.powertac.logtool.example.ProductionConsumption',
             #'ProductionConsumptionWeather': 'org.powertac.logtool.example.ProductionConsumptionWeather',
             #'SolarProduction': 'org.powertac.logtool.example.SolarProduction',
             #'TariffAnalysis': 'org.powertac.logtool.example.TariffAnalysis',
             #'TariffMktShare': 'org.powertac.logtool.example.TariffMktShare',
             #'TotalDemand': 'org.powertac.logtool.example.TotalDemand',
             #'WeatherForecastStats': 'org.powertac.logtool.example.WeatherForecastStats',
             #'WeatherStats': 'org.powertac.logtool.example.WeatherStats',
             #'WindStats': 'org.powertac.logtool.example.WindStats'
}

GAME_NUMBERS = list(range(1, 2))
