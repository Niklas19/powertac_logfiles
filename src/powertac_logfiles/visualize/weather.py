import matplotlib.pyplot as plt
import seaborn as sns
from powertac_logfiles import data


def visualize_weather():
    df_weather_report = data.load_weather_report()

    fig = plt.figure(figsize=(12, 15))
    ax1 = fig.add_subplot(311)
    ax1.set_title("Temperature")
    ax1 = sns.lineplot(ax=ax1, x="timeslotIndex", y="temperature", data=df_weather_report)
    ax2 = fig.add_subplot(312)
    ax2.set_title("Cloud Cover")
    ax2 = sns.barplot(ax=ax2, x="timeslotIndex", y="cloudCover", data=df_weather_report, color='#14779b')
    ax3 = fig.add_subplot(313)
    ax3.set_title("Wind Speed")
    ax3 = sns.barplot(ax=ax3, x="timeslotIndex", y="windSpeed", data=df_weather_report, color='#14779b')
    fig.tight_layout()
    plt.savefig('{}/weather/weather_report'.format(data.OUTPUT_DIR))
    print("Successfully created weather plot.")
