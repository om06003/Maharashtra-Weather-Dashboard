# Weather Data Visualization Dashboard
#
# This script fetches weather data from the Open-Meteo API and visualizes it using matplotlib.
#
# Requirements:
# - requests
# - matplotlib
#
# Before running, install dependencies:
# pip install requests matplotlib

import requests
import matplotlib.pyplot as plt
import datetime
import sys
from datetime import datetime, timedelta

print("Weather Dashboard - 5-Day Forecast")
print("=================================")

# City coordinates (Maharashtra Districts)
CITY = 'Mumbai'  # Default city
COORDINATES = {
    'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
    'Pune': {'lat': 18.5204, 'lon': 73.8567},
    'Nagpur': {'lat': 21.1458, 'lon': 79.0882},
    'Nashik': {'lat': 20.0059, 'lon': 73.7897},
    'Aurangabad': {'lat': 19.8762, 'lon': 75.3433},
    'Solapur': {'lat': 17.6599, 'lon': 75.9064},
    'Kolhapur': {'lat': 16.7050, 'lon': 74.2433},
    'Thane': {'lat': 19.2183, 'lon': 72.9781},
    'Navi Mumbai': {'lat': 19.0330, 'lon': 73.0297},
    'Amravati': {'lat': 20.9320, 'lon': 77.7523},
    'Akola': {'lat': 20.7002, 'lon': 77.0082},
    'Ahmednagar': {'lat': 19.0948, 'lon': 74.7480},
    'Jalgaon': {'lat': 21.0077, 'lon': 75.5626},
    'Nanded': {'lat': 19.1383, 'lon': 77.3210},
    'Satara': {'lat': 17.6805, 'lon': 74.0183},
    'Latur': {'lat': 18.4088, 'lon': 76.5604},
    'Chandrapur': {'lat': 19.9615, 'lon': 79.2961},
    'Parbhani': {'lat': 19.2608, 'lon': 76.7708},
    'Yavatmal': {'lat': 20.3888, 'lon': 78.1204},
    'Sangli': {'lat': 16.8524, 'lon': 74.5815},
    'Buldhana': {'lat': 20.5292, 'lon': 76.1842},
    'Dhule': {'lat': 20.9042, 'lon': 74.7749},
    'Beed': {'lat': 18.9891, 'lon': 75.7601},
    'Wardha': {'lat': 20.7453, 'lon': 78.6022},
    'Washim': {'lat': 20.1120, 'lon': 77.1428},
    'Hingoli': {'lat': 19.7173, 'lon': 77.1497},
    'Gadchiroli': {'lat': 20.1860, 'lon': 79.9947},
    'Gondia': {'lat': 21.4624, 'lon': 80.1961},
    'Jalna': {'lat': 19.8347, 'lon': 75.8816},
    'Osmanabad': {'lat': 18.1867, 'lon': 76.0358},
    'Palghar': {'lat': 19.6967, 'lon': 72.7698},
    'Raigad': {'lat': 18.5158, 'lon': 73.1822},
    'Ratnagiri': {'lat': 16.9902, 'lon': 73.3120},
    'Sindhudurg': {'lat': 16.0039, 'lon': 73.4644}
}

# Fetch 5-day weather forecast data from Open-Meteo
def fetch_weather_data(city):
    if city not in COORDINATES:
        print(f"Error: City '{city}' not found. Available cities: {', '.join(COORDINATES.keys())}")
        sys.exit(1)
        
    coords = COORDINATES[city]
    url = f'https://api.open-meteo.com/v1/forecast?latitude={coords["lat"]}&longitude={coords["lon"]}&hourly=temperature_2m,relative_humidity_2m&timezone=auto'
    
    print(f"\nFetching weather data for {city}...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("Weather data fetched successfully!")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        print("Please make sure you have an active internet connection")
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing weather data: {e}")
        print("Response content:", response.text)
        sys.exit(1)

# Parse the data for visualization
def parse_weather_data(data):
    times = []
    temps = []
    humidity = []
    
    try:
        # Get the next 5 days of data (120 hours)
        for i in range(120):
            time_str = data['hourly']['time'][i]
            temps.append(data['hourly']['temperature_2m'][i])
            humidity.append(data['hourly']['relative_humidity_2m'][i])
            times.append(datetime.fromisoformat(time_str))
        print(f"Parsed {len(times)} hours of weather data")
        print(f"Temperature range: {min(temps):.1f}°C to {max(temps):.1f}°C")
        print(f"Humidity range: {min(humidity):.1f}% to {max(humidity):.1f}%")
        return times, temps, humidity
    except KeyError as e:
        print(f"Error: Missing data in API response: {e}")
        print("API response structure:", data.keys())
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing weather data: {e}")
        sys.exit(1)

# Visualization dashboard
def plot_dashboard(times, temps, humidity, city):
    try:
        # Clear any existing plots
        plt.clf()
        
        # Set the style and color palette
        plt.style.use('default')  # Using default matplotlib style
        colors = ['#1f77b4', '#2ca02c']  # Blue for temperature, Green for humidity
        
        # Create figure and axis
        fig, ax1 = plt.subplots(figsize=(12, 6))
        # Set background colors
        fig.patch.set_facecolor('white')
        ax1.set_facecolor('#f8f8f8')
        # Add grid
        ax1.grid(True, linestyle='--', alpha=0.7, color='#cccccc')
        
        # Temperature plot (using first color)
        temp_color = colors[0]
        ax1.set_xlabel('Time', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Temperature (°C)', color=temp_color, fontsize=10, fontweight='bold')
        line1 = ax1.plot(times, temps, color=temp_color, marker='o', label='Temperature',
                 linewidth=2, markersize=6, markerfacecolor='white')
        ax1.tick_params(axis='y', labelcolor=temp_color)
        
        # Rotate x-axis labels and format them
        plt.xticks(rotation=45, ha='right')
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # Humidity plot (using second color)
        ax2 = ax1.twinx()
        humidity_color = colors[1]
        ax2.set_ylabel('Humidity (%)', color=humidity_color, fontsize=10, fontweight='bold')
        line2 = ax2.plot(times, humidity, color=humidity_color, marker='s', label='Humidity',
                 linewidth=2, markersize=6, markerfacecolor='white')
        ax2.tick_params(axis='y', labelcolor=humidity_color)
        
        # Title with custom styling
        plt.title(f'5-Day Weather Forecast for {city}, Maharashtra', 
                  pad=20, fontsize=14, fontweight='bold')
        
        # Add legend
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right', 
                  facecolor='white', edgecolor='none', 
                  bbox_to_anchor=(1, 1))
        
        # Adjust layout and display
        fig.tight_layout()
        
        print("\nDisplaying weather plot...")
        plt.show()
        
    except Exception as e:
        print(f"Error creating weather plot: {e}")
        raise

if __name__ == '__main__':
    print("\nMaharashtra Weather Dashboard - 5-Day Forecast")
    print("=" * 50)
    print("\nAvailable Districts:")
    
    # Display districts in columns
    districts = sorted(COORDINATES.keys())
    col_width = 15
    num_cols = 3
    
    for i in range(0, len(districts), num_cols):
        row = districts[i:i + num_cols]
        print("".join(name.ljust(col_width) for name in row))
    
    print("\nCurrently selected district:", CITY)
    print("-" * 50)
    
    data = fetch_weather_data(CITY)
    times, temps, humidity = parse_weather_data(data)
    plot_dashboard(times, temps, humidity, CITY)
