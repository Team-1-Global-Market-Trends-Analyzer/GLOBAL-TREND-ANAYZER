import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def train_model(data: pd.DataFrame):
    X = data[["revenue", "market_cap"]]
    y = data["performance_score"]  # Add performance score column in your dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def predict_performance(model, revenue, market_cap):
    prediction = model.predict([[revenue, market_cap]])
    return prediction[0]
