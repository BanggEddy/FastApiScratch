from fastapi import FastAPI
import uvicorn
import os
import json
import pandas as pd
import numpy as np

app = FastAPI()

global df
df = pd.read_csv("kz.csv",sep=",")
df = df.dropna()
#Passer user_id et category_id de float64 vers int
df["user_id"] = df["user_id"].astype(np.int64)

df["category_id"] = df["category_id"].astype(np.int64)
print(df["user_id"])

# FONCTION PANDAS
def get_pandas_user(df,user_id):
    df_filtree = df[df["user_id"]==user_id]
    return df_filtree

def get_pandas_brand(df,brand):
    df_filtree = df[df["brand"]==brand]
    return df_filtree
def get_pandas_category_code(df, category_code):
    df_filtree = df[df["category_code"] == category_code]
    return df_filtree


def add_pandas_command(user_id, order_id, product_id, category_id, category_code, brand, price):
    global df

    # Create a DataFrame with the new row data
    new_row = pd.DataFrame({
        'event_time': ["2020-11-21 10:10:30 UTC"],
        'user_id': [user_id],
        'order_id': [order_id],
        'product_id': [product_id],
        'category_id': [category_id],
        'category_code': [category_code],
        'brand': [brand],
        'price': [price]
    })

    # Concatenate the new row with the existing DataFrame
    df = pd.concat([df, new_row], ignore_index=True)

    print(df.tail())  # Print the last few rows of the DataFrame
    return new_row

# FONCTION FASTAPI
@app.get("/get_user_id/")
async def get_user_id(user_id:int):
    df_filtree = get_pandas_user(df,user_id)
    return df_filtree.to_dict(orient="records")

@app.get("/get_brand/")
async def get_brand(brand:str):
    df_filtree = get_pandas_brand(df,brand)
    return df_filtree.to_dict(orient="records")

@app.get("/get-category-code-id/")
async def get_category_code(category_code:str):
    df_filtree = get_pandas_category_code(df,category_code)
    return df_filtree.to_dict(orient="records")



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)