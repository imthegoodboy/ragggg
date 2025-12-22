# main.py
from fastapi import (
    FastAPI,
    Request,
    Body,
    Depends,
    HTTPException,
    status,
)
from dependencies import get_rag_content
from model import TextModelRequest, TextModelResponse, models, generate_text

app = FastAPI()


@app.post("/generate/text", response_model_exclude_defaults=True)
async def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    rag_content: str = Depends(get_rag_content),
) -> TextModelResponse:
    # 1. Validate model
    if body.model not in models:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid model selected",
        )

    # 2. Augment user prompt with RAG context
    final_prompt = body.prompt + "\n\n" + rag_content

    # 3. Generate response using LLM
    output = generate_text(
        models[body.model],
        final_prompt,
        body.temperature,
    )

    return TextModelResponse(
        content=output,
        ip=request.client.host,
    )
