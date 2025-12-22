# rag/service.py
import os
from loguru import logger
from .repository import VectorRepository
from .transform import clean, embed, load


class VectorService(VectorRepository):
    def __init__(self):
        super().__init__()

    async def store_file_content_in_db(
        self,
        filepath: str,
        chunk_size: int = 512,
        collection_name: str = "knowledgebase",
        collection_size: int = 768,
    ) -> None:
        # 1. Ensure the vector collection exists
        await self.create_collection(collection_name, collection_size)

        logger.debug(f"Inserting {filepath} content into database")

        # 2. Load file asynchronously, chunk by chunk
        async for chunk in load(filepath, chunk_size):
            logger.debug(f"Inserting '{chunk[0:20]}...' into database")

            # 3. Clean the text
            cleaned_text = clean(chunk)

            # 4. Convert text → embedding vector
            embedding_vector = embed(cleaned_text)

            # 5. Extract metadata (filename)
            filename = os.path.basename(filepath)

            # 6. Store vector + metadata in DB
            await self.create(
                collection_name,
                embedding_vector,
                cleaned_text,
                filename,
            )


# Single reusable service instance
vector_service = VectorService()
