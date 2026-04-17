import pickle
import pandas as pd

# Load model once
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)


def predict_price(data):
    df = pd.DataFrame([data])

    prediction = model.predict(df)[0]

    return round(prediction, 2)