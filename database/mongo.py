from pymongo import MongoClient

client = MongoClient(
"mongodb+srv://abhishek20:abhishek123123@cluster0.85usmfn.mongodb.net/?appName=Cluster0"
)

db = client["resume_analyzer"]

collection = db["candidates"]
