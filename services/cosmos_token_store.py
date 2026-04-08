import os
from azure.cosmos.aio import CosmosClient
from azure.cosmos import PartitionKey
from dotenv import load_dotenv

load_dotenv()

COSMOS_URI = os.getenv("COSMOS_URI")
COSMOS_KEY = os.getenv("COSMOS_KEY")

DATABASE_NAME = "devguard"
CONTAINER_NAME = "token_usage"

MAX_TOKENS = 1000000
AVG_TOKENS_PER_REQUEST = 2000


class TokenStore:

    def __init__(self):
        if not COSMOS_URI:
            raise RuntimeError("COSMOS_URI not found")
        if not COSMOS_KEY:
            raise RuntimeError("COSMOS_KEY not found")

        self.client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
        self.database = None
        self.container = None

    # ✅ Initialize Cosmos DB
    async def init(self):
        if self.container:
            return  # already initialized

        print("[Cosmos] Connecting to database...")

        self.database = await self.client.create_database_if_not_exists(
            id=DATABASE_NAME
        )

        self.container = await self.database.create_container_if_not_exists(
            id=CONTAINER_NAME,
            partition_key=PartitionKey(path="/project_id")
        )

        print("[Cosmos] Connected successfully.")

    # ✅ Auto-init safety (CRITICAL FIX)
    async def _ensure_init(self):
        if self.container is None:
            print("[Cosmos] Auto-initializing (fallback)...")
            await self.init()

    # ✅ Close only at shutdown
    async def close(self):
        if self.client:
            await self.client.close()
            print("[Cosmos] Connection closed")

    # ✅ Get or create project
    async def get_or_create_project(self, project_id: str):

        await self._ensure_init()

        try:
            item = await self.container.read_item(
                item=project_id,
                partition_key=project_id
            )
            return item

        except Exception:
            print(f"[Cosmos] Creating new project record: {project_id}")

            new_item = {
                "id": project_id,
                "project_id": project_id,
                "tokens_used": 0,
                "token_quota": MAX_TOKENS
            }

            await self.container.create_item(body=new_item)
            return new_item

    # ✅ Check quota
    async def check_quota(self, project_id: str, estimated_tokens: int = AVG_TOKENS_PER_REQUEST):

        item = await self.get_or_create_project(project_id)

        tokens_used = item["tokens_used"]
        quota = item["token_quota"]
        remaining = quota - tokens_used

        if remaining <= 0 or remaining < estimated_tokens:
            print(f"[Token Store] Quota EXCEEDED — Used: {tokens_used}/{quota}")
            return {"allowed": False}

        print(f"[Token Store] Quota OK — Used: {tokens_used}/{quota}")
        return {"allowed": True}

    # ✅ Update tokens
    async def update_tokens(self, project_id: str, tokens_used_request: int):

        item = await self.get_or_create_project(project_id)

        item["tokens_used"] += tokens_used_request

        await self.container.replace_item(item=item, body=item)

        print(f"[Token Store] Updated — Used: {item['tokens_used']}")

        return item