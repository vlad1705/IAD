import numpy as np
import pandas as pnd
import dateutil
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, DateFormatter
from collections import Counter


def GraphsDisplay(df):
    print("All graphs that may be displayed:")

    for i in range(1, len(df.columns)):
        print( str(i) + ')' + ' - ' + str(df.columns[i]))

    time = pnd.to_datetime(df.index.astype(str) + ' ' + df['Time'].astype(str))

    set_graphs = np.array(list(map(int, input("Set graphs you want to be displayed by their number:").split())))

    for i in set_graphs:

        if type(df.iloc[0, i]) is not str:

            x = time
            y = np.array(df.iloc[:, i])

            ax = plt.figure().add_subplot()
            ax.plot(x, y, label=df.columns[i])

            ax.xaxis.set_major_locator(DayLocator())
            ax.xaxis.set_major_formatter(DateFormatter("%d %b"))

            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
            plt.ylabel(df.columns[i])

            ax.grid(which='major', color='black')
            ax.grid(which='minor', linestyle='dotted')
            ax.minorticks_on()
            plt.legend()

        else:
            fig, ax = plt.subplots()

            dictionary = Counter(df.iloc[:, i])
            values = np.array(list(dictionary.values()))
            keys = np.array(list(dictionary.keys()))

            ax.pie(values, radius=1, startangle=90)

            ax.set(aspect="equal", title=df.columns[i])

            plt.legend(labels=keys, bbox_to_anchor=(1, 1))

        plt.show()


def converse_time(df):
    for i in range(df.shape[0]):
        df.loc[i, 'Time'] = dateutil.parser.parse(df.loc[i, 'Time'])
    df['Time'] = pnd.to_datetime(df['Time'], format='%H:%M').dt.time


def converse_date(df):
    for i in range(df.shape[0]):
        df.loc[i, 'day/month'] = dateutil.parser.parse(df.loc[i, 'day/month'] + '2019').date()

def converse_numbers(df):
    for i in ['Humidity', 'Wind Speed', 'Wind Gust']:
        df[i] = df[i].replace('\D', '', regex=True).astype(int)
    df['Pressure'] = df['Pressure'].replace(',', '.', regex=True).astype(float)

def dataParsing(df):
    converse_numbers(df)
    converse_time(df)
    converse_date(df)
    df.set_index('day/month', inplace=True)
    return df

dataframe = pnd.read_csv('DATABASE.csv', sep=';')

parseddata = dataParsing(dataframe)

GraphsDisplay(parseddata)
