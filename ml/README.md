# Machine Learning Modelisation

Welcome to the Machine Learning section of our Automatic Essay Grading project. This directory contains all the necessary components for the machine learning pipeline, from initial data analysis to the training of sophisticated models.

## Overview

This section is organized into several key areas:
- `preprocessing/`: Scripts and notebooks for data cleaning, feature extraction, and preparation.
- `training/`: Notebooks and scripts used for training various machine learning models.
- `error_analysis/`: Tools and notebooks for analyzing the performance and errors of the models.

## Preprocessing

The preprocessing stage is crucial for preparing the raw data for effective machine learning model training. This involves:
- Exploratory Data Analysis (EDA) to understand the dataset.
- Sampling techniques to handle imbalanced data, ensuring robust model training.

## Training

Here, we explore various machine learning approaches:
- Basic models using techniques like TF-IDF.
- Advanced models using GloVe embeddings.
- Cutting-edge approaches with transformers that are fine-tuned for our specific task.

## Error Analysis

After training, it is essential to evaluate the model comprehensively:
- `benchmark.ipynb`: Compares different models and their performance metrics.
- `transformers_ea.ipynb`: Deep dive into the transformer models' performance and error types.