# """
# FastAPI routes.
# Defines all API endpoints for the application.
# """

# import os
# from datetime import datetime
# from typing import Optional

# from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile

# from app.config import get_config
# from app.exceptions import AutoDocThinkerError, ValidationError
# from app.utils.logger import get_logger
# from app.utils.validators import (
#     get_file_type,
#     sanitize_filename,
#     validate_file_extension,
#     validate_query,
#     validate_text_input,
#     validate_url,
# )
# from app.workflow import process_query

# logger = get_logger("api")

# # Create routers
# main_router = APIRouter()
# router = APIRouter()


# @main_router.get("/health")
# async def health_check():
#     """Health check endpoint."""
#     return {
#         "status": "healthy",
#         "version": "2.0.0",
#         "timestamp": datetime.now().isoformat(),
#     }


# # ============== API Routes ==============


# @router.post("/process")
# async def process(
#     request: Request,
#     query: str = Form(...),
#     content_type: str = Form("file"),
#     file: Optional[UploadFile] = File(None),
#     url: Optional[str] = Form(None),
#     text: Optional[str] = Form(None),
# ):
#     """
#     Process a query with optional document/URL/text input.

#     Args:
#         query: User's question
#         content_type: 'file', 'url', or 'text'
#         file: Uploaded file (for content_type='file')
#         url: Web URL (for content_type='url')
#         text: Direct text (for content_type='text')

#     Returns:
#         JSON with answer and source
#     """
#     try:
#         config = get_config()

#         # Validate query
#         query = query.strip()
#         validate_query(query)

#         file_path = None
#         file_type = None

#         # Handle different content types
#         if content_type == "file":
#             if not file or not file.filename:
#                 raise ValidationError("Please upload a valid file (PDF, DOCX, TXT)")

#             # Validate extension
#             validate_file_extension(file.filename)
#             file_type = get_file_type(file.filename)

#             # Create secure filename with timestamp
#             original_name = sanitize_filename(file.filename)
#             filename = f"{datetime.now().timestamp()}_{original_name}"

#             # Save file
#             os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
#             file_path = os.path.join(config.UPLOAD_FOLDER, filename)

#             content = await file.read()
#             with open(file_path, "wb") as f:
#                 f.write(content)

#             logger.info(f"File uploaded: {filename}")

#         elif content_type == "url":
#             if not url:
#                 raise ValidationError("Please provide a URL")
#             url = url.strip()
#             validate_url(url)
#             file_path = url
#             file_type = "url"
#             logger.info(f"URL provided: {url}")

#         elif content_type == "text":
#             if not text:
#                 raise ValidationError("Please provide text content")
#             text = text.strip()
#             validate_text_input(text)

#             # Save text to temporary file
#             filename = f"{datetime.now().timestamp()}_text.txt"
#             file_path = os.path.join(config.UPLOAD_FOLDER, filename)
#             os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

#             with open(file_path, "w", encoding="utf-8") as f:
#                 f.write(text)
#             file_type = "txt"
#             logger.info(f"Text content saved to: {filename}")

#         else:
#             raise ValidationError("Invalid content type")

#         # Process the query
#         logger.info(f"Processing query: {query[:50]}...")
#         answer, source = process_query(
#             input_text=query, file_path=file_path, file_type=file_type
#         )

#         # Get document count for metadata
#         try:
#             from app.services.vector_store import get_vector_store

#             vector_store = get_vector_store()
#             chunk_count = vector_store.get_document_count()
#         except Exception:
#             chunk_count = 0

#         return {"answer": answer, "source": source, "metadata": {"chunks": chunk_count}}

#     except ValidationError as e:
#         logger.warning(f"Validation error: {e}")
#         raise HTTPException(status_code=400, detail=str(e))

#     except AutoDocThinkerError as e:
#         logger.error(f"Application error: {e}")
#         raise HTTPException(status_code=e.status_code, detail=str(e))

#     except Exception as e:
#         logger.error(f"Unexpected error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/documents/count")
# async def get_document_count():
#     """Get the number of documents in the vector store."""
#     try:
#         from app.services.vector_store import get_vector_store

#         vector_store = get_vector_store()
#         count = vector_store.get_document_count()

#         return {"count": count, "has_documents": count > 0}
#     except Exception as e:
#         logger.error(f"Failed to get document count: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/documents/clear")
# async def clear_documents():
#     """Clear all documents from the vector store."""
#     try:
#         from app.services.vector_store import get_vector_store

