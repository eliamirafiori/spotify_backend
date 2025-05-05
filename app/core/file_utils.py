from fastapi import UploadFile, File, HTTPException
from typing import Annotated
import os

ALLOWED_MIME_TYPES = {
    "audio/mpeg",  # .mp3
    "audio/wav",  # .wav
    "audio/x-wav",  # .wav
    "audio/aac",  # .aac
    "audio/mp4",  # .m4a
    "audio/flac",  # .flac
    "audio/alac",  # .alac
    "audio/aiff",  # .aiff, .aif
    "audio/x-aiff",  # .aiff, .aif
    "audio/ogg",  # .ogg
    "audio/x-ms-wma",  # .wma
}

ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".aac",
    ".m4a",
    ".flac",
    ".alac",
    ".aiff",
    ".aif",
    ".ogg",
    ".wma",
}


def validate_audio_file(file: UploadFile):
    # Validate MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    # Validate file extension
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file extension.")
