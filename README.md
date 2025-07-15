# Maharashtra Weather Dashboard

A Python-based weather dashboard that displays 5-day weather forecasts for all districts in Maharashtra, India. The application provides both terminal and web interfaces for viewing temperature and humidity forecasts.

## Features

- Real-time 5-day weather forecasts for all Maharashtra districts
- Temperature and humidity visualization
- Interactive matplotlib-based graphs
- Clean, modern UI
- Support for both terminal and web interfaces
- Uses the Open-Meteo API (no API key required)

## Requirements

- Python 3.6+
- requests
- matplotlib
- pandas
- Flask (for web interface)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/maharashtra-weather-dashboard.git
cd maharashtra-weather-dashboard
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Terminal Interface

Run the following command:
```bash
python weather_dashboard.py
```

### Web Interface

Run the following command:
```bash
python app.py
```
Then open your browser and navigate to `http://localhost:5000`

## Districts Covered

The dashboard includes all major districts in Maharashtra, including:
- Mumbai
- Pune
- Nagpur
- Thane
- Nashik
- And many more...

## Data Source

Weather data is fetched from the [Open-Meteo API](https://open-meteo.com/), which provides free access to weather forecast data.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
