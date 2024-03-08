from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# Creates and trains a random forest model
def create_model(data):
    x = data.drop(['Current Time', 'Workplace Violence'], axis=1)
    y = data['Workplace Violence']
    # 70 % training dataset and 30 % test datasets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)
    rf = RandomForestClassifier(n_estimators=100)
    # Training the model on the training dataset
    # fit function is used to train the model using the training sets as parameters
    rf.fit(x_train, y_train)
    return rf


def predict(model, X_test):
    y_pred = model.predict(X_test)
    return y_pred


def predict_prob(model, X_test):
    y_pred = model.predict_proba(X_test)
    return y_pred
