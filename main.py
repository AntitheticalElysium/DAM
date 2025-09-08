from fastapi import FastAPI
from pydantic import BaseModel
import joblib

model = joblib.load("regression.joblib")

app = FastAPI()

class HouseFeatures(BaseModel):
    size: float
    bedrooms: int
    garden: bool

# Browser test
@app.get("/predict")
async def predict_test():
    return {"y_pred": 2}

# POST for predictions
@app.post("/predict")
async def predict(features: HouseFeatures):
    garden_binary = 1 if features.garden else 0
    y_pred = model.predict([[features.size, features.bedrooms, garden_binary]])[0]
    return {"y_pred": y_pred}
