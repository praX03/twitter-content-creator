
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def get_database():
    """
    Function to connect to the MongoDB database.
    Returns the database instance.
    """
    uri = "mongodb+srv://rental:rental@cluster0.jmkc9j2.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    db_client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        db_client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    return db_client["Cluster0"]  # replace with your database name

def insert_document(document):
    """
    Function to insert a document into a specified collection.
    """
    db = get_database()
    collection = db["twitter-content-bot-user-details"]
    collection.insert_one(document)
    return True
