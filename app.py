from flask import Flask, render_template, request, jsonify
import io
import base64
from weather_dashboard import COORDINATES, fetch_weather_data, parse_weather_data
import matplotlib
matplotlib.use('Agg')  # Required for web server
import matplotlib.pyplot as plt

app = Flask(__name__)

def create_plot(times, temps, humidity, city):
    plt.clf()  # Clear any existing plots
    
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
    
    # Temperature plot
    temp_color = colors[0]
    ax1.set_xlabel('Time', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Temperature (°C)', color=temp_color, fontsize=10, fontweight='bold')
    line1 = ax1.plot(times, temps, color=temp_color, marker='o', label='Temperature',
             linewidth=2, markersize=6, markerfacecolor='white')
    ax1.tick_params(axis='y', labelcolor=temp_color)
    
    plt.xticks(rotation=45, ha='right')
    
    # Humidity plot
    ax2 = ax1.twinx()
    humidity_color = colors[1]
    ax2.set_ylabel('Humidity (%)', color=humidity_color, fontsize=10, fontweight='bold')
    line2 = ax2.plot(times, humidity, color=humidity_color, marker='s', label='Humidity',
             linewidth=2, markersize=6, markerfacecolor='white')
    ax2.tick_params(axis='y', labelcolor=humidity_color)
    
    plt.title(f'5-Day Weather Forecast for {city}, Maharashtra', 
              pad=20, fontsize=14, fontweight='bold')
    
    # Add legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right', 
              facecolor='white', edgecolor='none', 
              bbox_to_anchor=(1, 1))
    
    fig.tight_layout()
    
    # Convert plot to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100, facecolor='white')
    img.seek(0)
    plt.close()
    
    return base64.b64encode(img.getvalue()).decode()

@app.route('/')
def home():
    districts = sorted(COORDINATES.keys())
    return render_template('index.html', districts=districts)

@app.route('/get_weather')
def get_weather():
    try:
        city = request.args.get('city', 'Mumbai')
        data = fetch_weather_data(city)
        times, temps, humidity = parse_weather_data(data)
        
        plot_url = create_plot(times, temps, humidity, city)
        
        # Get current weather
        current_temp = temps[0]
        current_humidity = humidity[0]
        
        return jsonify({
            'success': True,
            'plot': plot_url,
            'city': city,
            'current': {
                'temperature': f'{current_temp:.1f}°C',
                'humidity': f'{current_humidity:.1f}%'
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
