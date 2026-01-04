import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def part1_script():
    # get data
    df = pd.read_csv('weather_data.csv', index_col=0)
    df.index = pd.to_datetime(df.index)
    x = df.index
    y = df['Temperature Air in °C']

    # use this dictionary for colors if you like or define your own. access like: somecolors['dark red']
    # these are just to show what color formats are accepted by matplotlib.pyplot
    somecolors = {
        'red': '#FF6666',
        'dark red': '#AA3333',
        'very red': '#FF0000',
        'also very red': (1, 0, 0),
        'another very red': 'red',
        'very green': '#00FF00',
        'very blue': '#0000FF'
    }

    # ------------------------------------------------------------------------------
    # your code here
    # ------------------------------------------------------------------------------
    # plot the temperature values and the weekly mean of the temperature values
    # for the weekly mean, use the Pandas.Series.rolling() method (e.g. y.rolling())

    weekly_mean = y.rolling(window='7D').mean() # Pandas Docu for rolling window operations 

    plt.figure(figsize=(10, 6)) # increased fig size to avoid legend overlapping data points
    plt.plot(x, y, color=somecolors['red'], label='Temperature (5-minutes intervals)')
    plt.plot(x, weekly_mean, color=somecolors['very blue'], label='Weekly Mean Temperature (7-day rolling)')

    plt.ylabel('Temperature in °C')
    plt.legend()
    plt.grid()
    plt.savefig("Part1_Temperature_Weekly_Mean.pdf", format="pdf")  # for your report
    plt.show()


    # use the methods plt.plot() with optional parameters color and label
    # use methods plt.ylabel(), plt.legend(), plt.grid(), plt.show()
    # hint: experiment with the sequence your commands

    # using commands in order given above gives correct plots will all wanted elements (legend, grid)
    # conclusions: plotting should be called first then we call rest of the methods with optional parameters too eg.
    # plt.logscale('y') before plt.show() or location of the legend plt.legend(loc='upper left')

    # regarding chosen colours, we decided to pick 2 contrasting ones, the daily background tempetures to be red but not too bright and eye hurting with 
    # well contrasting blue for the weekly mean line 

    # deduced latitude of the measurements: northern hemisphere

    # ------------------------------------------------------------------------------


def part2_script():
    # get data
    df = pd.read_csv('weather_data.csv', index_col=0)
    df.index = pd.to_datetime(df.index)
    x = df['Global Radiation in W/m2']  # x-values for both plots
    y1 = df['Temperature Air in °C']  # y-values for first plot
    coefficients1 = np.polyfit(x, y1, 1)
    y_trendline1 = np.poly1d(coefficients1)(x)  # y-values of trendline for first plot
    y2 = df['Relative Humidity in %']  # y-values for second plot
    coefficients2 = np.polyfit(x, y2, 1)
    y_trendline2 = np.poly1d(coefficients2)(x)  # y-values of trendline for second plot

    # prepare two plots (this will give you one figure object and one list of axes objects)
    # access the axes objects like ax[0].method() and ax[1].method() to call their methods
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

    # ------------------------------------------------------------------------------
    # your code here
    # ------------------------------------------------------------------------------
    # now use the axes objects to draw plots in them
    # in the first one, plot the point cloud temperature over radiation and the above prepared trendline
    # in the second one, plot the point cloud humidity over radiation and the above prepared trendline
    # use the methods ax[i].scatter(), ax[i].plot(), ax[i].grid()
    # careful: some methods have different names for axes objects: ax[i].set_xlabel(), ax[i].set_ylabel()
    # ------------------------------------------------------------------------------


def part3_script():
    # get data
    df = pd.read_csv('weather_data.csv', index_col=0)
    df.index = pd.to_datetime(df.index)

    # ------------------------------------------------------------------------------
    # your code here
    # ------------------------------------------------------------------------------
    # visualize the correlation matrix of your data
    # the correlation matrix of n data sets set[i] i = 1, ..., n
    # is the matrix (correlation(set[i], set[j]) i,j = 1, ..., n
    # create the correlation matrix with the method DataFrame.corr() (e.g. df.corr())
    # visualize the matrix with the method plt.matshow().
    # use the optional parameter cmap to pick a suitable colormap that is helpful for data analysis
    # use the optional parameters vmin, vmax to adjust the range of the color scale
    # make sure to draw the colorbar with colorbar() to allow interpretation of the plot.
    # label the axis ticks with the columns of your dataframe using plt.xticks() and plt.yticks to
    # ------------------------------------------------------------------------------


if __name__ == '__main__':
    part1_script()
    part2_script()
    part3_script()
    print("Assignment 2 executed!")
