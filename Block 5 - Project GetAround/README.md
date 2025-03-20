# Pricing Optimization Project for Getaround

## Introduction

This repository contains a complete solution for optimizing car rental operations and pricing for Getaround, a peer-to-peer car sharing platform (the "Airbnb for cars"). The project addresses critical business challenges related to rental delays and pricing optimization.

### Project Background

Getaround allows people to rent cars from individuals for periods ranging from hours to days. The company has experienced rapid growth since its founding in 2009, with over 5 million users and approximately 20,000 available cars worldwide as of 2019.

A key operational challenge identified by Getaround is the issue of late returns at checkout, which can cause significant problems:
- Creates friction for the next driver if the car is booked again on the same day
- Results in customer dissatisfaction due to waiting for delayed returns
- Sometimes leads to rental cancellations when cars aren't returned on time

To address these issues, Getaround is implementing a minimum delay between consecutive rentals, preventing cars from appearing in search results if requested checkin/checkout times are too close to existing bookings. This solution requires careful optimization to balance customer satisfaction with revenue impact.

### Project Objectives

This project helps Getaround determine:
1. The optimal minimum delay threshold between consecutive rentals
2. The appropriate scope for implementing this feature (all cars vs. only Connect cars)
3. The revenue impact of different threshold settings
4. The effectiveness of thresholds in preventing problematic cases

Through data analysis, predictive modeling, interactive visualization, and API development, this project provides stakeholders with the tools to make informed decisions that balance operational efficiency, customer satisfaction, and business revenue.

## Project Components

### 1. Data Analysis

This component contains exploratory data analysis (EDA) on the car rental dataset, focusing on delays between rentals and their impact on cancellations and user experience:

#### Dataset Overview
- Analysis of ~21,000 car rental reservations
- Key variables analyzed: rental timing, delays, check-in/out times, car utilization
- Focus on time gaps between consecutive rentals and checkout delays

#### Key Findings
- Only 9% of rentals have information about the previous rental (suggesting most cars have significant idle time between rentals)
- When categorizing time between rentals:
  - Cancelation rates don't significantly increase with shorter time gaps between reservations
  - Only 218 out of 21,000 reservations were negatively impacted by delays from previous rentals
  - 30 minutes appears to be a reasonable minimum gap between consecutive reservations

#### Car Utilization Patterns
- Most cars in the system are rented infrequently (majority with only 1-3 rentals)
- Only a small number of cars have more than 10 rentals in the dataset
- Connect check-in type is more common for same-day consecutive rentals

#### Checkout Behavior Analysis
- 32% of all rentals have late checkouts
- 80% of late checkouts involve delays of less than 2 hours
- Different patterns observed between mobile and connect check-in types
- Threshold analysis shows different optimal minimum gaps for mobile vs. connect rentals

#### Visualization
- Time series analysis of delays
- Categorized delay impacts by check-in type
- Threshold analysis to determine optimal minimum reservation gaps

This analysis provides crucial insights for determining the minimum time threshold between consecutive rentals and guides the optimization of pricing based on expected delays.

### 2. Pricing Optimization

The pricing optimization module implements a machine learning model to predict optimal car rental pricing based on various features. The model is built using MLflow for experiment tracking and model management.

#### Model Architecture
- **Model Type**: CatBoost Regressor (gradient boosting on decision trees)
- **Pipeline**: Includes preprocessing steps for both numeric and categorical features
- **Preprocessing**: 
  - Numeric features: SimpleImputer (mean strategy) + StandardScaler
  - Categorical features: SimpleImputer (most frequent strategy) + OneHotEncoder
  - Model key categorization for low-frequency models

#### Model Parameters
- Iterations: 1000
- Learning rate: 0.03
- Depth: 6
- Loss function: RMSE
- Random seed: 42

#### Performance Metrics
- **R² Score (Test Set)**: 0.784
- **RMSE**: 15.31
- Full training pipeline implemented with train/test split (80/20 ratio)

#### Implementation Details
- Data preparation includes handling of low-frequency model types
- MLflow tracking for experiment management and model versioning
- Automated preprocessing pipeline to ensure consistent transformations
- Model is exported and registered for production deployment

The model provides reliable price predictions based on car features, enabling dynamic pricing optimization and helping car owners maximize their rental income while maintaining competitive rates.

