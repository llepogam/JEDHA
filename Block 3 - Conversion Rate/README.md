# Conversion Rate Prediction

This notebook builds a machine learning model to predict customer conversion rates based on user behavior and demographic data. 

## Dataset

The dataset contains information about website visitors with the following features:
- **Country**: Origin country (China, Germany, UK, US)
- **Age**: Age of the user
- **New_User**: Whether it's a first-time visitor (1) or a returning user (0)
- **Source**: Traffic source (Ads, Direct, SEO)
- **Total_pages_visited**: Number of pages visited by the user
- **Converted**: Target variable (1 = converted, 0 = not converted)

## Project Structure

1. **Exploratory Data Analysis (EDA)**
   - Initial data examination
   - Distribution analysis
   - Conversion rate analysis by demographic and behavioral factors

2. **Data Preprocessing**
   - Feature engineering
   - Train/test split
   - Handling categorical features with one-hot encoding
   - Standardizing numerical features

3. **Model Development**
   - Logistic Regression implementation
   - Performance evaluation on training and test sets
   - Analysis of model coefficients

4. **Model Comparison**
   - Testing alternative algorithms:
     - Logistic Regression
     - Random Forest
     - Decision Tree
     - XGBoost
     - AdaBoost
   - Cross-validation with multiple metrics (Accuracy, F1, Recall, Precision)
   - Selection of best-performing model

5. **Final Model & Predictions**
   - Training on complete dataset
   - Generating predictions for test dataset
   - Exporting results to CSV

## Key Findings

- **Geographic differences**: German and UK users convert at significantly higher rates than Chinese users
- **User retention**: Returning users are much more likely to convert than new users
- **Engagement**: Higher page visits strongly correlate with increased conversion probability
- **Age**: Younger users tend to have higher conversion rates
- **Traffic source**: All traffic sources (Ads, Direct, SEO) perform similarly

## Business Recommendations

1. **Geographic targeting**: Address product-market fit issues in China through localization or technical improvements
2. **Focus on retention**: Implement strategies to encourage repeat visits
3. **Increase engagement**: Design website experience to encourage visitors to explore more pages
4. **Age targeting**: Consider campaigns targeting younger demographics
5. **Channel efficiency**: Since all traffic sources convert similarly, optimize marketing spend based on acquisition costs

## Model Performance

The Logistic Regression model achieved:
- Accuracy: ~98%
- F1 : ~75%
- Recall : ~68%
- Good overall performance, though recall on converted users could be improved

