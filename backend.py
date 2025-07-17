from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import xgboost as xgb
import os
import uvicorn

app = FastAPI(
    title="Ad Budget Allocation API",
    description="Allocates marketing budget based on predicted revenue using XGBoost",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File paths
BASE_DIR = "C:\\Users\\virat\\OneDrive\\Documents\\MINI_P\\datasets"

DATASETS = {
    "google_ads_1": os.path.join(BASE_DIR, "googleads1-performance.csv"),
    "microsoft_ads_1": os.path.join(BASE_DIR, "microsoftads1-performance.csv"),
    "meta_ads_1": os.path.join(BASE_DIR, "metaads1-performance.csv"),
    "website_landings_1": os.path.join(BASE_DIR, "website-landings1.csv"),
    "google_ads_2": os.path.join(BASE_DIR, "googlead2-performance.csv"),
    "microsoft_ads_2": os.path.join(BASE_DIR, "microsoftads2-performance.csv"),
    "meta_ads_2": os.path.join(BASE_DIR, "metaads2-performance.csv"),
    "website_landings_2": os.path.join(BASE_DIR, "website-landings2.csv"),
}

def load_and_prepare_data():
    datasets = {}
    for name, path in DATASETS.items():
        try:
            df = pd.read_csv(path)
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            df["source"] = name.split("_")[0]  # google, microsoft, meta
            datasets[name] = df
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed loading {name}: {e}")
    return pd.concat([df for key, df in datasets.items() if "website" not in key], ignore_index=True)

# Train an XGBoost model
def train_model(data):
    data.fillna(0, inplace=True)

    features = ["cost", "clicks", "conversions"]
    target = "revenue"

    X = data[features]
    y = data[target]

    model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X, y)
    return model

@app.get("/budget_allocation/")
def budget_allocation(total_budget: float = 10000.0):
    data = load_and_prepare_data()
    model = train_model(data)

    # Predict revenue for each row
    data["predicted_revenue"] = model.predict(data[["cost", "clicks", "conversions"]])

    # Group by source and sum predictions
    source_performance = data.groupby("source").agg({
        "predicted_revenue": "sum"
    }).reset_index()

    total_predicted_revenue = source_performance["predicted_revenue"].sum()
    if total_predicted_revenue == 0:
        total_predicted_revenue = 1e-6  # Prevent division by zero

    # Allocate budget proportional to predicted revenue
    source_performance["allocation_ratio"] = source_performance["predicted_revenue"] / total_predicted_revenue
    source_performance["new_budget"] = (source_performance["allocation_ratio"] * total_budget).round(2)

    return source_performance[["source", "new_budget"]].to_dict(orient="records")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running smoothly with XGBoost!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
