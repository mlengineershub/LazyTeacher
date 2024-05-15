# Data Directory for Automatic Essay Grading

Welcome to the Data directory of our Automatic Essay Grading project. This section of the repository contains all the datasets used for training, validating, and testing the machine learning models.

## Overview

This directory is organized to ensure easy access to various types of data needed throughout different stages of the project:

- `test.csv`: Data used for final testing of the models to evaluate their performance.
- `train.csv`: Training data used to build the models.
- `train_oversampled.csv`: Oversampled training data to handle class imbalance.
- `train_under.csv`: Undersampled training data for experimentation on reduced class imbalance.
- `val.csv`: Validation data used during the model tuning phase.
- `val_oversampled.csv`: Oversampled validation data.
- `val_under.csv`: Undersampled validation data.

## Data Description

Each dataset includes a collection of student essays along with their respective grades, which range from 1 to 6. The essays are evaluated based on various criteria, including grammar, coherence, logic, and overall quality of argumentation.

## Usage

These datasets are used at different stages of the machine learning pipeline:

- **Training Data (`train.csv`)**: Used to train the initial models.
- **Oversampled/Undersampled Training Data**: Used to evaluate the impact of different sampling techniques on model performance.
- **Validation Data (`val.csv`)**: Helps in tuning the models to avoid overfitting and to optimize performance.
- **Testing Data (`test.csv`)**: Used to assess the model in a scenario that mimics real-world application.

## Contributing

If you have suggestions for additional datasets or improvements in data preprocessing, please feel free to contribute. Detailed instructions on how to contribute can be found in the main project README.

## Contact

For questions or additional information about the datasets, refer to the main project README or reach out directly to the contributors via their GitHub profiles.
