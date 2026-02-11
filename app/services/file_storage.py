import os
from fastapi import UploadFile
from app.core.config import UPLOAD_DIR
import uuid

ALLOWED_EXTENSIONS = {".pdf"}


def save_pdf(file: UploadFile) -> str:
    _, ext = os.path.splitext(file.filename.lower())

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Only PDF files are allowed")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    unique_name = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    file.file.seek(0)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path
