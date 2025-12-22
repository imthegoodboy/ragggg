from pydantic import BaseModel
from transformers import pipeline

class TextModelRequest(BaseModel):
    prompt: str
    model: str = "tiny-gpt2"
    temperature: float = 0.7

class TextModelResponse(BaseModel):
    content: str
    ip: str

# Initialize a low memory model
try:
    # We use a pipeline for simplicity
    # Using sshleifer/tiny-gpt2 as an extremely low memory model
    model_name = "sshleifer/tiny-gpt2"
    generator = pipeline("text-generation", model=model_name)
    models = {
        "tiny-gpt2": generator
    }
except Exception as e:
    print(f"Warning: Could not load {model_name} model. Error: {e}")
    models = {}

def generate_text(model, prompt: str, temperature: float = 0.7) -> str:
    """
    Generate text using the provided model pipeline.
    """
    try:
        # Generate text
        # truncating to avoid potential length issues, though distilgpt2 handles up to 1024
        result = model(
            prompt, 
            max_length=200, 
            num_return_sequences=1, 
            temperature=temperature,
            truncation=True,
            do_sample=True
        )
        return result[0]['generated_text']
    except Exception as e:
        return f"Error during generation: {str(e)}"
