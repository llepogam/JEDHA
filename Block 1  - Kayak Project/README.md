# Kayak Project

The target of this project is to plan a trip based on the weather data. Here are the steps handled in thie project
- Spotting the best cities to explore based on the 7 days weather forecast
- Find the available hotels in the next days in these cities
- Create vizualisation per cities of the available hotel and store them on a S3 bucket

## Project Structure

The repository is organized into four main folders:

- **00_Cities**: Contains data and scripts related to the French cities selected and their information
  - `cities.txt`: Initial list of cities to analyze
  - `coordinates.csv`: Geocoded city data with INSEE codes
  - `weather.csv` & `weather_aggregated.csv`: Weather data outputs
  - `booking.json`: Final hotel data
  - `image/`: Directory for generated visualizations

- **01_Weather**: Manages weather data collection and analysis from Meteo Concept API
  - `weather.py`: Functions for fetching and analyzing weather data
  
- **02_Booking**: Handles scraping of hotel information from Booking.com
  - `booking/`: Scrapy spider for hotel data collection
  
- **03_Data_Transformation**: Processes and combines all the data into useful outputs
  - `transform_data.py`: Script for data cleaning, analysis, and visualization
  - Functions for AWS S3 integration and data storage

## How It Works

1. The system extracts information about cities in France from a predefined list:
   - Geolocates cities using OpenStreetMap's Nominatim API
   - Obtains official INSEE codes using the French government's geo API
   - Creates a foundation dataset with city names, coordinates, and INSEE codes
   
2. Weather forecasts for the coming week are collected for each city using Meteo Concept API:
   - Retrieves 7-day weather forecasts using the INSEE codes
   - Analyzes temperature, precipitation, and wind conditions
   
3. Cities are ranked based on favorable weather conditions:
   - Identifies days with unfavorable conditions (too hot, too cold, rainy, windy)
   - Scores and ranks cities by the number of favorable days
   
4. Booking.com is scraped to find the best hotels in the top 5 weather-ranked cities:
   - Searches for accommodations across multiple dates
   - Collects detailed hotel information including coordinates and pricing
   
5. All data is transformed and consolidated into views with city information, weather forecasts, and hotel locations


## Usage

### 1. City Data Collection

```bash
python 00_Cities/collect_cities.py
```

The city collection component:
- Starts with a predefined list of French cities stored in a `cities.txt` file
- Uses OpenStreetMap's Nominatim API to geocode each city and retrieve precise GPS coordinates
- Queries the French government's geo.api.gouv.fr to obtain the official INSEE code for each city based on its coordinates
- Creates and saves a `coordinates.csv` file with city names, coordinates, and INSEE codes that will be used for weather queries

### 2. Weather Analysis

```bash
python 01_Weather/forecast_analysis.py
```

The weather component:
- Fetches 7-day weather forecasts for each city using the Meteo Concept API
- Collects data on precipitation (rr1, rr10), temperature (tmin, tmax), wind speed (wind10m, gust10m), and rain probability
- Ranks cities based on customizable criteria:
  - Temperature range (default: 20-35°C)
  - Maximum acceptable rainfall (default: 10mm)
  - Maximum acceptable wind speed (default: 50km/h)
- Identifies days with unfavorable conditions (rainy, cold, hot, windy)
- Creates aggregated rankings of cities based on total favorable days

### 3. Hotel Data Scraping

```bash
python 02_Booking/booking_scraper.py
```

The booking component uses Scrapy to gather hotel information:
- Takes the top 5 cities with the best weather from the weather analysis
- Searches for hotels in each city for consecutive days within the next week
- For each city and date combination, scrapes:
  - Hotel names and rankings (including numerical ratings)
  - Price information for a standard 2-adult room
  - Distance from city center
  - Complete address information
  - Precise GPS coordinates (latitude and longitude)
  - Hotel descriptions
  - Direct URLs to the hotel pages

The spider performs a two-step scraping process:
1. First collecting basic information from search results
2. Then following links to individual hotel pages to gather detailed information

### 4. Data Transformation

```bash
python 03_Data_Transformation/transform_data.py
```

The data transformation component:
- Integrates data from all previous stages (cities, weather, booking)
- Filters and cleans hotel data:
  - Removes hotels with insufficient reviews (less than 100)
  - Keeps only hotels with ratings above 7.5
  - Standardizes distance metrics (converting km to meters)
  - Normalizes prices and dates
- Identifies hotels with consecutive night availability (2+ nights)
- Creates visualizations using Plotly:
  - Interactive maps showing hotel locations, prices, and ratings for each top city
  - Temperature distribution map across all cities
  - Weather metrics visualization
- Uploads results to AWS S3 storage:
  - CSV files with weather and hotel data
  - JSON files with booking information
  - Generated visualizations and images

## Output Files and Visualizations

The system generates several data files and visualizations:

### Data Files
- `coordinates.csv`: City names with INSEE codes and coordinates
- `weather.csv`: Raw 7-day weather forecasts for all cities
- `weather_aggregated.csv`: Ranked cities based on weather conditions
- `booking.json`: Detailed hotel information including:
  - Hotel names, rankings, and prices
  - Check-in and check-out dates
  - GPS coordinates (latitude and longitude)
  - Distances from city centers
  - Complete addresses and descriptions

### Visualizations
- Interactive maps for each top city showing:
  - Hotel locations with GPS coordinates
  - Price indicators (size of points)
  - Rating indicators (color of points)
  - Hover information with hotel details
- Weather visualization map showing:
  - Temperature distribution across cities
  - Top-ranked cities highlighted
  - Weather metrics comparison

All outputs are stored both locally and in an AWS S3 bucket for easy access and sharing.

