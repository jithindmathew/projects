import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    plt.figure(figsize=(10, 10))
    plt.scatter(df.iloc[:, 0], df.iloc[:, 1])

    # Create first line of best fit
    regressor = linregress(df.iloc[:, 0], df.iloc[:, 1])
    print(regressor.slope, regressor.intercept)
    x = range(1880, 2051)
    plt.plot(x, regressor.intercept + regressor.slope*x, 'r')

    # Create second line of best fit
    regressor2 = linregress(df.iloc[120:, 0], df.iloc[120:, 1])
    print(regressor2.slope, regressor2.intercept)
    x2 = range(2000, 2051)
    plt.plot(x2, regressor2.intercept + regressor2.slope*x2, 'g')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()