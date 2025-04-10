from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamestimatedmetrics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Get and process the data
all_teams = teams.get_teams()
team_ids = [team['id'] for team in all_teams]
metrics = teamestimatedmetrics.TeamEstimatedMetrics()
df = metrics.get_data_frames()[0]

ratings = df[['TEAM_ID', 'TEAM_NAME','E_OFF_RATING','E_DEF_RATING','W','L']]
ratings['TEAM_NAME'] = df['TEAM_NAME'].str.split().str[-1]
ratings.columns = ['TEAM_ID', 'Team','Offensive Rating','Defensive Rating','W','L']

# Merge with teams data to get abbreviations
team_abbr_dict = {team['id']: team['abbreviation'] for team in all_teams}
ratings['Abbreviation'] = ratings['TEAM_ID'].map(team_abbr_dict)

# Calculate averages
off_rating_avg = (ratings['Offensive Rating'].sum())/30
def_rating_avg = (ratings['Defensive Rating'].sum())/30

# Create figure
plt.figure(figsize=(14, 10))
ax = plt.gca()

# Set background color
plt.gcf().set_facecolor('#f0f0f0')
ax.set_facecolor('#f8f8f8')

# Calculate win percentage for color mapping
ratings['Win_Pct'] = ratings['W'] / (ratings['W'] + ratings['L'])
ratings = ratings.sort_values(by='Win_Pct', ascending=False)

# Style the plot
plt.title('NBA Offensive and Defensive Ratings', 
          fontsize=16, pad=20, fontweight='bold')
plt.xlabel('Offensive Ratings', fontsize=14)
plt.ylabel('Defensive Ratings', fontsize=14)

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

# Function to get team logos
def get_team_logo(team_abbr, zoom=0.15):
    try:
        # Manual corrections for teams with different abbreviations
        abbr_corrections = {
            'NOP': 'no',    # New Orleans Pelicans
            'UTA': 'utah',  # Utah Jazz
        }
        
        # Use corrected abbreviation if available
        url_abbr = abbr_corrections.get(team_abbr, team_abbr.lower())
        # URL for NBA team logos (using ESPN CDN)
        url = f"https://a.espncdn.com/i/teamlogos/nba/500/{url_abbr}.png"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        print(f"Error loading logo for {team_abbr}: {e}")
        # Try alternative URL format as fallback


# Add team logos instead of text
logo_zoom = 0.095
for i in range(len(ratings)):
    team_abbr = ratings['Abbreviation'].iloc[i]
    x = ratings['Offensive Rating'].iloc[i]
    y = ratings['Defensive Rating'].iloc[i]
    
    logo = get_team_logo(team_abbr)
    if logo:
        logo_arr = np.array(logo)
        img_height, img_width = logo_arr.shape[:2]
        zoom_factor = logo_zoom
        
        # Create an OffsetImage with the logo
        im = OffsetImage(logo_arr, zoom=zoom_factor)
        ab = AnnotationBbox(im, (x, y), frameon=False)
        ax.add_artist(ab)

# Add a legend for quadrants
plt.text(off_max - 2, def_min + 2, "Good Offense\nGood Defense", 
         ha='right', va='bottom', fontsize=10, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
plt.text(off_min + 2, def_min + 2, "Bad Offense\nGood Defense", 
         ha='left', va='bottom', fontsize=10, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
plt.text(off_max - 2, def_max - 2, "Good Offense\nBad Defense", 
         ha='right', va='top', fontsize=10, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
plt.text(off_min + 2, def_max - 2, "Bad Offense\nBad Defense", 
         ha='left', va='top', fontsize=10, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))


plt.tight_layout()
plt.show()