#         vector_store = get_vector_store()
#         vector_store.clear()

#         return {"status": "success", "message": "All documents cleared"}
#     except Exception as e:
#         logger.error(f"Failed to clear documents: {e}")
#         raise HTTPException(status_code=500, detail=str(e))



"""
FastAPI routes.
Defines all API endpoints for the application.
"""

import os
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile

from app.config import get_config
from app.exceptions import AutoDocThinkerError, ValidationError
from app.utils.logger import get_logger
from app.utils.validators import (
    get_file_type,
    sanitize_filename,
    validate_file_extension,
    validate_query,
    validate_text_input,
    validate_url,
)
from app.workflow import process_query

logger = get_logger("api")

main_router = APIRouter()
router = APIRouter()


@main_router.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
    }


# ===============================
# PROCESS QUERY
# ===============================

@router.post("/process")
async def process(
    request: Request,
    query: str = Form(...),
    content_type: str = Form("file"),
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    text: Optional[str] = Form(None),
):

    try:

        config = get_config()

        query = query.strip()
        validate_query(query)

        file_path = None
        file_type = None

        # ------------------------------------------------
        # DOCUMENT UPLOAD (ONLY WHEN FILE EXISTS)
        # ------------------------------------------------

        if content_type == "file" and file and file.filename:

            validate_file_extension(file.filename)
            file_type = get_file_type(file.filename)

            original_name = sanitize_filename(file.filename)
            filename = f"{datetime.now().timestamp()}_{original_name}"

            os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

            file_path = os.path.join(config.UPLOAD_FOLDER, filename)

            content = await file.read()

            with open(file_path, "wb") as f:
                f.write(content)

            logger.info(f"File uploaded: {filename}")

        # ------------------------------------------------
        # URL INPUT
        # ------------------------------------------------

        elif content_type == "url" and url:

            url = url.strip()
            validate_url(url)

            file_path = url
            file_type = "url"

            logger.info(f"URL provided: {url}")

        # ------------------------------------------------
        # TEXT INPUT
        # ------------------------------------------------

        elif content_type == "text" and text:

            text = text.strip()
            validate_text_input(text)

            filename = f"{datetime.now().timestamp()}_text.txt"

            os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

            file_path = os.path.join(config.UPLOAD_FOLDER, filename)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)

            file_type = "txt"

            logger.info(f"Text content saved to: {filename}")

        # ------------------------------------------------
        # NO FILE → JUST QUESTION
        # ------------------------------------------------

        else:

            logger.info("No new document uploaded. Using existing vector store.")

        # ------------------------------------------------
        # RUN WORKFLOW
        # ------------------------------------------------

        logger.info(f"Processing query: {query[:50]}...")

        answer, source = process_query(
            input_text=query,
            file_path=file_path,
            file_type=file_type,
        )

        try:

            from app.services.vector_store import get_vector_store

            vector_store = get_vector_store()

            chunk_count = vector_store.get_document_count()

        except Exception:

            chunk_count = 0

        return {
            "answer": answer,
            "source": source,
            "metadata": {"chunks": chunk_count},
        }

    except ValidationError as e:

        logger.warning(f"Validation error: {e}")

        raise HTTPException(status_code=400, detail=str(e))

    except AutoDocThinkerError as e:

        logger.error(f"Application error: {e}")

        raise HTTPException(status_code=e.status_code, detail=str(e))

    except Exception as e:

        logger.error(f"Unexpected error: {e}")

        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# VECTOR STORE INFO
# ===============================

@router.get("/documents/count")
async def get_document_count():

    try:

        from app.services.vector_store import get_vector_store

        vector_store = get_vector_store()

        count = vector_store.get_document_count()

        return {"count": count, "has_documents": count > 0}

    except Exception as e:

        logger.error(f"Failed to get document count: {e}")

        raise HTTPException(status_code=500, detail=str(e))


@router.post("/documents/clear")
async def clear_documents():

    try:

        from app.services.vector_store import get_vector_store

        vector_store = get_vector_store()

        vector_store.clear()

        return {
            "status": "success",
            "message": "All documents cleared",
        }

    except Exception as e:

        logger.error(f"Failed to clear documents: {e}")

        raise HTTPException(status_code=500, detail=str(e))