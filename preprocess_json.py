import requests
import os
import json
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity


def create_embedding(text_list):
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )

    # print("Status Code:", r.status_code)
    # print("Response:", r.text)

    data = r.json()

    if "embeddings" not in data:
        raise Exception(f"Ollama Error: {data}")

    return data["embeddings"]

jsons = os.listdir("merged_jsons")  #list all the jsons    
my_dicts = []
chunk_id = 0


for json_file in jsons:
    with open(f"merged_jsons/{json_file}", encoding="utf-8") as f:
        content  = json.load(f)
    print(f"creating embedding for {json_file}")

    embeddings = create_embedding([c["text"] for c in content["chunks"]])

    for i, chunk in enumerate(content["chunks"]):
        chunk["chunks_id"] = chunk_id
        chunk["embedding"] = embeddings[i]
        chunk_id += 1
        my_dicts.append(chunk)
        # if(i==3):  #read 5 chunks for now
        #     break
    # break
        
        
 
        
# print(my_dicts) 


# from rows to dataframes
df = pd.DataFrame.from_records(my_dicts)  
# print(df)

# 1. Save the model to a file
joblib.dump(df, 'embeddings.joblib')



