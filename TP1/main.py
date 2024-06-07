import pandas as pd
from fastapi import FastAPI
import numpy as np
import uvicorn
import logging  # Import the logging module

app = FastAPI()

Csv = pd.read_csv('kz.csv')  # Read the CSV file into the Csv variable

# Ensure user_id, brand, and category_id columns are integers
Csv['user_id'] = Csv['user_id'].fillna(0).astype(np.int64)
Csv['brand'] = Csv['brand'].fillna(0)
Csv['category_id'] = Csv['category_id'].fillna(0).astype(np.int64)

def get_pandas_user(df, user_id):
    df_filtered = df[df["user_id"] == user_id]
    return df_filtered

def get_pandas_brand(df, brand):
    df_filtered = df[df["brand"] == brand]
    return df_filtered

@app.get("/get_user/{user_id}")
async def get_user(user_id: int):
    df_filtered = get_pandas_user(Csv, user_id)  # Pass Csv to the function
    return df_filtered

@app.get("/get_brand/{brand}")
async def get_brand(brand: str):
    try:
        df_filtered = get_pandas_brand(Csv, brand)  # Pass Csv to the function
        # Convert np.int64 to Python's built-in int type to ensure JSON serialization
        df_filtered['user_id'] = df_filtered['user_id'].astype(int)
        df_filtered['category_id'] = df_filtered['category_id'].astype(int)
        return df_filtered.to_dict(orient="records")
    except Exception as e:
        logger = logging.getLogger(__name__)  # Define the logger
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
