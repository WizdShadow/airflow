import os

import pandas as pd
import json
import dill
import glob

def predict():
    predict = []
    fils = glob.glob("data/models/*.pkl")

    with open(fils[0], "rb") as f:
        model = dill.load(f)
    
    for  fil in os.listdir("data/test"):
            
        with open(f"data/test/{fil}", "r") as f:
            data = json.load(f)
    
        df = pd.DataFrame([data])
        predict.append(model.predict(df)[0])
    
    df = pd.DataFrame({"predict": predict,})
    df.to_csv("data/predictions/predict.csv", index=False)


if __name__ == '__main__':
    predict()
