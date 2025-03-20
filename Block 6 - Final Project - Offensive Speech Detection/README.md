# Offensive Speech Detection

This repository contains the code and resources for an offensive speech detection system, which identifies potentially harmful content in text. The project includes a machine learning model trained on tweet data, an API for making predictions, and a user-friendly web application.

## Project Overview

The goal of this project is to build and deploy a fully functional offensive speech detection model that can accurately classify text as either offensive or non-offensive. With major tech platforms reducing their content moderation efforts, tools like this have become increasingly important for maintaining healthy online spaces.

### Key Features

- Machine learning model trained on the OLID (Offensive Language Identification Dataset)
- RESTful API for text classification
- User-friendly web interface for easy interaction
- Comprehensive model evaluation metrics
- Complete MLflow experiment tracking

## Dataset

The project uses the Offensive Language Identification Dataset (OLID), which contains:
- 13,240 annotated tweets
- 33.2% of tweets labeled as offensive (4,400 tweets)
- Binary classification: offensive/not offensive
- Available on Hugging Face

The dataset was introduced in the paper "Predicting the Type and Target of Offensive Posts in Social Media" (2019).

## Preliminary Analysis

Several neural network architectures were tested to determine the most effective approach:

| Model | Description | Preprocessing | Results |
|-------|-------------|---------------|---------|
| GRU | Gated recurrent units with embedding layer, 1 GRU layer (64 units), max pooling/dropout/dense final layers | Text cleaning, lemmatization, stop words removal, encoding and padding | F1 Score: 0.63, Recall: 0.66, Accuracy: 0.74 |
| LSTM | Long short-term memory with embedding layer, 2 LSTM layers (64 units), max pooling/dropout/dense final layers | Text cleaning, lemmatization, stop words removal, encoding and padding | F1 Score: 0.61, Recall: 0.58, Accuracy: 0.75 |
| BERT | Pre-trained BERT model with dropout and dense final layers | Text cleaning, lemmatization, stop words removal, BERT preprocessing | F1 Score: 0.59, Recall: 0.57, Accuracy: 0.73, 3h training time |

Based on these results, the GRU architecture was selected for further development due to its superior recall and F1 score, which are crucial metrics for offensive speech detection.

## Model Fine-Tuning with MLflow

MLflow was used to track experiments and optimize the model:

- The final model achieved 73% accuracy and 68% recall
- Multiple experiments were conducted varying:
  - Number of units in each layer
  - Addition of intermediate layers
  - Number of epochs for training
- Both the prediction model and a separate preprocessing model were registered in MLflow

Due to limitations with MLflow and TensorFlow integration, the preprocessing and prediction functionalities were split into two separate models:
1. **Text Preprocessor Model**: Handles text cleaning, lemmatization, and stop word removal
2. **Prediction Model**: Focuses on vectorization, embedding, and classification

The complete preprocessing pipeline includes:
1. Text cleaning (punctuation/symbol removal, lowercase conversion)
2. Lemmatization and stop words removal
3. Text vectorization and padding

## API Development

A FastAPI-based REST API was created to serve the model:

- Two key endpoints:
  - `/preprocess`: Cleans and prepares text for the model
  - `/predict`: Provides classification and probability score
- Comprehensive documentation with examples
- Deployed on Hugging Face Spaces

Example API usage:
```python
import requests

url = "https://llepogam-hate-speech-detection-api.hf.space/predict"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

data = {
    "Text": "your text here"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## Web Application

A Streamlit application was developed to provide a user-friendly interface:

- Clean, intuitive design
- Visual indication of prediction confidence
- Analysis history tracking with S3 bucket storage
- Detailed FAQ section
- Responsive confidence meter visualization


## Future Improvements

Potential enhancements for future iterations:

1. **Model Improvements**:
   - Train on larger datasets
   - Implement more advanced model architectures
   - Leverage the latest pre-trained models

2. **Application Performance**:
   - Optimize for faster prediction
   - Upgrade server infrastructure
   - Improve error handling

3. **User Interface**:
   - Add batch prediction from CSV files
   - Implement additional visualization options
   - Enhance user feedback mechanisms

