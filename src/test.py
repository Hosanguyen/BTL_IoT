import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the variables
BROKER_URL = os.getenv('BROKER_URL')
BROKER_PORT = int(os.getenv('BROKER_PORT'))  # Convert to int if necessary
HOST = os.getenv('HOST')
HOST_PORT = int(os.getenv('HOST_PORT'))      # Convert to int if necessary
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB = os.getenv('MONGO_DB')

# Print to verify
print(f"BROKER_URL: {BROKER_URL}")
print(f"BROKER_PORT: {BROKER_PORT}")
print(f"HOST: {HOST}")
print(f"HOST_PORT: {HOST_PORT}")
print(f"MONGO_URI: {MONGO_URI}")
print(f"MONGO_DB: {MONGO_DB}")
