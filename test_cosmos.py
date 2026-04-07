import os
from azure.cosmos import CosmosClient

uri = os.environ.get("COSMOS_URI")
key = os.environ.get("COSMOS_KEY")

if not uri or not key:
    raise ValueError("COSMOS_URI or COSMOS_KEY not set in environment variables")

print("🔄 Connecting to Cosmos DB...")
client = CosmosClient(uri, credential=key)

for db in client.list_databases():
    print("✅ Found database:", db['id'])
