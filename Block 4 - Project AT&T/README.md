# AT&T Spam Detection Project

This repository contains a comprehensive SMS spam detection system that implements and compares multiple neural network architectures.

## 📋 Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
- [Models](#models)
- [Results](#results)
- [Conclusion](#conclusion)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview
This project aims to classify text messages as either spam or ham (legitimate) using various deep learning approaches. We implement and compare different neural network architectures to determine the most effective approach for SMS spam detection.

## 📊 Dataset
The project uses a standard SMS spam dataset containing labeled messages:
- Binary classification: spam (1) or ham (0)
- Text messages with varying lengths
- Imbalanced dataset with approximately 13% spam messages


## 🧠 Models
The project implements and compares five different models:

### Basic Models
1. **Simple Embedding Model**
   - Embedding layer followed by global average pooling
   - Multiple dense layers with dropout

2. **GRU Model**
   - Embedding layer
   - GRU layer with return sequences
   - Global max pooling
   - Multiple dense layers with dropout

3. **LSTM Model**
   - Embedding layer
   - LSTM layer with return sequences
   - Global max pooling
   - Multiple dense layers with dropout

### Transfer Learning Models
4. **GloVe Model**
   - Pre-trained GloVe embeddings (100-dimensional)
   - LSTM layer
   - Dense layer with sigmoid activation

5. **BERT Model**
   - TensorFlow Hub BERT encoder (small_bert/bert_en_uncased_L-4_H-512_A-8)
   - Dropout layer
   - Dense layer with sigmoid activation

## 📈 Results
Performance metrics for all models:

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Embedding | ~98% | High | Good | ~94% |
| GRU | ~98% | Good | High | ~95% |
| LSTM | ~98% | Good | High | ~94% |
| GloVe | Lower | Moderate | 74% | Lower |
| BERT | Good | High | Moderate | Good |

Key findings:
- Basic models achieved similar performance with excellent accuracy and F1 scores
- Different precision-recall trade-offs between models
- Transfer learning approaches did not significantly outperform simpler models
- GRU model demonstrated the best overall performance

## 🏆 Conclusion
The GRU model was selected as the best performing architecture due to its:
- High recall (critical for spam detection)
- Excellent overall F1 score
- Reasonable computational requirements compared to transfer learning approaches

