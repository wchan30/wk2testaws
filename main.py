from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamestimatedmetrics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Get and process the data
all_teams = teams.get_teams()
team_ids = [teams['id'] for teams in all_teams]
metrics = teamestimatedmetrics.TeamEstimatedMetrics()
df = metrics.get_data_frames()[0]

ratings = df[['TEAM_NAME','E_OFF_RATING','E_DEF_RATING','W','L']]
ratings['TEAM_NAME'] = df['TEAM_NAME'].str.split().str[-1]
ratings.columns = ['Team','Offensive Rating','Defensive Rating','W','L']

# Calculate averages
off_rating_avg = (ratings['Offensive Rating'].sum())/30
def_rating_avg = (ratings['Defensive Rating'].sum())/30

# Create figure
plt.figure(figsize=(12, 8))
ax = plt.gca()

# Set background color
plt.gcf().set_facecolor('#f0f0f0')
ax.set_facecolor('#f8f8f8')

# Calculate win percentage for color mapping
ratings['Win_Pct'] = ratings['W'] / (ratings['W'] + ratings['L'])
ratings = ratings.sort_values(by='Win_Pct', ascending=False)

# Create scatter plot with color based on win percentage
scatter = plt.scatter(ratings['Offensive Rating'], 
                     ratings['Defensive Rating'],
                     c=ratings['Win_Pct'],
                     cmap='RdYlBu_r',
                     s=90,
                     alpha=1)

# Add colorbar
plt.colorbar(scatter, label='Win Percentage')

# Style the plot
plt.title('NBA Offensive and Defensive Ratings', 
          fontsize=14, pad=20, fontweight='bold')
plt.xlabel('Offensive Ratings', fontsize=12)
plt.ylabel('Defensive Ratings', fontsize=12)

# Calculate min and max values for better axis limits
off_min = ratings['Offensive Rating'].min()
off_max = ratings['Offensive Rating'].max()
def_min = ratings['Defensive Rating'].min()
def_max = ratings['Defensive Rating'].max()

# Set axis limits with some padding
plt.xlim(np.floor(off_min) - 1, np.ceil(off_max) + 1)
plt.ylim(np.ceil(def_max) + 1, np.floor(def_min) - 1)  # Reversed for defensive rating

# Create tick ranges
x_ticks = np.arange(np.floor(off_min), np.ceil(off_max) + 1, 2)  # Every 2 points
y_ticks = np.arange(np.floor(def_min), np.ceil(def_max) + 1, 2)  # Every 2 points
plt.xticks(x_ticks)
plt.yticks(y_ticks)

plt.grid(True, linestyle='--', alpha=0.3)

# Add reference lines for average
plt.axvline(off_rating_avg, color='darkred', linestyle='--', linewidth=0.8, alpha=0.5)
plt.axhline(def_rating_avg, color='darkred', linestyle='--', linewidth=0.8, alpha=0.5)

# Add team labels
for i in range(len(ratings)):
    plt.annotate(ratings['Team'].iloc[i],
                (ratings['Offensive Rating'].iloc[i],
                 ratings['Defensive Rating'].iloc[i]-0.2),
                textcoords="offset points",
                xytext=(0, 5),
                ha='center',
                fontsize=8)

plt.tight_layout()
plt.show()