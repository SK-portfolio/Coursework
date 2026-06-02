import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("gapminder.csv")
agg = df.groupby(['continent', 'year'])['lifeExp'].mean().reset_index()
ireland = df[df['country'] == 'Ireland']

#PartA
#'''A
df_2002 = df[df['year'] == 2002]    #all country data
ireland = df_2002[df_2002['country'] == 'Ireland'] #ireland data

#Ch1: popn. - size
plt.figure(figsize=(10,6))
plt.scatter(df_2002['gdpPercap'], df_2002['lifeExp'],
            s=df_2002['pop'] / 1e5, alpha=0.8, label='Other Countries')
plt.scatter(ireland['gdpPercap'], ireland['lifeExp'],
            s=ireland['pop'] / 1e5, c='r', label='Ireland')
plt.xlabel('GDP per capita')
plt.ylabel('Life Expectancy')
plt.title('GDP vs Life Expectancy (Population as Size)')
plt.legend()
plt.show()

#Ch2: popn. - colour
plt.figure(figsize=(10,6))
plt.scatter(df_2002['gdpPercap'], df_2002['lifeExp'], 
            c=df_2002['pop'], cmap='viridis', s=200, alpha=0.5, label='Other Countries')
plt.scatter(ireland['gdpPercap'], ireland['lifeExp'], 
            c=ireland['pop'], edgecolor='red',
            cmap='viridis', s=200, alpha=0.9, label='Ireland')
plt.colorbar(label='Population (in millions)')
plt.xlabel('GDP per capita')
plt.ylabel('Life Expectancy')
plt.title('GDP vs Life Expectancy (Population as Color)')
plt.legend()
plt.show()

#Ch3: popn. - opacity
plt.figure(figsize=(10,6))
    # normalise pop to 0.1-1 opacity range
opacity = (df_2002['pop'] - df_2002['pop'].min()) / (df_2002['pop'].max() - df_2002['pop'].min()) * 0.9 + 0.1
plt.scatter(df_2002['gdpPercap'], df_2002['lifeExp'], s=200, alpha=opacity, label='Other Countries')
plt.scatter(ireland['gdpPercap'], ireland['lifeExp'],
            edgecolor='red', s=200, alpha=opacity)
    #replot ireland outline only(for clarity)
plt.scatter(ireland['gdpPercap'], ireland['lifeExp'],
            edgecolor='red', facecolor= 'none', s=200, alpha=0.5, label='Ireland')
plt.xlabel('GDP per capita')
plt.ylabel('Life Expectancy')
plt.title('GDP vs Life Expectancy (Population as Opacity)')
plt.legend()
plt.show()
#A'''

#PartB
#'''B
agg_continents = agg['continent'].unique()
# ---------- Ch4: Continent as Color ----------
plt.figure(figsize=(10,6))
for cont in agg_continents:
    data = agg[agg['continent'] == cont]
    plt.plot(data['year'], data['lifeExp'], label=cont, linewidth=2)
plt.plot(ireland['year'], ireland['lifeExp'], color='grey', linewidth=3, label='Ireland')
plt.xlabel('Year')
plt.ylabel('Life Expectancy')
plt.title('Life Expectancy over Time (Continent as Color)')
plt.legend()
plt.show()

# ---------- Ch5: Continent as Marker Style ----------
#Lstyles = ['solid','dashed','dashdot','dotted',(0, (1, 1))]
Mstyles = ["o","p","s","*","d"]

plt.figure(figsize=(10,6))
#for lstyle, mstyle, cont in zip(Lstyles, Mstyles, agg_continents):
for mstyle, cont in zip(Mstyles, agg_continents):
    data = agg[agg['continent'] == cont]
    plt.plot(data['year'], data['lifeExp'], c = 'blue', marker=mstyle, linewidth=1, label=cont)
    
plt.plot(ireland['year'], ireland['lifeExp'], c = 'r', marker="X", linewidth=2, label='Ireland')
plt.xlabel('Year')
plt.ylabel('Life Expectancy')
plt.title('Life Expectancy over Time (Continent as Line-Marker Combination)')
plt.legend()
plt.show()

# ---------- Ch6: Continent as Facets ----------
fig, axes = plt.subplots(2, 3, figsize=(15,8), sharex=True, sharey=True)
axes = axes.flatten()
plt.suptitle('Life Expectancy over Time (Continent as Facets)')
for i, cont in enumerate(agg_continents):
    ax = axes[i]
    data = agg[agg['continent'] == cont]
    ax.plot(data['year'], data['lifeExp'], color='blue', linewidth=2, label='Continent')
    ax.plot(ireland['year'], ireland['lifeExp'], color='red', linewidth=3, label='Ireland')
    ax.set_title("Ireland vs " + cont)
    ax.set_xlabel('Year')
    ax.set_ylabel('Life Expectancy')
        #legend added to the last subplot only
    if i == len(agg_continents) - 1:
        ax.legend(loc='upper right', bbox_to_anchor=(1.5, 1))

#hide unused subplots (since only use 7/9)
for j in range(len(agg_continents), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()
#B'''

#PartC
#'''C
import matplotlib.cm as cm
import matplotlib.colors as mcolors

#edgecolors for each continent
continent_colors = {
    'Asia': 'orange',
    'Europe': 'blue',
    'Africa': 'green',
    'Americas': 'purple',
    'Oceania': 'brown'
}

norm = mcolors.Normalize(vmin=df['year'].min(), vmax=df['year'].max())
cmap = cm.viridis
continents = df['continent'].unique()
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

plt.suptitle('Chart 7: Exploratory Visualization – Ireland vs Continents (1952–2007)', fontsize=14, weight='bold')
# create scatterplot
for i, cont in enumerate(continents):
    ax = axes[i]
    subset = df[df['continent'] == cont]
    sc = ax.scatter(subset['gdpPercap'], subset['lifeExp'],
                    c=subset['year'], cmap=cmap, norm=norm,
                    s=subset['pop'] / 1e6, alpha=0.5,
                    edgecolors=continent_colors[cont], linewidths=0.4, label=cont)
    
    ax.scatter(ireland['gdpPercap'], ireland['lifeExp'],
               c=ireland['year'], cmap=cmap, norm=norm,
               s=ireland['pop'] / 1e6, edgecolors='red',
               linewidths=0.5, label='Ireland')

    #ax.set_xscale('log')
    ax.set_title(f"Ireland vs {cont}")
    ax.set_xlabel('GDP per Capita')
    ax.set_ylabel('Life Expectancy')
    ax.legend(loc='lower right')
#hide extra subplot if any (6th panel unused)
for j in range(len(continents), len(axes)):
    fig.delaxes(axes[j])

#colorbar and legend
cbar = fig.colorbar(sc, ax=axes, orientation='vertical', fraction=0.025, pad=0.03)
cbar.set_label('Year')

plt.show()
#C'''
