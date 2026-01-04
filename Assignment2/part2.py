# Dealing with point clouds and generating several plots at once.
# Visualize the correlation of solar irradiation with temperature and the correlation of solar irradiation with relative moisture.
# Do this by plotting the point clouds and adding a linear trendline. See the code comments for more details.
# Put the figure in the report with a general description. Describe your code in the report.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde


# loading weather data
data = pd.read_csv('weather_data.csv')
# Extracting relevant columns
# columns = Index(['Unnamed: 0', 'Temperature Air in °C', 'Relative Humidity in %',
#        'Precipitation in mm', 'Precipitation Duration in min',
#        'Global Radiation in W/m2', 'Windspeed in m/s',
#        'Wind Direction in Degrees'],
#       dtype='object')
# plotting point clouds
# python

fig, axs = plt.subplots(1, 2, figsize=(12, 6))

def plot_with_density(ax, x_raw, y_raw, xlabel, title, cmap='viridis'):
    # remove NaNs
    mask = ~np.isnan(x_raw) & ~np.isnan(y_raw)
    x = x_raw[mask]
    y = y_raw[mask]
    if x.size == 0:
        ax.set_title(f'{title} (no data)')
        return

    hb = ax.hexbin(x, y, gridsize=50, cmap=cmap, mincnt=1)
    plt.colorbar(hb, ax=ax, label='point count')
    # linear trendline (fit on the cleaned data)
    coeff = np.polyfit(x, y, 1)
    poly = np.poly1d(coeff)
    xs = np.linspace(x.min(), x.max(), 200)
    ax.plot(xs, poly(xs), 'r--', linewidth=2)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Global Radiation in W/m2')

# First subplot: Solar Irradiation vs Temperature
plot_with_density(axs[0], data['Temperature Air in °C'].values, data['Global Radiation in W/m2'].values,
                  'Temperature Air in °C', 'Solar Irradiation vs Temperature')

# Second subplot: Solar Irradiation vs Relative Humidity
plot_with_density(axs[1], data['Relative Humidity in %'].values, data['Global Radiation in W/m2'].values,
                  'Relative Humidity in %', 'Solar Irradiation vs Relative Humidity')

plt.tight_layout()
plt.savefig('solar_irradiation_correlations.png')
plt.show()


# Visualize the correlation for each pair of columns of your dataset in one single figure.
# Do it by visualizing the so-called correlation matrix of your dataset. See code comments for more details.
# Put the figure in the report with a general description. Describe your code in the report and answer the following questions:
# What can be concluded from this figure?
# Explain the connection between this visualization and the visualizations created in Part 2.

# similarly also with matplotlib with correlation matrix, also plotting density
# dont incldue date column, the first one
data = data.drop(columns=['Unnamed: 0'])
corr = data.corr()  # dont include date column
fig, ax = plt.subplots(figsize=(12, 10))
cax = ax.matshow(corr, cmap='coolwarm')
fig.colorbar(cax, label='Pearson Correlation Coefficient (-1 to 1)')

ticks = np.arange(0, len(corr.columns), 1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(corr.columns, rotation=45, ha='left')
ax.set_yticklabels(corr.columns)

plt.title('Correlation Matrix of Weather Data', pad=20)
plt.tight_layout()
plt.savefig('correlation_matrix.png')
plt.show()
