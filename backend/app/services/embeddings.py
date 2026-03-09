"""
Embeddings service using Google Gemini API.
Generates text embeddings for semantic similarity matching.

To swap ChromaDB for Pinecone:
  - Replace `chromadb` imports with `pinecone`
  - Change `client = chromadb.Client()` to `pinecone.init(api_key=..., environment=...)`
  - Replace `collection.add(...)` with `index.upsert(...)`
  - Replace `collection.query(...)` with `index.query(...)`
"""
import asyncio
from typing import List
from google import genai
from app.core.config import settings

# Embedding model to use (free tier)
EMBEDDING_MODEL = "text-embedding-004"

# ─────────────────────────────────────────────
# ChromaDB (local vector search — free, no account needed)
# Uncomment the block below to use ChromaDB instead of in-memory comparison:
#
# import chromadb
# chroma_client = chromadb.Client()
# job_collection = chroma_client.get_or_create_collection(
#     name="jobs",
#     metadata={"hnsw:space": "cosine"}
# )
#
# def add_job_to_chroma(job_id: int, embedding: List[float], metadata: dict):
#     job_collection.add(
#         ids=[str(job_id)],
#         embeddings=[embedding],
#         metadatas=[metadata]
#     )
#
# def search_jobs_in_chroma(query_embedding: List[float], n_results: int = 5):
#     results = job_collection.query(
#         query_embeddings=[query_embedding],
#         n_results=n_results
#     )
#     return results
# ─────────────────────────────────────────────


def _get_client() -> genai.Client:
    """Create and return a Gemini client using the configured API key."""
    if not settings.gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured. "
            "Get your free key at: https://aistudio.google.com/apikey"
        )
    return genai.Client(api_key=settings.gemini_api_key)


async def generate_embedding(text: str) -> List[float]:
    """
    Generate a text embedding vector using Google Gemini API.

    Args:
        text: The text to embed (resume text or job description).

    Returns:
        A list of floats representing the embedding vector.

    Raises:
        ValueError: If the API call fails or returns invalid data.
    """
    if not settings.gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured. "
            "Get your free key at: https://aistudio.google.com/apikey"
        )

    # Truncate very long texts to avoid API limits (max ~2048 tokens)
    truncated_text = text[:8000] if len(text) > 8000 else text

    try:
        client = _get_client()
        # Use the async client (client.aio) to keep FastAPI async
        result = await client.aio.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=truncated_text,
        )
        # result.embeddings is a list of ContentEmbedding objects
        if not result.embeddings:
            raise ValueError("Gemini returned empty embeddings")
        return list(result.embeddings[0].values)
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to generate embedding: {str(e)}")


async def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts.
    Processes them concurrently for speed.

    Args:
        texts: List of text strings to embed.

    Returns:
        List of embedding vectors, one per input text.
    """
    tasks = [generate_embedding(text) for text in texts]
    return await asyncio.gather(*tasks)
