import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = np.array(10000*df['weight']/df['height']**2 > 25, dtype='int8')

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = np.array(df['cholesterol'] > 1, dtype='int8')

df['gluc'] = np.array(df['gluc'] > 1, dtype='int8')

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(
        df,
        value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'],
        id_vars=['cardio']
    )

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(
        data=df_cat,
        col='cardio',
        kind='count',
        hue='value',
        x='variable',
    )

# Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[
        (df['ap_hi'] >= df['ap_lo']) &
        (df['height'] >= df['height'].quantile(0.025)) & 
        (df['height'] <= df['height'].quantile(0.975)) & 
        (df['weight'] >= df['weight'].quantile(0.025)) & 
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)
    
    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(df_heat.shape[1], df_heat.shape[1]))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(
        mask=mask,
        square=True,
        data=corr,
        fmt='0.1f',
        annot=True,
        linewidths=1,
        vmin=-0.08,
        vmax=0.24,
    )
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
