# Walmart Store Sales Analysis

## Project Overview
The target of this project is to analyze and predict weekly sales figures from Walmart stores

## Dataset
The analysis uses the "Walmart_Store_sales.csv" dataset which includes:
- Weekly sales figures across multiple Walmart stores
- Economic indicators (CPI, unemployment rate, fuel prices)
- Temporal features (date information)
- Store-specific attributes
- Holiday flag indicators

## Key Features
- Comprehensive exploratory data analysis (EDA) of Walmart sales patterns
- Visualization of sales trends, store performance, and economic factor correlations
- Implementation of multiple regression models with regularization techniques
- Store clustering analysis based on performance metrics
- Feature importance evaluation to identify key sales drivers

## Technical Implementation
- **Data Preprocessing**: Handling missing values, date transformation, feature engineering
- **Visualization**: Interactive plots created with Plotly for sales trends and correlations
- **Machine Learning Pipeline**: Scikit-learn implementation with:
  - Linear regression as baseline model
  - Ridge and Lasso regression for regularization
  - K-means clustering for store segmentation
  - Cross-validation and hyperparameter tuning
- **Evaluation Metrics**: R² score used to assess model performance

## Key Findings
- Significant variation in sales performance between different stores
- Store-specific characteristics are the strongest predictors of sales
- No clear seasonality observed in the monthly sales patterns
- Limited dataset size (75 complete records after cleaning) restricts model performance
- Regularization techniques did not significantly improve predictive performance
- Store clustering based on performance metrics did not enhance prediction accuracy

## Limitations
- Small sample size limits model generalizability
- Lack of sufficient historical data per store (maximum 8 weekly records)
- Store-specific effects dominate predictions, making forecasting for new stores challenging

## Future Work
- Collect additional historical sales data to improve model robustness
- Explore advanced time series forecasting methods
- Incorporate additional features such as product categories and promotions
- Develop store-specific models to account for location uniqueness
- Implement ensemble methods to improve prediction accuracy

