import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### Part 2: Point clouds with trendlines
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


### Part 3: Correlation matrix

# similarly also with matplotlib with correlation matrix, also plotting density
# Convert 'Unnamed: 0' to datetime and then to minutes since start to enable correlation calculation
data['Unnamed: 0'] = pd.to_datetime(data['Unnamed: 0'])
min_time = data['Unnamed: 0'].min()
data['Minutes Since Measure Start'] = (data['Unnamed: 0'] - min_time).dt.total_seconds() / 60
data = data.drop(columns=['Unnamed: 0'])
corr = data.corr()  # dont include date column
fig, ax = plt.subplots(figsize=(12, 10))
cax = ax.matshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax, label='Pearson Correlation Coefficient (-1 to 1)', )

ticks = np.arange(0, len(corr.columns), 1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(corr.columns, rotation=45, ha='left')
ax.set_yticklabels(corr.columns)

plt.title('Correlation Matrix of Weather Data', pad=20)
plt.tight_layout()
plt.savefig('correlation_matrix.png')
plt.show()

corr_pairs = corr.unstack()  # Convert matrix to series
corr_pairs = corr_pairs[corr_pairs != 1.0]  # Remove self-correlations
corr_pairs = corr_pairs.drop_duplicates()  # Remove duplicate pairs
corr_pairs = corr_pairs.sort_values(ascending=False, key=abs)  # Sort by absolute value

print("\nTop 10 Highest Correlations:")
print("-" * 70)
for (var1, var2), corr_value in corr_pairs.head(10).items():
    print(f"{var1:40s} <-> {var2:40s}: {corr_value:6.3f}")
# Relative Humidity in %                   <-> Global Radiation in W/m2                : -0.545
# Temperature Air in °C                    <-> Global Radiation in W/m2                :  0.505
# Temperature Air in °C                    <-> Relative Humidity in %                  : -0.439
# Relative Humidity in %                   <-> Minutes Since Measure Start             :  0.416
# Windspeed in m/s                         <-> Wind Direction in Degrees               :  0.362
# Precipitation in mm                      <-> Precipitation Duration in min           :  0.344
# Relative Humidity in %                   <-> Precipitation Duration in min           :  0.280
# Windspeed in m/s                         <-> Minutes Since Measure Start             : -0.244
# Relative Humidity in %                   <-> Windspeed in m/s                        : -0.225
# Precipitation Duration in min            <-> Global Radiation in W/m2                : -0.138