### 3. Streamlit App

An interactive web application built with Streamlit that provides comprehensive analysis of car rental data with a focus on delays between reservations. The app helps stakeholders visualize the impact of delays and make informed decisions about minimal time thresholds between bookings.

#### Key Features
- **Interactive Dashboard Layout**: Multi-tab interface for organized data exploration
- **Real-time Data Visualization**: Dynamic charts and graphs powered by Plotly
- **Threshold Analysis Tool**: Interactive slider to analyze the impact of different minimum delay settings
- **Comprehensive Metrics**: Detailed breakdown of rental statistics by various categories

#### App Sections
1. **Key Insights**: Summary metrics and findings about rental patterns and delays
   - Total rentals, check-in types, and delay impacts
   - Highlighted key findings about time gaps, checkout behaviors, and recommended buffer times

2. **General Analysis**: Broader analysis of rental patterns
   - Distribution visualizations for key metrics (check-in type, state, time gaps)
   - Comparative analysis of time between consecutive rentals
   - Rental frequency analysis by car

3. **Late Checkout Impact**: Analysis of how late checkouts affect subsequent rentals
   - Checkout delay categorization and visualization
   - Cancellation rates related to late checkouts
   - Impact assessment on follow-up rentals

4. **Threshold Analysis**: Interactive tool for determining optimal minimum delay thresholds
   - Impact assessment for different minimum delay settings (15-360 minutes)
   - Separate analysis for connect and mobile check-in types
   - Detailed breakdown of affected rentals at selected thresholds

The app provides stakeholders with the data-driven insights needed to implement an optimal minimum delay policy between consecutive rentals, balancing customer experience with business efficiency.

### 4. API

A RESTful API built with FastAPI that provides access to the car rental price prediction model, allowing for seamless integration with other systems or applications.

#### API Overview
- **Framework**: FastAPI
- **Deployment**: Supports cloud deployment (configured for Hugging Face Spaces)
- **Documentation**: Auto-generated interactive Swagger UI at `/docs` endpoint
- **Model Integration**: Direct connection to the MLflow registered model

#### Endpoints
1. **Root Endpoint** (`GET /`)
   - Simple welcome message and documentation redirect

2. **Prediction Endpoint** (`POST /predict`)
   - Accepts car features as JSON input
   - Returns predicted rental price per day
   - Includes model version information

#### Input Features
The API accepts the following car characteristics for prediction:
- `model_key`: Car manufacturer (Citroën, Peugeot, BMW, etc., with fallback to "Others")
- `mileage`: Car mileage in kilometers
- `engine_power`: Engine power in horsepower
- `fuel`: Fuel type (diesel, petrol, hybrid_petrol, electro)
- `paint_color`: Car color (black, grey, white, red, etc.)
- `car_type`: Vehicle category (convertible, coupe, estate, sedan, etc.)
- `private_parking_available`: Whether private parking is available (boolean)
- `has_gps`: Whether the car has GPS (boolean)
- `has_air_conditioning`: Whether the car has A/C (boolean)
- `automatic_car`: Whether the car has automatic transmission (boolean)
- `has_getaround_connect`: Whether the car has Getaround Connect feature (boolean)
- `has_speed_regulator`: Whether the car has cruise control (boolean)
- `winter_tires`: Whether the car has winter tires (boolean)

#### Implementation Details
- Input validation with Pydantic models
- Automated data type conversion
- Comprehensive error handling
- Detailed API documentation with usage examples
- Integration with the MLflow model registry
- Model versioning support

The API allows for both individual predictions and potential batch integration, enabling real-time pricing recommendations for new car listings or adjustment of existing prices based on market conditions.

## Installation and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/pricing-optimization.git
cd pricing-optimization

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Streamlit App
```bash
cd streamlit
streamlit run app.py
```

### Using the API
```bash
cd api
uvicorn main:app --reload
```
Then navigate to http://localhost:8000/docs for the interactive API documentation.

### Running the Analysis Scripts
```bash
cd data_analysis
python analysis.py
```

## Dependencies

- Python 3.8+
- pandas, numpy, matplotlib, seaborn, plotly
- scikit-learn, catboost, mlflow
- streamlit
- fastapi, uvicorn, pydantic
- Other dependencies listed in requirements.txt

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.