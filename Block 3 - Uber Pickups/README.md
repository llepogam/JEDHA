# Uber Pickup Project

## Overview
This project provides a comprehensive analysis of Uber trip data from New York City in April 2014. The analysis examines spatiotemporal patterns in ride requests and employs advanced clustering techniques to identify high-demand "hot zones" across the city. Through interactive visualizations and machine learning approaches, this notebook reveals valuable insights into urban mobility patterns.

## Dataset
The analysis utilizes the `uber-raw-data-apr14.csv` file containing approximately 564,000 pickup records for April 2014, including:
- Timestamp information
- Geographic coordinates (latitude and longitude)
- Base type identifiers

## Contents

### 1. Exploratory Data Analysis (EDA)
- Data cleaning and preprocessing
- Temporal feature extraction (year, month, day, hour, weekday)
- Geographic filtering using bounding box coordinates for NYC
- Statistical summaries and distribution analysis

### 2. Temporal Pattern Analysis
- Weekly ride distribution patterns (peak on Wednesdays)
- Daily demand cycles (morning rush at 7am, evening peaks between 5-8pm)
- Weekend vs. weekday comparison (elevated nighttime activity on weekends)
- Hourly demand fluctuations by day of week

### 3. Spatial Analysis and Visualization
- Interactive mapping of pickup locations using Plotly
- Base type distribution across geographic regions
- Focused analysis on specific time slices (April 30th at 5pm)

### 4. Unsupervised Learning for Cluster Detection
- **K-Means Clustering**:
  - Optimal cluster determination using the Elbow method
  - Silhouette score validation (k=6 and k=9 identified as optimal)
  - Visualization of cluster centers and boundaries
  
- **DBSCAN Clustering**:
  - Density-based spatial clustering with noise
  - Parameter tuning (eps=0.15, min_samples=10)
  - Noise point filtering and cluster center visualization

### 5. Hot Zone Identification
- Custom `plot_hot_zone()` function development
- Dynamic hot zone detection based on time parameters
- Identification of consistent high-demand areas (airports, Manhattan, Brooklyn)
- Temporal evolution of hot zones throughout the day

## Key Findings
- Demand follows clear weekly cycles with mid-week peaks
- Morning and evening rush hours show distinct demand patterns
- Weekend nightlife creates unique spatial demand distributions
- Major transportation hubs (airports) and central business districts emerge as persistent hot zones
- Hot zone patterns shift dynamically throughout the day


## Future Work
- Extend analysis to multiple months to detect seasonal patterns
- Incorporate external factors (weather, events, holidays)
- Develop predictive models for demand forecasting
- Optimize vehicle allocation based on spatiotemporal patterns
- Compare patterns across different ride-sharing services

