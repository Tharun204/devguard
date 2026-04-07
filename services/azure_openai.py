import os
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
import httpx

load_dotenv()

AZURE_ENDPOINT   = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_KEY        = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_VERSION    = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# HTTP client with extended timeout
http_client = httpx.AsyncClient(timeout=60.0)

# Azure OpenAI client
client = AsyncAzureOpenAI(
    api_key=AZURE_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=AZURE_VERSION,
    http_client=http_client,
)


async def call_llm(prompt: str, model: str = None):
    """Call Azure OpenAI chat completion."""

    deployment = model or AZURE_DEPLOYMENT

    response = await client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    content     = response.choices[0].message.content
    tokens_used = response.usage.total_tokens

    return content, tokens_used