# dependencies.py
from fastapi import Body
from rag.service import vector_service
from rag.transform import embed
from model import TextModelRequest


async def get_rag_content(
    body: TextModelRequest = Body(...)
) -> str:
    """
    Fetch relevant context from vector DB based on user prompt
    """

    # 1. Convert user prompt → embedding
    query_vector = embed(body.prompt)

    # 2. Search vector DB for relevant chunks
    rag_results = await vector_service.search(
        collection_name="knowledgebase",
        query_vector=query_vector,
        retrieval_limit=3,
        score_threshold=0.7,
    )

    # 3. Extract original text from payload
    rag_content_str = "\n".join(
        [item.payload["original_text"] for item in rag_results]
    )

    return rag_content_str
