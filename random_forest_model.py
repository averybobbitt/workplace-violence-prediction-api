import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split, cross_val_score

# Creates and trains a random forest model
def create_random_forest_model(data):
    X = data.drop(['Current Time', 'Workplace Violence'], axis=1)
    y = data['Workplace Violence']
    # 70 % training dataset and 30 % test datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)
    rf = RandomForestClassifier(n_estimators=100)
    # Training the model on the training dataset
    # fit function is used to train the model using the training sets as parameters
    rf.fit(X_train, y_train)
    return rf

def make_prediction(model, X_test):
    y_pred = model.predict(X_test)
    return y_pred

def make_prob_prediction(model, X_test):
    y_pred = model.predict_proba(X_test)
    return y_pred