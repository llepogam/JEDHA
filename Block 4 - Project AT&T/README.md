# AT&T Spam Detection Project

## Project Overview
This project implements and compares different neural network architectures for SMS spam detection. The goal is to classify text messages as either spam ("unwanted, unsolicited messages") or ham ("legitimate messages"). Various models are built and evaluated to determine the most effective approach for this binary classification task.
Dataset
The project uses a standard SMS spam dataset containing labeled messages. Key dataset characteristics:

Binary classification: spam (1) or ham (0)
Text messages with varying lengths
Imbalanced dataset with fewer spam than ham messages

## Project Structure

1. Exploratory Data Analysis (EDA)

- Loading and examining the dataset
- Analyzing class distribution (~13% spam messages)
- Text consolidation and cleaning

2. Data Preprocessing

Text cleaning using SpaCy : 
- Removing non-alphanumeric characters
- Converting to lowercase
- Lemmatization
- Removing stop words
- Tokenization and sequence padding

3. Model Development

The project implements and compares five different models:

Basic Models

- Simple Embedding Model
- GRU Model
- LSTRM Model

Transfer Learning Models

- GloVe Model  : Pre-trained GloVe embeddings (100-dimensional)
- BERT Model : TensorFlow Hub BERT encoder (small_bert/bert_en_uncased_L-4_H-512_A-8)


4. Evaluation

All models are evaluated using standard classification metrics:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion matrices

Additionally, the models are tested on unseen examples to assess real-world performance.

## Key Findings

All basic models (Embedding, GRU, LSTM) achieved similar performance with ~98% accuracy and ~94% F1 score.

Different models offer different precision-recall trade-offs:
- Simple embedding model has higher precision
- GRU and LSTM models have higher recall


Surprisingly, transfer learning approaches (GloVe and BERT) did not significantly outperform the simpler models:
- GloVe performed poorly with only 74% recall
- BERT showed good precision but lower recall than the LSTM model


LSTM model achieved the best overall performance with the highest F1 score and recall

When tested on manually created spam examples, models showed inconsistent performance, suggesting that:
- Modern spam differs from training data patterns
- Models might need retraining on more recent data



## Conclusion
The LSTM model was selected as the best performing model due to its high recall (important for spam detection) and overall F1 score. The project demonstrates that sometimes simpler models can outperform complex transfer learning approaches, especially when working with specific domains like spam detection.
For practical deployment, the model would benefit from continuous retraining with newer spam samples to adapt to evolving spam patterns.