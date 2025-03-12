# NBA Team Efficiency Tracker

A data visualization tool that extracts NBA team efficiency metrics from the official NBA API and displays offensive and defensive ratings for all teams in a quadrant chart format. The visualization includes team logos for easy identification and highlights performance relative to league averages.

## Features

- **Data Extraction**: Pulls live data from the official NBA API using the `nba_api` package
- **Comprehensive Metrics**: Visualizes both offensive and defensive efficiency ratings for all 30 NBA teams
- **Visual Clarity**: Uses team logos instead of text labels for an intuitive and clean design
- **Performance Context**: Shows league averages and categorizes teams into performance quadrants
- **Updated Weekly**: Designed to be refreshed weekly to track team performance trends

## Technical Implementation

- **Data Acquisition**: Uses `nba_api.stats.endpoints.teamestimatedmetrics` for official NBA efficiency data
- **Data Processing**: Employs Pandas for data manipulation and preparation
- **Visualization**: Built with Matplotlib for customized quadrant charts with team logos
- **Image Processing**: Integrates PIL and requests to fetch and display team logos from ESPN CDN
- **Statistical Context**: Calculates and displays league average lines for both offensive and defensive metrics

## How It Works

The tool creates a four-quadrant visualization where:
- X-axis represents Offensive Rating (points scored per 100 possessions)
- Y-axis represents Defensive Rating (points allowed per 100 possessions)
- Team logos are positioned based on their ratings
- Quadrants clearly indicate different performance profiles (good offense/defense, bad offense/defense)

## Sample Output

The visualization shows each team's position relative to league averages with:
- Team logos for quick visual identification
- Gridlines for easy metric reading
- Performance quadrant descriptions
- League average reference lines

## Getting Started

1. Clone this repository
2. Install required dependencies:
   ```
   pip install nba_api pandas matplotlib numpy requests pillow
   ```
3. Run the script to generate the current visualization:
   ```
   python nba_efficiency_tracker.py
   ```

## Future Improvements

- Add historical tracking to show week-over-week changes in team efficiency
- Implement interactive features using Plotly
- Add automated data refresh via GitHub Actions
- Create web-based dashboard for easier sharing

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request.
