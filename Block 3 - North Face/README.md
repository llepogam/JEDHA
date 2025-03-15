# North Face Project

This project use clustering algorithme and  topic modeling  product descriptions. It processes a dataset of Northface product and applies natural language processing methods to identify patterns and group similar products.

## Overview
The notebook provides a comprehensive pipeline for analyzing textual product data:

- Data Loading and Preprocessing: Reads and cleans product descriptions
- Text Vectorization: Converts text to numerical features using NLP techniques
- Recommender System: Applies clustering algorithms to group similar products
- Topic Modeling: Extracts main topics from product descriptions and C=creates word clouds to visualize key terms in each topic

## Key Components

Data Preprocessing

- Text cleaning and normalization
- Tokenization and stopword removal
- Feature creation from product descriptions

Clustering with DBSCAN

- Multiple DBSCAN runs with different parameters (epsilon and min_samples)
- Cosine similarity metric for text comparison
- Identification of optimal clustering parameters
- Analysis of outliers in the dataset
- Word clouds visualisation

Topic Modeling

- Extraction of latent topics from product descriptions
- Word importance analysis for each topic
- Topic assignment to individual products
- Word clouds for visualizing important terms in each topic


