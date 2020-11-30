from pymongo import MongoClient
import pandas as pd
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["Students"]

student_col = db["student"]   
df = pd.read_csv('data.csv', encoding='latin1')
data_json = json.loads(df.to_json(orient='records'))
student_col.insert_many(data_json)