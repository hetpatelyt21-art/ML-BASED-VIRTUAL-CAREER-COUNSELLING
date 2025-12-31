import joblib
import pandas as pd

model = joblib.load('core/ml/random_forest_model.pkl')

def predict_basic_test_result(responses):
    data = {f"Q{i}": responses.get(f"Q{i}", 0) for i in range(1, 21)}
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return prediction
