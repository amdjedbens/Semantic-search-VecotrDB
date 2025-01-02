import os
import sys
from dotenv import load_dotenv, find_dotenv
import time
from pinecone import ServerlessSpec
import pinecone

class Utils:
    def __init__(self):
        # load .env file
        load_dotenv(find_dotenv())

    def get_openai_api_key(self):
        # load .env file
        # get the api key
        return os.getenv("OPENAI_API_KEY")
    
    def get_pinecone_api_key(self):
        load_dotenv(find_dotenv())
        return os.getenv("PINECONE_API_KEY")
    
    def create_dlai_index_name(self, pinecone_obj, index_name, dimension=384):
        #return f"course-{index_name}-{int(time.time())}"
        pinecone_client = pinecone_obj
        # Check if the index exists and delete it (using a set comprehension for faster lookup)
        index_names = {index.name for index in pinecone.list_indexes()}
        try: 

            if index_name in index_names:
                pinecone_client.delete_index(index_name)
                print(f"Deleted existing index: {index_name}")
            print(f"Creating index: {index_name}")
            # Create a Pinecone index with the name INDEX_NAME
            pinecone.create_index(
                index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region='us-east-1')
            )
            print(f"Created index: {index_name}")
            
        except Exception as e:
            print(f"Error creating index: {e}")
        return index_name
