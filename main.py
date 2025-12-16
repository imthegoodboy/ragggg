from fastapi import FastAPI, UploadFile, File,status,HTTPException
from typing import Annotated
from upload import save_file

app = FastAPI()
@app.post("/upload")
async def file_upload(
    file:Annotated[UploadFile, File(description="Uploaded PDF documents")]
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are allowed")
    try:
        await save_file(file)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "File uploaded successfully","filename": file.filename}

 
